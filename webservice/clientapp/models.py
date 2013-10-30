# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django.db import models
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


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

    released_datetime = models.DateTimeField(db_index=True, blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True, auto_now_add=True)

    tracker = FieldTracker()


from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=ClientPackageVersion)
def client_packageversion_pre_save(sender, instance, *args, **kwargs):

    if instance.tracker.has_changed('download') and instance.download:
       instance.download_size = instance.download.size
