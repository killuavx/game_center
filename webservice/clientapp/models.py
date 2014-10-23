# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.db import models
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from toolkit.helpers import sync_status_from, released_hourly_datetime, qurl_to
from toolkit.managers import CurrentSitePassThroughManager, PublishedManager
from toolkit.models import SiteRelated, PublishDisplayable
from mezzanine.core.models import TimeStamped, Orderable
from toolkit.fields import MultiResourceField
from mezzanine.core.fields import FileField
import os


class ClientPackageVersionQuerySet(QuerySet):

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(status=self.model.STATUS.published)\
            .filter(released_datetime__lte=dt)

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


CLIENT_PACKAGEVERSION_DIRECTORY_PREFIX  = 'clientapp'

CLIENT_PACKAGEVERSION_DIRECTORY_DTFORMAT = "%s/%s" %(CLIENT_PACKAGEVERSION_DIRECTORY_PREFIX,
                                                     '%Y/%m/%d/%H%M-%S-%f')


def clientpackageversion_upload_to(instance, filename):
    clientpackageversion_workspace_by_created(instance)
    basename = os.path.basename(filename)
    return "%s/%s" % (instance.workspace.name, basename)


def clientpackageversion_workspace_by_created(instance):
    if not instance.workspace:
        if not instance.created_datetime:
            instance.created_datetime = now().astimezone()
        sd = instance.created_datetime.astimezone()
        instance.workspace = sd.strftime(CLIENT_PACKAGEVERSION_DIRECTORY_DTFORMAT)


class ClientPackageVersion(SiteRelated, models.Model):

    class Meta:
        verbose_name = _('Client Package Version')
        verbose_name_plural = _('Client Package Versions')
        unique_together = (
            ('site', 'package_name', 'version_code',),
        )
        ordering = ('package_name', '-version_code', )

    objects = CurrentSitePassThroughManager\
        .for_queryset_class(ClientPackageVersionQuerySet)()

    icon = ThumbnailerImageField(
        upload_to=clientpackageversion_upload_to,
        default='',
        blank=True,
    )

    cover = ThumbnailerImageField(
        upload_to=clientpackageversion_upload_to,
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
        upload_to=clientpackageversion_upload_to,
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

    resources = MultiResourceField()

    workspace = FileField(default='',
                          blank=True,
                          max_length=500)

    def sync_status(self):
        return sync_status_from(self)

    def __str__(self):
        return "%s:%s" %(self.package_name, self.version_name)


def client_download_url(package_name, **kwargs):
    client_dw_url = reverse('clientapp-latest_download',
                            kwargs=dict(package_name=package_name))
    return qurl_to(client_dw_url, **kwargs)


from django.db.models.signals import pre_save
from django.dispatch import receiver
from os.path import getsize
from django.conf import settings

@receiver(pre_save, sender=ClientPackageVersion)
def client_packageversion_pre_save(sender, instance, **kwargs):
    clientpackageversion_workspace_by_created(instance)
    try:
        path = os.path.join(settings.MEDIA_ROOT, str(instance.workspace))
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    except:
        pass
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


class LoadingCoverQuerySet(QuerySet):

    def find_covers(self, package_name, version_name=None, **kwargs):
        if version_name is None:
            return self.filter(package_name=package_name)
        else:
            return self.filter(version__package_name=package_name,
                               version__version_name=version_name)


class LoadingCoverManager(PublishedManager, CurrentSitePassThroughManager):
    pass


def _clientloading_upload_to_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    path = "clientloading/%s" % instance.package_name
    basename = instance.created.strftime('%Y%m%d-%H%M%S')
    return '%(path)s/%(filename)s.%(extension)s' % {'path': path,
                                                    'filename': basename,
                                                    'extension': extension,
                                                    }


class LoadingCover(SiteRelated,
                   PublishDisplayable,
                   Orderable,
                   TimeStamped):

    objects = LoadingCoverManager.for_queryset_class(LoadingCoverQuerySet)()

    title = models.CharField(max_length=200)

    package_name = models.CharField(max_length=200, blank=True)

    version = models.ForeignKey(ClientPackageVersion,
                                default=None,
                                null=True,
                                blank=True)

    image = models.ImageField(upload_to=_clientloading_upload_to_path)

    def clean(self):
        if not self.package_name and not self.version:
            raise ValidationError('package_name or version cannot be empty')

        if self.version and not self.package_name:
            self.package_name = self.version.package_name

        if not self.created:
            self.created = now()

        self.in_sitemap = False

    class Meta:
        verbose_name = '封面'
        verbose_name_plural = '封面图片'
        index_together = (
            ('site', '_order'),
            ('site', 'status'),
            ('site', 'status', '_order'),
        )
        ordering = ('site', '_order')

    def sync_status(self):
        return sync_status_from(self)
