# -*- encoding=utf-8 -*-
from os.path import basename
from django.db import models
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import FieldTracker, Choices
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager

class Place(models.Model):

    slug = models.CharField(verbose_name=_('slug'),
                            unique=True,
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

    def __str__(self):
        return self.slug

class AdvertisementQuerySet(QuerySet):

    def published(self):
        return self.filter(
            released_datetime__lte=now(), status=self.model.STATUS.published)

    def by_ordering(self):
        return self.order_by('relation_advertisement__ordering')

    def place_in(self, place):
        return self.filter(places=place)

def advertisement_upload_to(instance, filename):
    fbasename = basename(filename)
    fbname ,extension = fbasename.split('.')
    path = "%(prefix)s/%(date)s/%(ct)s-%(oid)d/%(fbname)s.%(extension)s/" % {
        'prefix': 'advertisement',
        'date': now().strftime("%Y%m%d"),
        'ct': instance.content_type.model,
        'oid': instance.object_id,
        'fbname': 'cover',
        'extension': extension
    }
    return path

class Advertisement(models.Model):

    objects = PassThroughManager.for_queryset_class(AdvertisementQuerySet)()

    cover = ThumbnailerImageField(
        verbose_name=_('advertisement cover'),
        upload_to=advertisement_upload_to,
    )

    title = models.CharField(verbose_name=_('title'),
                             max_length=36,
                             )

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, related_name='adv_content_type')
    content = generic.GenericForeignKey("content_type", "object_id")

    places = models.ManyToManyField(Place,
                                    symmetrical=False,
                                    through='Advertisement_Places',
                                    related_name='advertisements',
                                    blank=True,
                                    null=True,
                                    )

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

    def is_published(self):
        return self.status == self.STATUS.published \
            and self.released_datetime <= now()
    is_published.boolean = True
    is_published.short_description = _('released?')

    def __str__(self):
        return self.title

class Advertisement_Places(models.Model):

    place = models.ForeignKey(Place, related_name='relation_place')
    advertisement = models.ForeignKey(Advertisement, related_name='relation_advertisement')
    ordering = models.PositiveIntegerField(max_length=3, default=0,blank=True)

    class Meta:
        ordering = ('ordering', )
        unique_together = (
            ('place', 'advertisement', )
        )

from django.db.models.signals import pre_save
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

