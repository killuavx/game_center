# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django.db import models
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from toolkit.helpers import sync_status_from


class ClientPackageVersionQuerySet(QuerySet):

    def published(self):
        return self.filter(status=self.model.STATUS.published)\
            .filter(released_datetime__lte=now())

    def latest_version(self):
        return self.latest('version_code')


def factory_version_upload_to_path(basename):
    def upload_to(instance, filename):
        extension = filename.split('.')[-1].lower()
        path = "clientapp/v%d" % (int(instance.version_code))
        return '%(path)s/%(filename)s.%(extension)s' % {'path': path,
                                                        'filename': basename,
                                                        'extension': extension,
                                                        }
    return upload_to


class ClientPackageVersion(models.Model):

    class Meta:
        verbose_name = _('Client Package Version')
        verbose_name_plural = _('Client Package Versions')
        unique_together = (
            ('package_name', 'version_code',),
        )
        ordering = ('package_name', '-version_code', )

    objects = PassThroughManager\
        .for_queryset_class(ClientPackageVersionQuerySet)()

    icon = ThumbnailerImageField(
        upload_to=factory_version_upload_to_path('icon'),
        default='',
        blank=True,
    )

    cover = ThumbnailerImageField(
        upload_to=factory_version_upload_to_path('cover'),
        default='',
        blank=True,
    )

    package_name = models.CharField(
        verbose_name=_('package name'),
        blank=False,
        null=False,
        max_length=128)

    download = models.FileField(
        verbose_name=_('version file'),
        upload_to=factory_version_upload_to_path('application'),
        default='',
        blank=True
    )

    download_size = models.PositiveIntegerField(
        verbose_name=_('app file byte size'),
        default=0,
        blank=True,
        editable=False,
    )

    download_count = models.PositiveIntegerField(
        verbose_name=_('package version download count'),
        max_length=9,
        default=0,
        blank=True
    )

    version_name = models.CharField(
        verbose_name=_('version name'),
        max_length=16,
        blank=False,
        null=False
    )

    version_code = models.IntegerField(
        verbose_name=_('version code'),
        max_length=8,
        blank=False,
        null=False
    )

    summary = models.CharField(
        verbose_name=_('summary'),
        max_length=255,
        default="",
        blank=True,
        null=False
    )

    memorandum = models.TextField(
        verbose_name=_("version memorandum by developer or operator"),
        default='',
        blank=True,
    )

    whatsnew = models.TextField(
        verbose_name=_("what's new"),
        default="",
        blank=True)

    STATUS = Choices(
        'draft',
        'unpublished',
        'rejected',
        'published',
    )

    status = StatusField(default='draft', blank=True)

    released_datetime = models.DateTimeField(
        verbose_name=_('released time'),
        db_index=True,
        blank=True,
        null=True)

    created_datetime = models.DateTimeField(
        verbose_name=_('created time'),
        auto_now_add=True)

    updated_datetime = models.DateTimeField(
        verbose_name=_('updated time'),
        auto_now_add=True)

    tracker = FieldTracker()

    def sync_status(self):
        return sync_status_from(self)

    def __str__(self):
        return "%s:%s" %(self.package_name, self.version_code)


from django.db.models.signals import pre_save
from django.dispatch import receiver
from os.path import getsize

@receiver(pre_save, sender=ClientPackageVersion)
def client_packageversion_pre_save(sender, instance, **kwargs):

    if instance.tracker.has_changed('download') and instance.download:
        try:
            file_size = instance.download.file.size
        except:
            file_name = instance.download.name
            file_size = getsize(file_name)
        instance.download_size = file_size

@receiver(pre_save, sender=ClientPackageVersion)
def updated_datetime_pre_save_with_tracker(sender, instance, **kwargs):
    """same with DatetimeField(auto_now=True),
    but open for package_version_post_save signals,
    because model datetime with auto_now=True would be overwrite on save action
    """
    changed = instance.tracker.changed()
    try:
        changed.pop('updated_datetime')
    except KeyError:
        pass

    if len(changed):
        instance.updated_datetime = now()
