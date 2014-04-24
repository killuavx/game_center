# -*- encoding=utf-8 -*-
import datetime
from os.path import basename
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from django.conf import settings
from django.core import exceptions
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from toolkit.fields import StarsField
from django.utils.translation import ugettext_lazy as _
import tagging
from tagging_autocomplete.models import TagAutocompleteField as TagField
from easy_thumbnails.fields import ThumbnailerImageField

from toolkit.models import SiteRelated, CurrentSitePassThroughManager
from toolkit.helpers import import_from, sync_status_from


class AuthorQuerySet(QuerySet):

    def have_package(self, package):
        return self.filter(packages__in=package)

    def by_name_order(self, order=None):
        field = 'name'
        if order is None:
            return self
        elif order is True:
            return self.order_by('-' + field)
        else:
            return self.order_by('+' + field)

    def activated(self):
        return self.filter(status=self.model.STATUS.activated)

    def published(self):
        return self.activated()

    def unactivated(self):
        return self.exclude(status=self.model.STATUS.activated)

    def unpublished(self):
        return self.unactivated()


def factory_author_upload_to(basename):
    def upload_to(instance, filename):
        extension = filename.split('.')[-1].lower()
        dt_path = now().strftime("%Y%m%d%H%M/%S-%f")
        path = "author/%s" % dt_path
        return '%(path)s/%(filename)s.%(extension)s' % {'path': path,
                                                        'filename': basename,
                                                        'extension': extension,
        }

    return upload_to


class Author(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager.for_queryset_class(AuthorQuerySet)()


    icon = ThumbnailerImageField(upload_to=factory_author_upload_to('icon'),
                                 blank=True,
                                 default='')

    cover = ThumbnailerImageField(upload_to=factory_author_upload_to('cover'),
                                  blank=True,
                                  default='')

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        unique_together = (
            ('site', 'name',),
        )

    name = models.CharField(verbose_name=_('author name'),
                            max_length=64)

    email = models.EmailField(verbose_name=_('email'),
                              unique=True)

    phone = models.CharField(verbose_name=_('phone'),
                             max_length=16,
                             blank=True,
                             null=True)

    # home_page = models.URLField(blank=True,null=True)

    topics = generic.GenericRelation('taxonomy.TopicalItem')

    STATUS = Choices(
        ('draft', 'draft', _('Draft')),
        ('unactivated', 'unactivated', _('Unactivated')),
        ('activated', 'activated', _('Activated')),
        ('rejected', 'rejected', _('Rejected'))
    )

    status = StatusField(verbose_name=_('status'))

    def __str__(self):
        return str(self.name)

    __unicode__ = __str__

    def get_absolute_url(self):
        return '/authors/%s' % self.pk


class PackageQuerySet(QuerySet):

    def by_category(self, category):
        return self.filter(categories__contains=category)

    def by_author(self, author):
        return self.filter(author=author)

    def by_published_order(self, newest=None):
        qs = self.published()
        field = 'released_datetime'
        if newest is None:
            return qs
        elif newest is True:
            return qs.order_by('-' + field)
        else:
            return qs.order_by('+' + field)

    def by_rankings_order(self):
        return self.order_by('-download_count')

    def by_updated_order(self):
        return self.order_by('-updated_datetime')

    def published(self):
        return self.filter(
            released_datetime__lte=now(), status=self.model.STATUS.published)

    def unpublished(self):
        return self.filter(released_datetime__gt=now()) \
            .exclude(status=self.model.STATUS.published)


class Package(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager.for_queryset_class(PackageQuerySet)()

    class Meta:
        permissions = (
            ('can_deliver_package', _('Can deliver package')),
            ('can_remove_package', _('Can remove package')),
            ('can_change_package', _('Can change package')),
        )
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")
        unique_together = (
            ('site', 'package_name',)
        )

    title = models.CharField(
        verbose_name=_('package title'),
        max_length=128)

    package_name = models.CharField(
        verbose_name=_('package name'),
        db_index=True,
        max_length=128)

    summary = models.CharField(
        verbose_name=_('summary'),
        max_length=255,
        null=False,
        default="",
        blank=True)

    description = models.TextField(
        verbose_name=_('description'),
        null=False,
        default="",
        blank=True)

    author = models.ForeignKey(Author, related_name='packages')


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
        db_index=True,
        auto_now_add=True)

    categories = models.ManyToManyField(
        'taxonomy.Category',
        verbose_name=_('categories'),
        related_name='packages',
        blank=True)

    tags_text = TagField(
        verbose_name=_('tags'),
        default="",
        blank=True)

    topics = generic.GenericRelation('taxonomy.TopicalItem')

    download_count = models.PositiveIntegerField(
        verbose_name=_('package download count'),
        max_length=9,
        db_index=True,
        default=0,
        blank=True
    )

    STATUS = Choices(
        ('draft', 'draft', _('Draft')),
        ('published', 'published', _('Published')),
        ('unpublished', 'unpublished', _('Unpublished')),
        ('rejected', 'rejected', _('Rejected')),
    )

    status = StatusField(verbose_name=_('status'))


    def was_published_recently(self):
        if self.released_datetime:
            return self.released_datetime >= now() - datetime.timedelta(days=1)
        else:
            return False

    was_published_recently.admin_order_field = 'released_datetime'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('Released recently?')

    tracker = FieldTracker()

    def is_published(self):
        return self.status == self.STATUS.published \
            and self.released_datetime <= now()

    @property
    def main_category(self):
        try:
            return self.categories.all()[0]
        except (exceptions.ObjectDoesNotExist, IndexError):
            return None

    def clean(self):
        if self.status == self.STATUS.published:
            latest_version = None
            try:
                latest_version = self.versions.latest_published()
            except exceptions.ObjectDoesNotExist:
                pass

            if not latest_version:
                raise exceptions.ValidationError(
                    _('No published version can enough to publish package,'
                      'or you can change package status to Unpublished.'
                    )
                )
        super(Package, self).clean()

    def __str__(self):
        return self.title

    __unicode__ = __str__

    def __init__(self, *args, **kwargs):
        super(Package, self).__init__(*args, **kwargs)

    def get_absolute_url(self, link_type=0):
        if link_type == 0:
            return '/packages/%s/' % self.package_name
        else:
            return '/packages/%s/' % self.pk


tagging.register(Package)


class PackageVersionQuerySet(QuerySet):

    def by_updated_order(self):
        return self.order_by('-updated_datetime')

    def by_published_order(self, newest=None):
        field = 'released_datetime'
        qs = self.published()
        if newest is None:
            return qs
        elif newest is True:
            return qs.order_by('-' + field)
        else:
            return qs.order_by('+' + field)

    def by_rankings_order(self):
        return self.order_by('-download_count')

    def published(self):
        return self.filter(
            released_datetime__lte=now(), status=self.model.STATUS.published)

    def unpublished(self):
        return self.filter(released_datetime__gt=now()) \
            .exclude(status=self.model.STATUS.published)

    def latest_version(self):
        return self.latest('version_code')

    def latest_published(self):
        return self.published().latest('version_code')


def factory_version_upload_to_path(basename):
    def upload_to(instance, filename):
        extension = filename.split('.')[-1].lower()
        path = "package/%d/v%d" % (
            int(instance.package.pk), int(instance.version_code))
        return '%(path)s/%(filename)s.%(extension)s' % {'path': path,
                                                        'filename': basename,
                                                        'extension': extension,
        }

    return upload_to


class PackageVersion(SiteRelated, models.Model):

    objects =  CurrentSitePassThroughManager\
        .for_queryset_class(PackageVersionQuerySet)()

    class Meta:
        verbose_name = _("Package Version")
        verbose_name_plural = _("Package Versions")
        unique_together = (
            ('site', 'package', 'version_code'),
        )


    icon = ThumbnailerImageField(
        default='',
        upload_to=factory_version_upload_to_path('icon'),
        blank=True,
    )

    cover = ThumbnailerImageField(
        default='',
        upload_to=factory_version_upload_to_path('cover'),
        blank=True,
    )

    download = models.FileField(
        verbose_name=_('version file'),
        upload_to=factory_version_upload_to_path('application'),
        default='',
        blank=True)

    di_download = models.FileField(
        verbose_name=_('version file with data integration'),
        upload_to=factory_version_upload_to_path('application-di'),
        default='',
        blank=True
    )

    download_count = models.PositiveIntegerField(
        verbose_name=_('package version download count'),
        max_length=9,
        default=0,
        blank=True
    )

    package = models.ForeignKey(Package, related_name='versions')

    version_name = models.CharField(
        verbose_name=_('version name'),
        max_length=16,
        blank=False,
        null=False)

    version_code = models.IntegerField(
        verbose_name=_('version code'),
        max_length=8,
        blank=False,
        null=False)

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
    #inspection_report = models.TextField(default='', blank=True)
    #report = models.OneToOneField('PackageVersionReport',
    #                              on_delete=True)

    status = StatusField(default='draft', blank=True)

    released_datetime = models.DateTimeField(db_index=True, blank=True,
                                             null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True, auto_now_add=True)

    stars = StarsField(verbose_name=_('Star'))

    tracker = FieldTracker()

    def get_absolute_url(self, link_type=0):
        if link_type == 0:
            return '/packages/%s/%s' %(self.package.package_name, self.version_name)
        else:
            return '/packageversions/%s' % self.pk

    def __str__(self):
        return str(self.version_code)

    def __hash__(self):
        return int(self.version_code)

    __unicode__ = __str__

    DOWNLOAD_FILETYPE_PK = 0
    DOWNLOAD_FILETYPE_DI = 1
    DOWNLOAD_FILETYPES = {
        'di': DOWNLOAD_FILETYPE_DI,
        'pk': DOWNLOAD_FILETYPE_PK,
    }

    DOWNLOAD_FILETYPES = {
        'di': DOWNLOAD_FILETYPE_DI,
        'pk': DOWNLOAD_FILETYPE_PK,
    }

    DOWNLOAD_FILELOCATION_FS = 0
    DOWNLOAD_FILELOCATION_CDN = 1
    DOWNLOAD_FILELCOATIONS = {
        'cdn': DOWNLOAD_FILELOCATION_CDN,
        'fs': DOWNLOAD_FILELOCATION_FS,
    }

    def get_download(self, filetype=None):
        if filetype is None:
            return self.di_download if self.di_download else self.download
        else:
            if filetype == self.DOWNLOAD_FILETYPE_DI:
                return self.di_download
            else:
                return self.download

    def get_download_size(self, filetype=None):
        download = self.get_download(filetype=filetype)
        try:
            return download.size
        except:
            return 0

    def get_download_url(self, filetype=None, is_dynamic=True, **kwargs):
        kwargs.setdefault('entrytype', 'web')
        if is_dynamic:
            url = self.get_download_dynamic_url(filetype=filetype)
        else:
            url = self.get_download_static_url(filetype=filetype)

        if kwargs:
            part = list(urlparse(url))
            query_idx = 4
            query_params = list(parse_qsl(part[query_idx])) + list(kwargs.items())
            part[query_idx] = urlencode(query_params)
            url = urlunparse(part)
        return url

    def get_download_static_url(self, filetype=None):
        return self.get_download(filetype=filetype).url

    def get_download_dynamic_url(self, filetype=None):
        kwargs = dict(pk=self.pk)
        if filetype:
            kwargs['filetype'] = filetype
        return reverse('download_packageversion', kwargs=kwargs)

    def sync_status(self):
        return sync_status_from(self)


def screenshot_upload_to_path(instance, filename):
    filebasename = basename(filename).lower()
    version = instance.version
    return "package/%(pkg_id)d/v%(version_code)d/screenshot/%(basename)s" % {
        'pkg_id': version.package_id,
        'version_code': version.version_code,
        'basename': filebasename
    }


class PackageVersionScreenshot(models.Model):

    version = models.ForeignKey(PackageVersion, related_name='screenshots')

    image = ThumbnailerImageField(
        upload_to=screenshot_upload_to_path,
        blank=False
    )

    alt = models.CharField(
        _('image alt'),
        max_length=30,
        blank=True)

    ROTATE = (
        ( '-180', '-180'),
        ( '-90', '-90'),
        ( '0', '0'),
        ( '90', '90'),
        ( '180', '180'),
    )

    rotate = models.CharField(
        verbose_name=_('image rotate'),
        max_length=4,
        default=0,
        choices=ROTATE)

    def delete(self, using=None):
        self.image.delete(save=False)
        super(PackageVersionScreenshot, self).delete(using=using)

    def __str__(self):
        try:
            return self.image.url
        except:
            return self.alt


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


#@receiver(pre_save, sender=PackageVersion)
def package_version_pre_save(sender, instance, **kwargs):
    try:
        parser_opts = getattr(settings, 'PACKAGE_FILE_PARSE_OPTS', dict())
        parser_class = import_from(
            parser_opts.get('package_version_parser_class',
                            'warehouse.utils.parser.PackageFileParser'))
        parse_handle_class = import_from(
            parser_opts.get('package_version_parse_handle_class',
                            'warehouse.utils.parse_handle.ParsePackageVersion'))
    except:
        parser_class = None
        parse_handle_class = None
        pass

    if instance.download and parser_class and parse_handle_class:
        parser = parser_class(instance.download.file.file.name)
        handle = parse_handle_class(instance, parser)

        if handle.can_parse_appfile():
            try:
                package = instance.package
            except:
                package = handle.parse_to_package()
                package.save()
                instance.package_id = package.pk

            handle.parse_to_version()

            # no icon on new create
            if not instance.icon and not instance.pk:
                handle.fetch_icon_to_version()
            #  change icon manually
            elif instance.tracker.has_changed('icon'):
                return


@receiver(post_save, sender=PackageVersion)
def package_version_post_save(sender, instance, **kwargs):
    """package sync ...
        1. updated_datetime when self version published and changed
        2. download_count when self version download_count changed
    """
    package = instance.package
    if instance.status == instance.STATUS.published \
        and instance.tracker.changed():
        package.updated_datetime = instance.updated_datetime

    if instance.status == instance.STATUS.published \
        and instance.tracker.has_changed('download_count'):
        aggregate = package.versions \
            .filter(status=instance.STATUS.published) \
            .aggregate(download_count=models.Sum('download_count'))
        package.download_count = aggregate.get('download_count', 0)

    if package.tracker.changed():
        package.save()
        pass

# fix for PackageVersion save to update Package(set auto_now=False) updated_datetime
@receiver(pre_save, sender=Package)
def package_pre_save(sender, instance, **kwargs):
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



