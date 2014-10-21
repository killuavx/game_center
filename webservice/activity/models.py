# -*- coding: utf-8 -*-
from model_utils import FieldTracker
from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.db.models.query import QuerySet
from django.utils.timezone import now
from mezzanine.core.models import TimeStamped, CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT
from mezzanine.utils.models import get_user_model_name

from activity.managers import GiftBagManager, GiftCardManager, BulletinManager, ActivityManager
from toolkit.models import PublishDisplayable, SiteRelated
from toolkit.helpers import current_request, get_global_site
from toolkit.helpers import sync_status_from


class EmptyRemainingGiftCard(Exception):
    pass


user_model_name = get_user_model_name()


class GiftBag(PublishDisplayable,
              SiteRelated,
              TimeStamped,
              models.Model):

    objects = GiftBagManager()

    title = models.CharField(max_length=500)

    for_package = models.ForeignKey('warehouse.Package',
                                    verbose_name='应用',
                                    related_name='giftbags')

    for_version = models.ForeignKey('warehouse.PackageVersion',
                                    verbose_name='应用版本',
                                    related_name='giftbags',
                                    null=True,
                                    blank=True)

    summary = models.CharField(verbose_name='礼包内容', max_length=500)

    usage_description = models.TextField(verbose_name='使用方法')

    issue_description = models.TextField(verbose_name='发号说明')

    cards_remaining_count = models.IntegerField(default=0, editable=False)

    cards_total_count = models.IntegerField(default=0, editable=False)

    publisher = models.ForeignKey(user_model_name,
                                  on_delete=models.DO_NOTHING)

    tracker = FieldTracker()

    def clean(self):
        super(GiftBag, self).clean()
        if self.for_version_id is not None:
            if self.for_version.package_id != self.for_package_id:
                raise ValidationError('PackageVersion (%s) Does not belong to Package (%s)' %(self.for_version,
                                                                                              self.for_package))

    def save(self, *args, **kwargs):
        if self.publisher_id is None:
            self.publisher = current_request().user
        if self.cards_remaining_count == 0:
            self.status = CONTENT_STATUS_DRAFT
        return super(GiftBag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '礼包'
        verbose_name_plural = '礼包'
        index_together = (
            ('site', 'for_package',),
            ('site', 'for_package', 'for_version'),

            ('site', 'publish_date', ),
            ('site', 'for_package', 'publish_date',),
            ('site', 'for_package', 'for_version', 'publish_date', ),

            ('site', 'status', 'publish_date', ),
            ('site', 'status', 'for_package', 'publish_date',),
            ('site', 'status', 'for_package', 'for_version', 'publish_date', ),
        )
        ordering = ('-publish_date', )

    @transaction.commit_on_success
    def take_by(self, user, took_date=None):
        dt = now().astimezone() if took_date is None else took_date
        try:
            card = self.cards.select_for_update().remaining()[0]
        except IndexError:
            raise EmptyRemainingGiftCard
        else:
            card.owner = user
            card.took_date = dt
            card.save()
            return card

    def has_took_by(self, user):
        return self.get_took_card_by(user).exists()

    def get_took_cards_by(self, user):
        return self.cards.filter(owner_id=user.pk)

    def __str__(self):
        return self.title

    def is_status_published(self):
        return self.status==CONTENT_STATUS_PUBLISHED


class GiftCardQuerySet(QuerySet):

    def remaining(self):
        table = self.model._meta.db_table
        return self.extra(where=['%s.owner_id IS NULL' % table])

    def has_took(self, giftbag, user):
        if isinstance(giftbag, int):
            giftbag_id = giftbag
        else:
            giftbag_id = giftbag.pk
        return self.filter(giftbag_id=giftbag_id, owner=user.pk).exists()

    def took_by(self, user):
        return self.filter(owner_id=user.pk)

    def took_from(self, giftbag):
        if isinstance(giftbag, int):
            giftbag_id = giftbag
        else:
            giftbag_id = giftbag.pk
        return self.filter(giftbag_id=giftbag_id)


class GiftCard(SiteRelated, models.Model):

    objects = GiftCardManager.for_queryset_class(GiftCardQuerySet)()

    giftbag = models.ForeignKey(GiftBag, related_name='cards')

    code = models.CharField(max_length=50, editable=False)

    owner = models.ForeignKey(user_model_name,
                              null=True,
                              blank=True,
                              on_delete=models.DO_NOTHING)

    took_date = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = '礼品码'
        verbose_name_plural = '礼品码'
        unique_together = (
            ('site', 'giftbag', 'code'),
        )
        index_together = (
            ('site', 'giftbag', 'owner'),
            ('site', 'giftbag', 'owner', 'took_date'),
            ('site', 'owner'),
        )

    def __str__(self):
        return "%s: %s" % (self.giftbag_id, self.code)


from import_export import resources, widgets, fields as ie_fields


class CodeWidget(widgets.CharWidget):

    def clean(self, value):
        if value:
            return value.strip()
        return value


class GiftCardResource(resources.ModelResource):

    giftbag = ie_fields.Field(column_name='giftbag',
                              attribute='giftbag_id',
                              widget=widgets.IntegerWidget())

    code = ie_fields.Field(column_name='code',
                           attribute='code',
                           widget=CodeWidget())

    class Meta:
        model = GiftCard
        fields = ('giftbag', 'code', )
        import_id_fields = ['giftbag', 'code']

    def get_instance(self, instance_loader, row):
        giftbag_field = self.fields['giftbag']
        code_field = self.fields['code']
        model = self._meta.model
        try:
            return model.objects.get(site_id=get_global_site().pk,
                                     giftbag_id=giftbag_field.clean(row),
                                     code=code_field.clean(row))
        except model.DoesNotExist:
            return None


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete


@receiver(pre_save, sender=GiftCard)
def giftcard_pre_save_took(sender, instance, **kwargs):
    if instance.pk and instance.tracker.has_changed('owner_id'):
        instance._owner_changed = True


@receiver(post_save, sender=GiftCard)
def giftcard_post_save_took(sender, instance, created, **kwargs):
    if getattr(instance, '_owner_changed', False):
        del instance._owner_changed
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.save()


@receiver(post_save, sender=GiftCard)
def giftcard_created(sender, instance, created, **kwargs):
    if created:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()


@receiver(post_delete, sender=GiftCard)
def giftcard_delete(sender, instance, **kwargs):
    try:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()
    except GiftBag.DoesNotExist:
        pass


from warehouse.tasks import sync_package


FLAG_GIFTBAG = '礼包'


def remove_giftbag_flag(giftbag):
    package = giftbag.for_package
    version = giftbag.for_version
    def _remove_tag(inst, tag):
        inst.tags_text = inst.tags_text.replace(tag, '').replace('  ', ' ')
        inst.save()
        return inst

    if version:
        _remove_tag(version, FLAG_GIFTBAG)

    version_flag = False
    for v in package.versions.published():
        if FLAG_GIFTBAG in v.tags_text:
            version_flag = True
            break
    if not version_flag:
        _remove_tag(package, FLAG_GIFTBAG)

    sync_package.apply_async((package.pk,), countdown=10)


def add_giftbag_flag(giftbag):
    version = giftbag.for_version
    package = giftbag.for_package
    version_changed = False
    if version and FLAG_GIFTBAG not in version.tags_text:
        version.tags_text = FLAG_GIFTBAG + " " + version.tags_text
        version.save()
        version_changed = True


    package_changed = False
    if FLAG_GIFTBAG not in package.tags_text:
        package.tags_text = FLAG_GIFTBAG + ' ' + package.tags_text
        package.save()
        package_changed = True

    if package_changed or (version_changed and package.latest_version_id == version.pk):
        sync_package.apply_async((package.pk,), countdown=10)


giftbag_sync_flag = '_sync_package_flag_type'


@receiver(pre_save, sender=GiftBag)
def change_giftbag_cards_count(sender, instance, **kwargs):
    if instance.tracker.has_changed('status') and instance.is_status_published():
        setattr(instance, giftbag_sync_flag, 'add')
        return

    if not instance.pk and instance.tracker.has_changed('status') and not instance.is_status_published():
        setattr(instance, giftbag_sync_flag, 'remove')
        return

    if not instance.is_status_published():
        return

    total_grow = False
    if instance.cards_total_count > instance.tracker.previous('cards_total_count'):
        total_grow = True

    if instance.tracker.previous('cards_total_count') == 0 and total_grow:
        setattr(instance, giftbag_sync_flag, 'add')
    elif instance.cards_remaining_count == 0:
        setattr(instance, giftbag_sync_flag, 'remove')


@receiver(post_save, sender=GiftBag)
def sync_giftbag_package_flag(sender, instance, **kwargs):
    sync_type = getattr(instance, giftbag_sync_flag, None)
    if sync_type == 'remove':
        remove_giftbag_flag(instance)
    elif sync_type == 'add':
        add_giftbag_flag(instance)


@receiver(post_delete, sender=GiftBag)
def delete_package_giftbag_flag(sender, instance, **kwargs):
    remove_giftbag_flag(instance)


from django.utils.timezone import utc
#from activity import documents as docs

#@receiver(post_save, sender=GiftBag)
"""
def giftbag_post_save_sync(sender, instance, created, **kwargs):
    defaults=dict(
        site_id=instance.site_id,
        title=instance.title,
        for_package_id=instance.for_package_id,
        for_version_id=instance.for_version_id,
        summary=instance.summary,
        usage_description=instance.usage_description,
        issue_description=instance.issue_description,
        publish_date=instance.publish_date.astimezone(utc),
        expirty_date=instance.expiry_date.astimezone(utc) if instance.expiry_date else None,
        cards_total_count=instance.cards_total_count,
        cards_remaining_count=instance.cards_remaining_count,
    )
    gb, created = docs.GiftBag.objects.get_or_create(id=instance.pk,
                                            defaults=defaults)
    if not created:
        for k,v in defaults.items():
            setattr(gb, k, v)
"""

from toolkit.managers import CurrentSiteManager


class Note(SiteRelated,
           models.Model):

    objects = CurrentSiteManager()

    all_objects = models.Manager()

    slug = models.SlugField(max_length=150)

    title = models.CharField(max_length=250)

    description = models.TextField()

    #rich_description = RichTextField()

    class Meta:
        verbose_name_plural = verbose_name = '说明'
        unique_together = (
            ('site', 'slug'),
        )


import os
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Ownable, MetaData
from mezzanine.core.fields import FileField
from easy_thumbnails.fields import ThumbnailerImageField

ACTIVITY_DIRECTORY_DTFORMAT = 'activity/%Y/%m/%d/%H%M-%S-%f'


def activity_profile_upload_to(instance, filename):
    activity_workspace_by_created(instance)
    basename = os.path.basename(filename)
    return "%s/%s" % (instance.workspace.name, basename)


def activity_workspace_by_created(instance):
    if not instance.workspace:
        if not instance.created:
            instance.created = now().astimezone()
        else:
            instance.created = instance.created.astimezone()
        sd = instance.created
        instance.workspace = sd.strftime(ACTIVITY_DIRECTORY_DTFORMAT)


class Activity(SiteRelated,
               MetaData,
               PublishDisplayable,
               TimeStamped,
               Ownable,
               models.Model):

    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=2000, null=True)

    cover = ThumbnailerImageField(
        default='',
        upload_to=activity_profile_upload_to,
        blank=True,
        max_length=500,
    )

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          help_text='!!切勿随意修改!!',
                          format='File')

    objects = ActivityManager()

    content = RichTextField()

    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
        unique_together = (
            ('site', 'slug',),
        )
        index_together = (
            ('site', 'status', ),
            ('site', 'status', 'publish_date', 'expiry_date'),
        )

    def get_absolute_url(self):
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        activity_workspace_by_created(self)
        return super(Activity, self).save(*args, **kwargs)

    def sync_status(self):
        return sync_status_from(self)


class Bulletin(SiteRelated,
               PublishDisplayable,
               TimeStamped,
               Ownable,
               models.Model):

    objects = BulletinManager()

    title = models.CharField(max_length=500)

    summary = models.CharField(max_length=500)

    content = RichTextField()

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        index_together = (
            ('site', 'status', ),
            ('site', 'status', 'publish_date', 'expiry_date'),
        )
        ordering = ('-publish_date', )

    def get_absolute_url(self):
        return None

    def __str__(self):
        return self.title
