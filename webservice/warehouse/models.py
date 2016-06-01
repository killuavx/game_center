# -*- encoding=utf-8 -*-
import datetime
from os.path import join, splitext
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core import validators
from django.conf import settings
from django.core import exceptions
from django.core.urlresolvers import reverse, get_callable
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from django.utils.translation import ugettext_lazy as _
import tagging
from toolkit.fields import TagField
#from easy_thumbnails.fields import ThumbnailerImageField
from toolkit.fields import QiniuThumbnailerImageField

from toolkit.managers import CurrentSitePassThroughManager, PassThroughManager
from toolkit.fields import StarsField, PkgFileField, MultiResourceField
from toolkit.models import SiteRelated
from toolkit import model_url_mixin as urlmixin, cache_tagging_mixin as cachemixin
from toolkit.helpers import import_from, sync_status_from, released_hourly_datetime, qurl_to
from toolkit.storage import package_storage, image_storage, screenshot_thumbnail_storage

storage = package_storage

slugify_function_path = getattr(settings, 'SLUGFIELD_SLUGIFY_FUNCTION',
                                'toolkit.helpers.slugify_unicode')
slugify = get_callable(slugify_function_path)
from mezzanine.core.fields import FileField
from comment.fields import CommentsField


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


def author_workspace_path(author):
    _id = author.pk
    subdir = 'author'
    try:
        if hasattr(author, 'track_id'):
            _id = author.artist_id
        else:
            iauthor = author.iosauthor
            _id = iauthor.artist_id
        subdir = 'iauthor'
    except ObjectDoesNotExist:
        dt_path = now().strftime("%Y%m%d%H%M/%S-%f")
        subdir = "author/%s" % dt_path
        _id = ''
    return join(subdir, str(_id)).rstrip('/')


def factory_author_upload_to(basename):

    def upload_to(instance, filename):
        extension =  splitext(filename)[1].lstrip('.')
        if not instance.workspace:
            instance.workspace = author_workspace_path(instance)
        relative_path = instance.workspace
        return "%s/%s.%s" % (relative_path, basename, extension)

    return upload_to


class PlatformBase(object):

    _is_base = True

    PLATFORM_BASE = 'base'

    PLATFORM_IOS = 'ios'

    PLATFORM_ANDROID = 'android'

    _platform = PLATFORM_BASE

    @property
    def platform(self):
        return self._platform

    @property
    def is_base(self):
        return self._is_base

    @property
    def is_ios_model(self):
        if self.is_base:
            return False

        if self.platform == self.PLATFORM_IOS:
            return True

        return False

    @property
    def is_ios(self):
        if self.is_ios_model:
            return True
        try:
            name = self._meta.module_name
            attr = getattr(self, 'ios%s' % name)
        except (AttributeError, ObjectDoesNotExist) as e:
            return False
        else:
            return True

    @property
    def as_ios(self):
        if self.is_ios_model:
            return self

        if self.is_ios:
            name = self._meta.module_name
            if name.startswith('ios'):
                return self
            else:
                return getattr(self, 'ios%s' % name)
        return None

    @property
    def is_android(self):
        return not self.is_ios

    @property
    def is_android_model(self):
        if self.is_base:
            return True
        return False

    @property
    def as_android(self):
        return self.as_base

    @property
    def as_base(self):
        if self.is_ios_model:
            name = self._meta.module_name
            name = name.lstrip('ios')
            ptr = '%s_ptr' % name
            return getattr(self.as_ios, ptr)
        else:
            return self


class Author(urlmixin.AuthorAbsoluteUrlMixin,
             PlatformBase, SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager\
        .for_queryset_class(AuthorQuerySet)()

    all_objects = PassThroughManager.for_queryset_class(AuthorQuerySet)()


    icon = QiniuThumbnailerImageField(upload_to=factory_author_upload_to('icon'),
                                 blank=True,
                                 thumbnail_storage=image_storage,
                                 storage=image_storage,
                                 default='')

    cover = QiniuThumbnailerImageField(upload_to=factory_author_upload_to('cover'),
                                  blank=True,
                                  thumbnail_storage=image_storage,
                                  storage=image_storage,
                                  default='')

    resources = MultiResourceField()

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        unique_together = (
            ('site', 'name',),
        )

    name = models.CharField(verbose_name=_('author name'),
                            max_length=255)

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

    status = StatusField(verbose_name=_('status'), )

    tracker = FieldTracker()

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          help_text='!!切勿随意修改!!',
                          format='File')

    def sync_status(self):
        return sync_status_from(self)

    def __str__(self):
        return str(self.name)

    __unicode__ = __str__

    def get_absolute_url(self):
        return '/authors/%s' % self.pk

    def get_absolute_iospc_url(self):
        return reverse('iospc_vendors_list', kwargs={'slug': 'spec-top-author', 'pk': self.pk})


class PackageQuerySet(QuerySet):

    def by_category(self, category):
        return self.filter(categories__contains=category)

    def by_author(self, author):
        return self.filter(author=author)

    def by_published_order(self, newest=None):
        qs = self.published()
        return qs.by_released_order(newest=newest)

    def by_released_order(self, newest=None):
        field = 'released_datetime'
        if newest is None:
            return self
        elif newest is True:
            return self.order_by('-' + field)
        else:
            return self.order_by('+' + field)

    def by_rankings_order(self):
        return self.order_by('-download_count')

    def by_updated_order(self):
        return self.order_by('-updated_datetime')

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(
            released_datetime__lte=dt, status=self.model.STATUS.published)

    def unpublished(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(released_datetime__gt=dt) \
            .exclude(status=self.model.STATUS.published)


class PackageManager(cachemixin.PackageCacheManagerMixin,
                     CurrentSitePassThroughManager):

    pass


class AllPackageManager(cachemixin.PackageCacheManagerMixin,
                        PassThroughManager):
    pass


PACKAGE_FLAGS = ['首发', '热门', '活动', '礼包']


def get_flags_from(tags_text):
    tags_text = tags_text.strip() if tags_text else None
    if not tags_text:
        return []
    _flags = []
    for f in PACKAGE_FLAGS:
        if f in tags_text:
            _flags.append(f)
    return _flags


package_name_pattern = '[\w\d_.-]+'


class Package(PlatformBase,
              urlmixin.PackageAbsoluteUrlMixin,
              cachemixin.PackageTaggingMixin,
              SiteRelated, models.Model):

    objects = PackageManager.for_queryset_class(PackageQuerySet)()

    all_objects = AllPackageManager.for_queryset_class(PackageQuerySet)()

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
        index_together = (
            ('site', 'id'),
            ('site', 'status', ),
            ('site', 'status', 'released_datetime'),
        )

    title = models.CharField(
        verbose_name=_('package title'),
        max_length=255)

    package_name = models.CharField(
        validators=[
            validators.RegexValidator(
                re.compile('^%s$' % package_name_pattern),
                '包名无效，只能由[A-Za-z0-9_.]字符组合而成', 'invalid')
        ],
        verbose_name=_('package name'),
        db_index=True,
        max_length=255)

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

    latest_version = models.ForeignKey('PackageVersion',
                                       null=True,
                                       default=None,
                                       db_index=True,
                                       related_name='+')

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
        #limit_choices_to=dict(
        #    site_id=current_site_id,
        #),
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

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          format='File')

    def is_published(self):
        return self.status == self.STATUS.published \
            and self.released_datetime <= now()


    primary_category = models.ForeignKey('taxonomy.Category',
                                         related_name='primary_packages',
                                         #limit_choices_to=dict(
                                         #    site_id=current_site_id,
                                         #),
                                         null=True, blank=True)

    root_category = models.ForeignKey('taxonomy.Category',
                                      related_name='root_packages',
                                      #limit_choices_to=dict(
                                      #   site_id=current_site_id,
                                      #),
                                      null=True, blank=True)

    main_category_names = models.CharField(max_length=500, default='')


    @property
    def main_category(self):
        cat = None
        try:
            if self.primary_category_id:
                cat = self.categories.model.objects\
                    .get_cache_category(self.primary_category_id)
        except self.categories.model.DoesNotExist:
            pass
        return cat

    @property
    def main_categories(self):
        if hasattr(self, '_main_categories'):
            return self._main_categories
        main_cat, cats = self._package_categories()
        self._main_categories = cats
        self._main_category = main_cat
        return self._main_categories

    def _package_categories(self):
        from taxonomy.models import Category
        cats = [cat for cat in self.categories.all()
                if cat.is_leaf_node() and \
                   cat.get_root().slug in Category.ROOT_SLUGS]
        try:
            main_category = cats[0]
        except IndexError:
            main_category = None
        return main_category, cats


    # 奖励金币
    has_award = models.BooleanField(default=False)

    award_coin = models.IntegerField(default=0)

    def clean(self):
        super(Package, self).clean()
        self.updated_datetime = now()

    def __str__(self):
        return self.title

    __unicode__ = __str__

    def get_absolute_url(self, link_type=0):
        if link_type == 0:
            return '/packages/%s/' % self.package_name
        else:
            return '/packages/%s/' % self.pk

    def get_package_url(self, link_type=0):
        if link_type == 0:
            return '/package/?name=%s' % self.package_name
        else:
            return '/package/?id=%s' % self.pk

    @property
    def flags(self):
        return get_flags_from(self.tags_text)


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

    def published(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(
            released_datetime__lte=dt, status=self.model.STATUS.published)

    def unpublished(self, released_hourly=True):
        dt = released_hourly_datetime(now(), released_hourly)
        return self.filter(released_datetime__gt=dt) \
            .exclude(status=self.model.STATUS.published)

    def latest_version(self):
        return self.latest('version_code')

    def latest_published(self, released_hourly=True):
        return self.published(released_hourly).latest('version_code')


def package_workspace_path(package):
    _id = package.pk
    subdir = 'package'
    try:
        if hasattr(package, 'track_id'):
            _id = package.track_id
        else:
            iospackage = package.iospackage
            _id = iospackage.track_id
        subdir = 'ipackage'
    except ObjectDoesNotExist:
        pass
    return join(subdir, str(_id))


def packageversion_workspace_path(version):
    if version.package.workspace:
        prefix = version.package.workspace.name
    else:
        prefix = package_workspace_path(version.package)
    return join(prefix, 'v%s' % version.version_code)


def version_upload_path(instance, filename):
    if instance.workspace:
        prefix = instance.workspace.name
    else:
        prefix = packageversion_workspace_path(instance)
    return join(prefix, filename)


class PkgReportField(models.BooleanField):

    def __init__(self, *args, **kwargs):
        super(PkgReportField, self).__init__(*args, **kwargs)
        self.added_fields = self._get_added_fields()

    def _get_added_fields(self):
        return {
            "network": ('%s_network', models.BooleanField(verbose_name='网络',
                                                          default=False, blank=True)),
            "gplay": ('%s_gplay', models.BooleanField(verbose_name='谷歌服务',
                                                      default=False, blank=True)),
            "root": ('%s_root', models.BooleanField(verbose_name='root权限',
                                                    default=False, blank=True)),
            "adv": ('%s_adv', models.BooleanField(verbose_name='广告',
                                                  default=False, blank=True)),
            }

    def _field_name(self, attrname, name):
        return self.added_fields[name][0] % attrname

    def _field_type(self, name):
        return self.added_fields[name][1]

    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            for idx in self.added_fields.keys():
                cls.add_to_class(self._field_name(name, idx), self._field_type(idx))
        super(PkgReportField, self).contribute_to_class(cls, name)


class PackageVersionManager(cachemixin.PackageVersionCacheManagerMixin,
                            CurrentSitePassThroughManager):
    pass


class AllPackageVersionManager(cachemixin.PackageVersionCacheManagerMixin,
                               PassThroughManager):
    pass


class PackageVersion(urlmixin.ModelAbsoluteUrlMixin,
                     cachemixin.PackageVersionTaggingMixin,
                     PlatformBase,
                     SiteRelated, models.Model):

    objects = PackageVersionManager\
        .for_queryset_class(PackageVersionQuerySet)()

    all_objects = AllPackageVersionManager\
        .for_queryset_class(PackageVersionQuerySet)()

    class Meta:
        verbose_name = _("Package Version")
        verbose_name_plural = _("Package Versions")
        unique_together = (
            ('site', 'package', 'version_code'),
        )
        index_together = (
            ('site', 'package', ),
            ('site', 'id', ),
            ('site', 'status', ),
            ('site', 'status', 'released_datetime'),
            ('has_award', ),
            ('site', 'has_award', ),
            ('site', 'award_coin', ),
            ('site', 'reported', ),
            ('site', 'reported', 'status', ),
        )

    icon = QiniuThumbnailerImageField(
        default='',
        upload_to=version_upload_path,
        blank=True,
        max_length=500,
        thumbnail_storage=image_storage,
        storage=image_storage,
    )

    cover = QiniuThumbnailerImageField(
        default='',
        upload_to=version_upload_path,
        blank=True,
        max_length=500,
        thumbnail_storage=image_storage,
        storage=image_storage,
    )

    download = PkgFileField(
        verbose_name=_('version file'),
        upload_to=version_upload_path,
        default='',
        max_length=500,
        storage=storage,
        blank=True)

    di_download = PkgFileField(
        verbose_name=_('version file with data integration'),
        upload_to=version_upload_path,
        default='',
        blank=True,
        max_length=500,
        storage=storage,
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
        max_length=50,
        blank=False,
        null=False)

    version_code = models.IntegerField(
        verbose_name=_('version code'),
        max_length=8,
        default=1,
        blank=False)

    subtitle = models.CharField(
        verbose_name=_('version subtitle'),
        default='',
        blank=True,
        max_length=255)

    summary = models.CharField(
        verbose_name=_('summary'),
        max_length=255,
        default="",
        blank=True)

    description = models.TextField(
        verbose_name=_('description'),
        default="",
        blank=True)

    whatsnew = models.TextField(
        verbose_name=_("what's new"),
        default="",
        blank=True)

    tags_text = TagField(
        verbose_name=_('tags'),
        default="",
        blank=True)

    #supported_features = models.ManyToManyField('SupportedFeature', blank=True)

    #supported_languages = models.ManyToManyField('SupportedLanguage', blank=True)

    #supported_devices = models.ManyToManyField('SupportedDevice', blank=True)

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

    updated_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    stars = StarsField(verbose_name=_('Star'))

    tracker = FieldTracker()

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          format='File')

    resources = MultiResourceField()

    comments = CommentsField()

    # 奖励金币
    has_award = models.BooleanField(default=False)

    award_coin = models.IntegerField(default=0)

    # report
    reported = PkgReportField(verbose_name='已检查', default=False, blank=True)

    def clean(self):
        super(PackageVersion, self).clean()
        self.updated_datetime = now()

    def get_absolute_url(self, link_type=0):
        if link_type == 0:
            return '/packages/%s/%s' %(self.package.package_name, self.version_name)
        else:
            return '/packageversions/%s' % self.pk

    def __str__(self):
        return "%s:%s" %(self.package, self.version_name)

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

    def is_download_cpk(self, filetype=None):
        download = self.get_download(filetype)
        if not download:
            return False
        if download == self.di_download:
            return True
        return False

    def is_download_apk(self, filetype=None):
        download = self.get_download(filetype)
        if not download:
            return False
        if download == self.download:
            return True
        return False

    def get_download(self, filetype=None):
        if filetype is None:
            return self.di_download if self.di_download else self.download
        else:
            if filetype == self.DOWNLOAD_FILETYPE_DI:
                return self.di_download
            else:
                return self.download

    def get_download_size(self, filetype=None):
        if filetype == self.DOWNLOAD_FILETYPE_DI:
            return self.di_download_size
        elif filetype == self.DOWNLOAD_FILETYPE_PK:
            return self.download_size
        else:
            return self.di_download_size if self.di_download else self.download_size

    def get_download_url(self, filetype=None, is_dynamic=True, **kwargs):
        kwargs.setdefault('entrytype', 'web')
        if is_dynamic:
            url = self.get_download_dynamic_url(filetype=filetype)
        else:
            url = self.get_download_static_url(filetype=filetype)
        return qurl_to(url, **kwargs)

    def get_download_static_url(self, filetype=None):
        return self.get_download(filetype=filetype).url

    def get_download_dynamic_url(self, filetype=None):
        kwargs = dict(pk=self.pk)
        if filetype:
            kwargs['filetype'] = filetype
        return reverse('download_packageversion', kwargs=kwargs)

    def sync_status(self):
        return sync_status_from(self)

    def _get_languages(self):
        lang_desc_maps = dict(
            ZH='中文',
            EN='英文',
            _='其他'
        )
        return []
        lang_codes = list(self.supported_languages.values_list('code', flat=True))
        desc_langs = []
        if len(lang_codes):
            if 'ZH' in lang_codes:
                del lang_codes[lang_codes.index('ZH')]
                desc_langs.append(lang_desc_maps['ZH'])
            if 'EN' in lang_codes:
                del lang_codes[lang_codes.index('EN')]
                desc_langs.append(lang_desc_maps['EN'])
            if len(lang_codes):
                desc_langs.append(lang_desc_maps['_'])
        else:
            desc_langs.append(lang_desc_maps['_'])
        return desc_langs

    @property
    def language_names(self):
        if not hasattr(self, '_language_names'):
            self._language_names = self._get_languages()
        return self._language_names

    @property
    def flags(self):
        return get_flags_from(self.tags_text)



tagging.register(PackageVersion)


def screenshot_upload_path(instance, filename):
    subdir = 'screenshots'
    if instance.kind != instance.KIND.default:
        subdir = "%s%s" % (instance.kind, subdir)

    if instance.version.workspace:
        prefix = instance.version.workspace.name
    else:
        prefix = packageversion_workspace_path(instance.version)
    return join(prefix, subdir, filename)


class PackageVersionScreenshotManager(models.Manager):

    def ipad(self):
        return self.filter(kind='ipad')

    def default(self):
        return self.filter(kind='default')


class PackageVersionScreenshot(models.Model):

    objects = PackageVersionScreenshotManager()

    version = models.ForeignKey(PackageVersion, related_name='screenshots')

    image = QiniuThumbnailerImageField(
        upload_to=screenshot_upload_path,
        max_length=500,
        blank=False,
        thumbnail_storage=screenshot_thumbnail_storage,
        storage=screenshot_thumbnail_storage,
    )

    def image_url(self, size=None):
        if size:
            return self.image[size].url
        return self.image.url

    KIND = Choices(
        ('default', 'default', 'Default'),
        ('ipad', 'ipad', 'iPad'),
    )

    kind = models.CharField(default=KIND.default,
                            choices=KIND,
                            max_length=20,
                            blank=True,)

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

    def save(self, *args, **kwargs):
        self.kind = slugify(self.kind.replace(" ", ''))
        return super(PackageVersionScreenshot, self).save(*args, **kwargs)

    def delete(self, using=None):
        self.image.delete(save=False)
        super(PackageVersionScreenshot, self).delete(using=using)

    def __str__(self):
        try:
            return self.image.url
        except:
            return self.alt

    class Meta:
        index_together = (
            ('version', 'kind'),
        )


from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete, post_delete
from django.dispatch import receiver


def sync_pkg_cats(pkg):
    """
        Package.categories同步(primary/root)_category
    """
    main_category, main_categories = pkg._package_categories()
    if main_category:
        if pkg.primary_category_id != main_category.pk:
            pkg.primary_category = main_category
            pkg.root_category = main_category.get_root()
    else:
        pkg.primary_category_id = None
        pkg.root_category_id = None

    if main_categories:
        main_category_names = [cat.name for cat in main_categories]
        pkg.main_category_names = ",".join(main_category_names)


@receiver(m2m_changed, sender=Package.categories.through)
def package_post_changed_category(sender, action, instance, model, pk_set, **kwargs):
    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    if isinstance(instance, Package):
        pkg = instance
        sync_pkg_cats(pkg)
        pkg.save()
    else:
        pkgs = model.objects.in_bluk(list(pk_set))
        for p in pkgs:
            sync_pkg_cats(p)
            p.save()


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


_sync_pkg_field = '_version_sync_package_published'

@receiver(pre_save, sender=PackageVersion)
def package_version_pre_save_check_publish_to_sync(sender, instance, **kwargs):
    # 状态更改 或者发布时间更改至未来时间
    if instance.tracker.has_changed('status') or \
            (instance.status == PackageVersion.STATUS.published
             and instance.tracker.has_changed('released_datetime')):
        setattr(instance, _sync_pkg_field, True)


@receiver(post_save, sender=PackageVersion)
def package_version_post_save(sender, instance, **kwargs):
    """
        发布软件版本 同步package状态(status/released_datetime)
    """
    if getattr(instance, _sync_pkg_field, False):
        from warehouse import tasks
        package = instance.package
        now_dt = now().astimezone()
        try:
            latest_published = package.versions.latest_published(released_hourly=False)

            # 当前最后可发布版本,不是刚保存的这个版本(instance)则重置最后发布版本
            # 使得热数据重置为最后可发布版本
            if latest_published.pk != instance.pk:
                latest_published_released_dt = latest_published.released_datetime.astimezone()

                if now_dt >= latest_published_released_dt:
                    tasks.publish_packageversion.apply_async((latest_published.pk, ),
                                                             countdown=10)
                elif now_dt < latest_published_released_dt:
                    tasks.publish_packageversion\
                        .apply_async((latest_published.pk, ),
                                     eta=latest_published_released_dt+datetime.timedelta(seconds=10))

        except ObjectDoesNotExist:
            # 没有最后可发布版本(未到发布时间) 清除热数据
            tasks.delete_package_data_center(package.pk)

        if instance.status == PackageVersion.STATUS.published:
            version_released_dt = instance.released_datetime.astimezone()

            # 1. 在过去或当时发布 则及时处理
            if now_dt >= version_released_dt:
                # 因为当前线程保存数据至数据库耗时比 后台执行发布task.publish_packageversion慢
                # countdown 10s保证数据状态同步
                tasks.publish_packageversion.apply_async((instance.pk,),
                                                         countdown=10)
                return

            # 2. 在未来的时间发布 使用消息队列
            elif now_dt < version_released_dt:
                # 在未来发布时间基础上加10秒，保证数据状态同步
                # 原因同上
                tasks.publish_packageversion \
                    .apply_async((instance.pk,),
                                 eta=version_released_dt+datetime.timedelta(seconds=10))
                return


@receiver(pre_delete, sender=PackageVersion)
def package_version_pre_delete(sender, instance, **kwargs):
    setattr(instance, '_delete_version_pk', instance.package.pk)
    setattr(instance, '_package_pk', instance.package.pk)


@receiver(post_delete, sender=PackageVersion)
def package_version_post_delete(sender, instance, **kwargs):
    #pk = getattr(instance, '_delete_version_pk', None)
    pkg_pk = getattr(instance, '_package_pk', None)
    from warehouse import tasks
    try:
        latest_published = instance.package.versions.latest_published(released_hourly=False)
        released_dt = latest_published.released_datetime.astimezone()
        now_dt = now().astimezone()
        if released_dt > now_dt:
            eta = released_dt + datetime.timedelta(seconds=10)
        else:
            eta = now_dt + datetime.timedelta(seconds=10)
        tasks.publish_packageversion.apply_async((latest_published.pk,), eta=eta)

    except ObjectDoesNotExist:
        tasks.delete_package_data_center(pkg_pk)


@receiver(pre_save, sender=PackageVersion)
def package_version_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        package = instance.package
        if not instance.summary:
            instance.summary = package.summary

        if not instance.subtitle:
            instance.subtitle = package.title

        if not instance.description:
            instance.description = package.description

        instance.tags_text = " ".join([instance.tags_text, package.tags_text])

    if not instance.workspace:
        instance.workspace = packageversion_workspace_path(instance)


SYNC_PACKAGEVERSION_CHANGED_FIELDS = [
    'stars_count',
    'has_award',
    'award_coin',
]


@receiver(pre_save, sender=PackageVersion)
def package_version_pre_save_check_changed_fields(sender, instance, **kwargs):
    # ignore new create
    if instance.pk is None:
        return
    instance._sync_changed_fields = getattr(instance, '_sync_changed_fields', dict())
    for field_name in SYNC_PACKAGEVERSION_CHANGED_FIELDS:
        if instance.tracker.has_changed(field_name):
            instance._sync_changed_fields[field_name] = True

    instance.has_award = bool(instance.award_coin)



@receiver(post_save, sender=PackageVersion)
def package_version_post_save_check_to_sync(sender, instance, created=False, **kwargs):
    has_changed = getattr(instance, '_sync_changed_fields', dict())
    # ignore not published
    if instance.status != PackageVersion.STATUS.published:
        return

    for field_name in SYNC_PACKAGEVERSION_CHANGED_FIELDS:
        if has_changed.get(field_name):
            from warehouse.tasks import sync_package
            sync_package.apply_async((instance.package.pk,),
                                     countdown=10)
            break
    delattr(instance, '_sync_changed_fields')


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

    if changed and not instance.tracker.has_changed('updated_datetime'):
        instance.updated_datetime = now().astimezone()

    if not instance.workspace:
        instance.workspace = ''


@receiver(post_save, sender=Package)
def package_post_save(sender, instance, created=False, **kwargs):
    if created:
        instance.workspace = package_workspace_path(instance)
        instance.save()

    if instance.status != Package.STATUS.published:
        from warehouse.tasks import delete_package_data_center
        delete_package_data_center(instance.pk)


@receiver(pre_delete, sender=Package)
def package_pre_delete(sender, instance, **kwargs):
    setattr(instance, '_delete_pk', instance.pk)


@receiver(post_delete, sender=Package)
def package_post_delete(sender, instance, **kwargs):
    pk = getattr(instance, '_delete_pk', None)
    from warehouse.tasks import delete_package_data_center
    delete_package_data_center(pk)



@receiver(pre_save, sender=Author)
def author_pre_save(sender, instance, **kwargs):
    if not instance.workspace:
        instance.workspace = author_workspace_path(instance)


class SupportedLanguage(models.Model):

    LANG_MASK_ZH = 0b100

    LANG_MASK_EN = 0b010

    LANG_MASK_OTHER = 0b001

    code = models.CharField(unique=True, max_length=10)

    name = models.CharField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        if self.pk is None and not self.name:
            self.name = self.code.lower()
        return super(SupportedLanguage, self).save(*args, **kwargs)

    def __str__(self):
        if self.name:
            return self.name
        return self.code


class SupportedFeature(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager()

    code = models.CharField(max_length=1024)

    name = models.CharField(default='',
                            blank=True,
                            max_length=30)

    def __str__(self):
        if self.name:
            return self.name
        return self.code

    class Meta:
        unique_together = (
            ('site', 'code'),
        )


class SupportedDevice(SiteRelated, models.Model):

    objects = CurrentSitePassThroughManager()

    code = models.CharField(unique=True, max_length=150)

    name = models.CharField(default='', blank=True, max_length=50)

    def __str__(self):
        if self.name:
            return self.name
        return self.code

    class Meta:
        unique_together = (
            ('site', 'code')
        )


# IOS
class IOSPlatform(PlatformBase):

    _is_base = False

    _platform = PlatformBase.PLATFORM_IOS


class IOSAuthor(IOSPlatform, Author):

    objects = CurrentSitePassThroughManager.for_queryset_class(AuthorQuerySet)()

    artist_id = models.IntegerField(verbose_name='artistId', unique=True)

    view_url = models.URLField(verbose_name='artistViewUrl',
                               max_length=500,
                               null=True,
                               blank=True)

    seller_url = models.URLField(verbose_name='sellerUrl',
                                 max_length=500,
                                 null=True,
                                 blank=True)

    seller_name = models.CharField(verbose_name='sellerName',
                                   null=True,
                                   blank=True,
                                   max_length=150)


class IOSPackage(IOSPlatform, Package):

    objects = CurrentSitePassThroughManager.for_queryset_class(PackageQuerySet)()

    track_id = models.IntegerField(verbose_name='trackId', unique=True)

    view_url = models.URLField(verbose_name='trackViewUrl',
                               max_length=500,
                               null=True,
                               blank=True)

    appleuser_rating = models.FloatField(verbose_name='averageUserRating',
                                         default=None,
                                         null=True,
                                         blank=True)


class IOSPackageVersion(IOSPlatform, PackageVersion):

    objects = CurrentSitePassThroughManager \
        .for_queryset_class(PackageVersionQuerySet)()

    formatted_price = models.CharField(max_length=50,
                                       null=True,
                                       blank=True)

    price = models.DecimalField(default=0,
                                max_digits=12,
                                decimal_places=3,
                                db_index=True)

    price_currency = models.CharField(verbose_name='currency',
                                      max_length=4,
                                      default=None,
                                      blank=True,
                                      null=True)

    appleuser_rating = models.FloatField(verbose_name='averageUserRatingForCurrentVersion',
                                         default=None,
                                         null=True,
                                         blank=True)

    appleformatted_rating = models.CharField(verbose_name='trackContentRating',
                                             default=None,
                                             blank=True,
                                             null=True,
                                             max_length=12)

    is_support_iphone = models.BooleanField(default=True,
                                            db_index=True,
                                            blank=True)

    is_support_ipad = models.BooleanField(default=False,
                                          db_index=True,
                                          blank=True)

    def is_free(self):
        return self.price.is_zero()

    def _get_support_device_types(self):
        devtypes = ['iPad', 'iPhone', 'iPod']
        return []
        result = set()
        for dev in self.supported_devices.all():
            for t in devtypes:
                if dev.code.startswith(t):
                    result.add(t)
                    break
        return list(result)

    @property
    def device_types(self):
        if not hasattr(self, '_support_device_types'):
            self._support_device_types = self._get_support_device_types()
        return self._support_device_types

    @property
    def support_ipad(self):
        return 'iPad' in self.device_types

    @property
    def support_iphone(self):
        return 'iPhone' in self.device_types

    @property
    def support_alldevices(self):
        return self.support_ipad and self.support_iphone


if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((PkgReportField,), [], {}),
            ],
                                patterns=["warehouse\.models\."])
    except ImportError:
        pass
