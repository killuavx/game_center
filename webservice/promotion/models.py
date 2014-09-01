# -*- encoding=utf-8 -*-
from os.path import basename, dirname
from django.db import models
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import FieldTracker, Choices
from model_utils.fields import StatusField
from toolkit.fields import MultiResourceField
from toolkit.managers import CurrentSitePassThroughManager
from toolkit.helpers import sync_status_from, released_hourly_datetime
from toolkit import model_url_mixin as urlmixin
from toolkit.models import SiteRelated
from toolkit.storage import image_storage
from toolkit.fields import QiniuThumbnailerImageField
from django.core import exceptions
from copy import deepcopy

from mezzanine.core.fields import FileField


class Place(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager()

    slug = models.CharField(verbose_name=_('slug'),
                            max_length=32,
                            help_text='唯一定位一个位置的名称，'
                                      '命名使用英文字母、数字和"-"组合',
    )

    help_text = models.CharField(verbose_name=_('help text'),
                                 max_length=50,
                                 default='',
                                 blank=True,
                                 help_text='提示位置使用方式',
    )

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')
        unique_together = (
            ('site', 'slug',),
        )

    def __str__(self):
        return self.slug


class AdvertisementQuerySet(QuerySet):

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(
            released_datetime__lte=dt, status=self.model.STATUS.published)

    def by_ordering(self):
        return self.order_by('relation_advertisement__ordering')

    def place_in(self, place):
        return self.filter(places=place)


def advertisement_workspace_path(instance, dt):
    path = None
    if instance.content:
        path = '%s-%s' %(instance.content_type.model, instance.object_id)
    if not instance.workspace:
        d = dt.astimezone().strftime('%H%M')
        if path is None:
            path = dt.astimezone().strftime('%H%M')
        instance.workspace = "%(prefix)s/%(date)s/%(path)s" % {
            'prefix': 'advertisement', 'date': d, 'path': path
        }
    return instance


def advertisement_upload_to(instance, filename):
    fbasename = basename(filename)
    advertisement_workspace_path(instance, now())
    return "%s/%s" %(instance.workspace.name, fbasename.lower())


class Advertisement(urlmixin.AdvertisementAbsoluteUrlMixin,
                    SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager\
        .for_queryset_class(AdvertisementQuerySet)()

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          format='File')

    cover = ThumbnailerImageField(
        verbose_name=_('advertisement cover'),
        upload_to=advertisement_upload_to,
    )

    title = models.CharField(verbose_name=_('title'),
                             max_length=36,
    )

    object_id = models.PositiveIntegerField(default=0, blank=True)
    content_type = models.ForeignKey(ContentType,
                                     related_name='adv_content_type',
                                     default=None,
                                     blank=True,
                                     null=True,
                                     )
    link = models.URLField(max_length=1024, default='', blank=True)

    TARGET = Choices(
        ('_self', 'default', '本窗口'),
        ('_blank', 'blank', '新开窗口'),
    )

    target = models.CharField(max_length=10,
                              choices=TARGET,
                              default=TARGET.default)

    content = generic.GenericForeignKey("content_type", "object_id")

    places = models.ManyToManyField(Place,
                                    symmetrical=False,
                                    through='Advertisement_Places',
                                    related_name='advertisements',
                                    blank=True,
                                    null=True,
    )

    resources = MultiResourceField()

    STATUS = Choices(
        ('draft', _('Draft')),
        ('unpublished', _('Unpublished')),
        ('published', _('Published')),
    )

    status = StatusField(default=STATUS.draft, blank=True)

    released_datetime = models.DateTimeField(blank=True,
                                             null=True,
                                             db_index=True)

    updated_datetime = models.DateTimeField(db_index=True,
                                            editable=False)

    created_datetime = models.DateTimeField(editable=False)

    tracker = FieldTracker()

    class Meta:
        verbose_name = _('advertisement')
        verbose_name_plural = _('advertisements')

    def is_published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.status == self.STATUS.published \
            and self.released_datetime <= dt

    is_published.boolean = True
    is_published.short_description = _('released?')

    def clean(self):
        from toolkit.helpers import get_global_site
        site = get_global_site()
        if self.link.startswith('/') and site:
            self.link = "http://%s%s" % (site.domain, self.link)

        if not self.content and not self.link:
            raise exceptions.ValidationError('content/link 必须二选一')

        if self.content and self.link:
            raise exceptions\
                .ValidationError('content/link 必须二选一: %s, %s' %(self.content, self.link))

    def __str__(self):
        return self.title

    def sync_status(self):
        return sync_status_from(self)


class Advertisement_Places(models.Model):

    place = models.ForeignKey(Place, related_name='relation_place')

    advertisement = models.ForeignKey(Advertisement,
                                      related_name='relation_advertisement')
    ordering = models.PositiveIntegerField(max_length=3, default=0, blank=True)

    updated_datetime = models.DateTimeField(auto_now=True, default=now)

    created_datetime = models.DateTimeField(auto_now_add=True, default=now)

    class Meta:
        ordering = ('place', '-ordering', )
        index_together = (
            ('place', 'ordering', ),
        )
        unique_together = (
            ('place', 'advertisement', ),
        )


from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(pre_save, sender=Advertisement)
def advertisement_pre_save(sender, instance, **kwargs):
    """same with DatetimeField(auto_now=True),
    but model datetime changed by custom with auto_now=True would be overwrite on save action
    """
    changed = instance.tracker.changed()
    try:
        changed.pop('updated_datetime')
    except KeyError:
        pass

    if len(changed) \
        and not instance.tracker.has_changed('updated_datetime'):
        instance.updated_datetime = now()

    if not instance.created_datetime:
        instance.created_datetime = now()

    if instance.tracker.has_changed('status') \
        and instance.status == sender.STATUS.published \
        and not instance.released_datetime:
        instance.released_datetime = now()

    advertisement_workspace_path(instance, now())


from dateutil import rrule
from datetime import timedelta
from django.db.models.query import Q


class RecommendQuerySet(AdvertisementQuerySet):

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(status=self.model.STATUS.published)\
            .filter(Q(released_datetime__lte=dt))\
            .filter(Q(expiry_datetime__gt=dt) | Q(expiry_datetime=None))


RECOMMEND_DIRECTORY_DTFORMAT = 'recommend/%Y/%m/%d/%H%M-%S-%f'


def recommend_workspace_path(instance, dt):
    if not instance.workspace:
        instance.workspace = dt.astimezone().strftime(RECOMMEND_DIRECTORY_DTFORMAT)
    return instance


def recommend_upload_to(instance, filename):
    fbasename = basename(filename)
    if not instance.created_datetime:
        instance.created_datetime = now().astimezone()
    recommend_workspace_path(instance, instance.created_datetime)
    return "%s/%s" %(instance.workspace.name, fbasename.lower())


class Recommend(urlmixin.RecommendAbsoluteUrlMixin,
                SiteRelated, models.Model):
    """
    小编推荐
    """

    class Meta:
        index_together = (
            ('site', 'content_type', 'object_id', ),
            ('site', 'status', ),
            ('site', 'released_datetime', 'expiry_datetime', ),
            ('site', 'status', 'released_datetime', 'expiry_datetime', ),
        )

    objects = CurrentSitePassThroughManager \
        .for_queryset_class(RecommendQuerySet)()

    title = models.CharField(verbose_name=_('title'), max_length=36, )

    summary = models.CharField(max_length=250)

    cover = QiniuThumbnailerImageField(
        storage=image_storage,
        thumbnail_storage=image_storage,
        upload_to=recommend_upload_to,
    )

    content = generic.GenericForeignKey("content_type", "object_id")
    object_id = models.PositiveIntegerField(default=0, blank=True)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to=dict(app_label='warehouse',
                                                           model__in=['package', 'packageversion']),
                                     blank=True,
                                     null=True)

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          format='File')

    resources = MultiResourceField()

    STATUS = Choices(
        ('draft', _('Draft')),
        ('unpublished', _('Unpublished')),
        ('published', _('Published')),
    )

    status = StatusField(default=STATUS.draft, blank=True)

    weekday_numbers = models.CharField(max_length=15,
                                       default='0',
                                       help_text='一周推荐星期序号, 可多选, monday:0 ... sunday:6, 格式以空格分割'
    )

    released_datetime = models.DateTimeField(db_index=True)

    updated_datetime = models.DateTimeField(db_index=True, editable=False)

    created_datetime = models.DateTimeField(auto_now_add=now, editable=False)

    expiry_datetime = models.DateTimeField(_("Expires on"),
                                           help_text=_("With Published chosen, won't be shown after this time"),
                                           blank=True, null=True)

    tracker = FieldTracker()

    def is_published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.status == self.STATUS.published \
            and self.released_datetime <= dt \
            and self.expiry_datetime > dt
    is_published.boolean = True
    is_published.short_description = _('is published?')

    def allow_show(self, dt, released_hourly=True):
        dt = released_hourly_datetime(dt, released_hourly)
        return dt.weekday() in [w.weekday for w in self.weekdays]

    def can_show_today(self):
        return self.allow_show(now().astimezone())
    can_show_today.boolean = True

    def allow_show_dates(self, max_count=None):
        expiry_datetime = self.expiry_datetime
        if not self.expiry_datetime:
            expiry_datetime = self.released_datetime + timedelta(days=7)

        return rrule.rrule(rrule.WEEKLY,
                           count=max_count,
                           byweekday=self.weekdays,
                           wkst=rrule.SU,
                           dtstart=self.released_datetime,
                           until=expiry_datetime)

    @property
    def weekdays(self):
        return [rrule.weekdays[int(wd)] for wd in self.weekday_numbers.split(' ')]

    def clean(self):
        self.updated_datetime = now()
        self.weekday_numbers = self.weekday_numbers.strip()
        try:
            weekdays = self.weekdays
        except TypeError:
            e = exceptions.ValidationError(dict(
                weekdays='weekdays must in %s' % (
                    {_wd.weekday: repr(_wd) for _wd in rrule.weekdays}
                )))

    @property
    def icon(self):
        obj = self.content
        if not obj:
            return None
        else:
            # for PackageVersion
            if hasattr(obj, 'icon'):
                return obj.icon

            # for Package
            elif getattr(obj, 'latest_version', None):
                return obj.latest_version.icon
        return None

    def save(self, update_site=False, *args, **kwargs):
        if not self.updated_datetime:
            self.updated_datetime = self.created_datetime
        return super(Recommend, self).save(update_site=update_site, *args, **kwargs)

    def sync_status(self):
        return sync_status_from(self)

    def __str__(self):
        return self.title
