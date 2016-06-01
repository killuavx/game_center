# -*- coding: utf-8 -*-
from bson import ObjectId
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Count, Q
from django.utils.timezone import *
from datetime import timedelta, datetime
from django.db import models
from django.db.models.query import QuerySet
from copy import deepcopy
from django.utils.encoding import force_bytes
from model_utils.managers import PassThroughManager
from model_utils.tracker import FieldTracker
from .documents.event import Event
from django.core.urlresolvers import resolve, Resolver404, reverse
from hashlib import md5
from .helpers import PLATFORM_ANDROID, PLATFORM_IOS, packageversion_id_fill, find_platform_categories

import logging
logger = logging.getLogger('scripts')

UNDEFINED = 'undefined'

# Dimensions

PLATFORM_CHOICES = (
    (UNDEFINED, 'None'),
    (PLATFORM_ANDROID, 'Android'),
    (PLATFORM_IOS, 'iOS'),
)

PLATFORM_DEFAULT = PLATFORM_ANDROID

platform = models.CharField(max_length=20,
                            db_index=True,
                            default=PLATFORM_DEFAULT,
                            choices=PLATFORM_CHOICES)

def dictdata_strip_val(data):
    for f, v in data.items():
        if isinstance(v, str):
            data[f] = v.strip()
    return data


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class Dimension(models.Model):
    
    class Meta:
        abstract = True


class EventDimManager(models.Manager):

    def get_or_create_events(self):
        results = list()
        for k, n in Event.EVENT_TYPES:
            inst, created = self.get_or_create(eventtype=k)
            results.append((inst, created))
        return results


class EventDim(Dimension):

    objects = EventDimManager()

    eventtype = models.CharField(max_length=20)

    class Meta:
        verbose_name = '事件'
        verbose_name_plural = '事件列表'
        db_table = 'dim_event'

    def __str__(self):
        return str(self.eventtype)


def random_key(string):
    m = md5()
    m.update(force_bytes(string))
    return m.hexdigest()


class ProductKeyDim(Dimension):

    name = models.CharField(max_length=30, default=UNDEFINED)

    key = models.CharField(max_length=40,
                           unique=True,
        default=lambda:random_key(datetime.now().isoformat())
    )

    entrytype = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品列表'
        db_table = 'dim_productkey'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.key


class ProductDim(Dimension):

    entrytype = models.CharField(max_length=50,
                                 db_index=True)

    channel = models.CharField(max_length=50,
                               db_index=True,
                               blank=True,
                               default=UNDEFINED)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品列表'
        db_table = 'dim_product'
        unique_together = (
            ('entrytype', 'channel'),
        )

    def __str__(self):
        return "%s:%s" %(self.entrytype, self.channel)


class DateDimManager(models.Manager):

    def get_or_create_dates_between(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError('end datetime must great than or equal to start datetime')
        result = list()
        i = 0
        while True:
            next_date = start_date + timedelta(days=i)
            result.append(self.get_or_create(datevalue=next_date))
            if next_date >= end_date:
                break
            i += 1
        return result

    def get_by_datetime(self, dt):
        tz = get_default_timezone()
        dt = make_aware(dt, tz) if not is_aware(dt) else dt
        return self.filter(datevalue=dt.date()).get()

    def between(self, start_date, end_date):
        tz = get_default_timezone()
        s_date = make_aware(start_date, tz) if not is_aware(start_date) else start_date
        e_date = make_aware(end_date, tz) if not is_aware(end_date) else end_date
        return self.filter(datevalue__gte=s_date.date(),
                           datevalue__lte=e_date.date())\
            .order_by('datevalue')

    def get_days_dims(self, dt, interval=3):
        assert interval >= 1
        end = dt + timedelta(days=interval-1)
        return self.between(dt, end)

    def get_daily_dims(self, dt):
        return self.get_days_dims(dt, interval=1)

    def get_weekly_dims(self, dt):
        return self.filter(year=dt.year,
                           week=int(dt.strftime('%W')))\
            .order_by('datevalue')

    def get_monthly_dims(self, dt):
        return self.filter(year=dt.year, month=dt.month)\
            .order_by('datevalue')

    def until(self, end_date, with_self=False):
        tz = get_default_timezone()
        e_date = make_aware(end_date, tz) if not is_aware(end_date) else end_date
        if with_self:
            return self.filter(datevalue__lte=e_date.date())
        else:
            return self.filter(datevalue__lt=e_date.date())

    def until_dim(self, end_dim, with_self=False):
        if with_self:
            return self.filter(datevalue__lte=end_dim.datevalue)
        else:
            return self.filter(datevalue__lt=end_dim.datevalue)


class DateDim(Dimension):

    objects = DateDimManager()

    datevalue = models.DateField(unique=True)

    year = models.PositiveIntegerField(max_length=4)

    week = models.PositiveIntegerField(max_length=3)

    month = models.PositiveIntegerField(max_length=2)

    dayofweek = models.PositiveIntegerField(max_length=1)

    day = models.PositiveIntegerField(max_length=2)

    tracker = FieldTracker()

    class Meta:
        verbose_name = '日期'
        verbose_name_plural = '日期列表'
        index_together = (
            ('year', 'month', 'day'),
            ('year', 'week'),
        )
        db_table = 'dim_date'

    def save(self, **kwargs):
        if not self.pk or self.tracker.has_changed('datevalue'):
            d = self.datevalue
            self.year = d.year
            self.month = d.month
            self.day = d.day
            self.dayofweek = int(d.strftime('%w'))
            self.week = int(d.strftime('%W'))
        return super(DateDim, self).save(**kwargs)

    def create_next_date(self):
        datevalue = self.datevalue + timedelta(days=1)
        cls = self.__class__
        return self.objects.create(datevalue=datevalue)

    def get_or_create_next_date(self):
        datevalue = self.datevalue + timedelta(days=1)
        cls = self.__class__
        return cls.objects.get_or_create(datevalue=datevalue)

    def __str__(self):
        return str(self.datevalue)


class HourDimManager(models.Manager):

    def get_or_create_24_hour(self):
        for i in range(24):
            self.get_or_create(hour=i)


class HourDim(Dimension):

    objects = HourDimManager()

    hour = models.PositiveSmallIntegerField(max_length=2,
                                            db_index=True)

    class Meta:
        db_table = 'dim_hour'

    def get_or_create_next_hour(self):
        hour = self.hour + 1
        if hour >= 24:
            raise ValueError('')
        return self.objects.get_or_create(hour=hour)

    def __str__(self):
        return str(self.hour)


def packagecategorydim_fill_to(pkg_or_ver_dim):
    obj = pkg_or_ver_dim
    cats = find_platform_categories(obj.platform, obj)
    if cats:
        root_cat, primary_cat, second_cat = cats
        if root_cat:
            obj.root_category, created = packagecategorydim_get_or_category_from(root_cat)
        if primary_cat:
            obj.primary_category, created = packagecategorydim_get_or_category_from(primary_cat)
        if second_cat:
            obj.second_category, created = packagecategorydim_get_or_category_from(second_cat)
    return obj


def packagecategorydim_get_or_category_from(category):
    if not category:
        return None, None
    obj, created = PackageCategoryDim.objects.get_or_create(
        cid=category.pk,
        slug=category.slug,
        defaults=dict(
            name=category.name
        )
    )
    if obj.name != category.name:
        category.name = obj.name
        category.save()
    return obj, created


class PackageCategoryDim(Dimension):

    cid = models.IntegerField(verbose_name='源数据taxonomy_category.id',
                              null=True)

    name = models.CharField(max_length=100,
                            default=UNDEFINED)

    slug = models.CharField(max_length=100,
                            default=UNDEFINED,
                            unique=True)

    def __str__(self):
        return "%s:%s:%s" %(self.name, self.slug, self.cid)

    class Meta:
        db_table = 'dim_packagecategory'
        verbose_name = '应用分类'
        verbose_name_plural = '应用分类列表'


class BasePackageDim(Dimension):

    title = models.CharField(max_length=255, default='')

    PLATFORM_CHOICES = PLATFORM_CHOICES

    platform = deepcopy(platform)

    root_category = models.ForeignKey(PackageCategoryDim, null=True, related_name='+')

    primary_category = models.ForeignKey(PackageCategoryDim, null=True, related_name='+')

    second_category = models.ForeignKey(PackageCategoryDim, null=True, related_name='+')

    class Meta:
        abstract = True


def sync_package_dim(from_, to_):
    to_.root_category_id = from_.root_category_id
    to_.primary_category_id = from_.primary_category_id
    to_.second_category_id = from_.second_category_id
    to_.pid = from_.pid
    to_.title = from_.title
    return to_


def packagekey_dim_has_diff_between(obj1, obj2):
    return not(obj1.root_category_id == obj2.root_category_id
               and obj1.primary_category_id == obj2.primary_category_id
               and obj1.second_category_id == obj2.second_category_id
               and obj1.title == obj2.title)


class PackageKeyManager(models.Manager):

    def get_or_create_from_package_dim(self, package_dim):
        packagekey, created = PackageKeyDim.objects \
            .get_or_create(platform=package_dim.platform,
                           package_name=package_dim.package_name)
        if created or (package_dim.pid and not packagekey.pid) \
            or packagekey_dim_has_diff_between(packagekey, package_dim):
            packagekey = sync_package_dim(package_dim, packagekey)
            packagekey.save()
        return packagekey, created


class PackageKeyDim(BasePackageDim):

    objects = PackageKeyManager()

    pid = models.IntegerField(verbose_name='源数据库warehouse_package.id',
                              null=True)

    package_name = models.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = 'dim_packagekey'
        unique_together = (
            ('platform', 'package_name',)
        )
        verbose_name = '应用'
        verbose_name_plural = '应用列表'

    def __str__(self):
        return "%s:%s:%s" %(self.title, self.package_name, self.pid)

    @property
    def package(self):
        if not self.pid:
            return None
        from warehouse.models import Package
        try:
            return Package.objects.get(pk=self.pid)
        except Package.DoesNotExist:
            return None

    def package_admin_url(self):
        link = reverse(
            'admin:%s_%s_change' % ('warehouse', 'package'),
            args=[self.pid])
        return link


class PackageDim(BasePackageDim):

    pid = models.IntegerField(verbose_name='源数据库warehouse_package.id',
                              null=True)

    vid = models.IntegerField(verbose_name='源数据库warehouse_packageversion.id',
                              null=True)

    package_name = models.CharField(max_length=255, db_index=True)

    version_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'dim_package'
        unique_together = (
            ('platform', 'package_name', 'version_name',),
        )
        index_together = (
            ('platform', 'package_name',),
        )
        verbose_name = '应用版本'
        verbose_name_plural = '应用版本列表'

    def prepare_package(self):
        """
        from warehouse.models import Package
        if self.version and not self.version_name:
            self.version_name = self.version.version_name

        if self.version and not self.package:
            self.package = self.version.package

        if self.package_name and not self.package:
            try:
                self.package = Package.objects.get(package_name=self.package_name)
            except Package.DoesNotExist:
                pass

        if self.package and not self.package_name:
            self.package_name = self.package.package_name

        if self.package and self.version_name and not self.version:
            try:
                self.version = self.package.versions.get(version_name=self.version_name)
            except Package.DoesNotExist:
                pass

        if self.package and not self.title:
            self.title = self.package.title
            if hasattr(self.version, 'label'):
                self.title += ' | ' + self.version.label
        """

    def __str__(self):
        return "%s:%s:%s:%s:%s" % (self.title,
                                   self.package_name, self.pid,
                                   self.version_name, self.vid)

    @property
    def package(self):
        if not self.pid:
            return None
        from warehouse.models import Package
        try:
            return Package.objects.get(pk=self.pid)
        except Package.DoesNotExist:
            return None

    def package_admin_url(self):
        link = reverse(
            'admin:%s_%s_change' % ('warehouse', 'package'),
            args=[self.pid])
        return link

    @property
    def version(self):
        if not self.vid:
            return None
        from warehouse.models import PackageVersion
        try:
            return PackageVersion.objects.get(pk=self.vid)
        except PackageVersion.DoesNotExist:
            return None

    def package_admin_url(self):
        link = reverse(
            'admin:%s_%s_change' % ('warehouse', 'packageversion'),
            args=[self.vid])
        return link


class SubscriberIdDim(Dimension):

    imsi = models.CharField(max_length=30,
                            unique=True,
                            default=UNDEFINED)

    mnc = models.CharField(max_length=10,
                           default=UNDEFINED,
                           db_index=True)

    class Meta:
        db_table = 'dim_subscriberid'
        verbose_name = '运营商服务号'
        verbose_name_plural = '运营商服务号列表'

    def __str__(self):
        return self.imsi


class DeviceDim(Dimension):
    """
    独立设备
    {
    "have_gravity" : true,
    "have_wifi" : true,
    "phone_type" : 1,

    "have_gps" : true,
    "have_bt" : true,
    "is_mobiledevice" : true,
    "imsi" : "",
    "phone_type" : 2,
    "is_mobiledevice" : true,
    }
    """

    imei = models.CharField(max_length=25,
                            default=UNDEFINED,
                            unique=True)

    # same to ProductDim.platform
    PLATFORM_CHOICES = PLATFORM_CHOICES

    platform = deepcopy(platform)

    class Meta:
        db_table = 'dim_device'
        verbose_name = '设备号'
        verbose_name_plural = '设备号列表'

    def __str__(self):
        return self.imei


class DevicePlatformDim(Dimension):
    """
    设备平台
    """

    PLATFORM_CHOICES = PLATFORM_CHOICES

    platform = deepcopy(platform)

    class Meta:
        db_table = 'dim_deviceplatform'
        verbose_name = '平台'
        verbose_name_plural = '平台列表'

    def __str__(self):
        return self.platform


class DeviceOSDim(Dimension):
    """
    设备系统
    """

    # same to ProductDim.platform
    PLATFORM_CHOICES = PLATFORM_CHOICES

    platform = deepcopy(platform)

    os_version = models.CharField(max_length=300,
                                  default=UNDEFINED)

    class Meta:
        db_table = 'dim_deviceos'
        unique_together = (
            ('platform', 'os_version'),
        )
        verbose_name = '设备os'
        verbose_name_plural = '设备os列表'

    def __str__(self):
        return "%s, %s" % (self.platform, self.os_version)


class DeviceResolutionDimManager(models.Manager):

    def get_or_create_by_orig_resolution(self, orig_resolution):
        rd = self.model()
        rd.standard_resolution = orig_resolution
        return self.get_or_create(orig_resolution=rd.orig_resolution,
                           defaults=dict(
                               orig_resolution=rd.orig_resolution,
                               resolution=rd.resolution,
                               orig_width=rd.orig_width,
                               orig_height=rd.orig_height,
                               width=rd.width,
                               height=rd.height
                           ))


class DeviceResolutionDim(Dimension):
    """
    设备分辨率
    """

    objects = DeviceResolutionDimManager()

    resolution = models.CharField(max_length=25,
                                  db_index=True,
                                  default=UNDEFINED)

    orig_resolution = models.CharField(max_length=25,
                                       db_index=True,
                                       unique=True,
                                       default=UNDEFINED)

    orig_width = models.CharField(max_length=10,
                                  default=UNDEFINED)

    orig_height = models.CharField(max_length=10,
                                   default=UNDEFINED)

    width = models.CharField(max_length=10,
                             default=UNDEFINED)

    height = models.CharField(max_length=10,
                              default=UNDEFINED)

    class Meta:
        db_table = 'dim_deviceresolution'
        index_together = (
            ('width', 'height'),
            ('orig_width', 'orig_height'),
        )
        verbose_name = '设备分辨率'
        verbose_name_plural = '设备分辨率列表'

    def _get_resolution(self):
        if not all((self.width, self.height)) \
            or UNDEFINED in (self.width, self.height):
            return UNDEFINED
        return "%sx%s" % (self.width, self.height)

    def _set_resolution(self, orig_resolution):
        try:
            self.orig_width, self.orig_height = orig_resolution.split("x")
            self.width = min(self.orig_width, self.orig_height)
            self.height = max(self.orig_width, self.orig_height)
        except (ValueError, TypeError) as e:
            self.orig_width = self.orig_height = UNDEFINED
            self.width = self.height = UNDEFINED

        self.resolution = self._get_resolution()
        self.orig_resolution = self._get_orig_resolution()

    def _get_orig_resolution(self):
        if not all((self.orig_width, self.orig_height)) \
            or UNDEFINED in (self.orig_width, self.orig_height):
            return UNDEFINED
        return "%sx%s" % (self.orig_width, self.orig_height)

    standard_resolution = property(_get_resolution, _set_resolution)

    def __str__(self):
        return self.resolution


class DeviceModelDim(Dimension):
    """
    设备类型
    """

    manufacturer = models.CharField(max_length=300, db_index=True)

    device_name = models.CharField(max_length=255, default='')

    module_name = models.CharField(max_length=255, default='')

    model_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'dim_devicemodel'
        unique_together = (
            ('manufacturer', 'device_name', 'module_name', 'model_name'),
        )

    def __str__(self):
        return self.model_name


class DeviceSupplierDim(Dimension):
    """
    运营商
    """

    name = models.CharField(max_length=60,
                            blank=True,
                            default='unknown')

    # mcc and mnc
    mccmnc = models.CharField(max_length=16,
                              unique=True,
                              default=UNDEFINED)

    # mcc
    country_code = models.CharField(max_length=10,
                                    db_index=True,
                                    default=UNDEFINED)

    country_name = models.CharField(max_length=128,
                                    default='unknown')

    class Meta:
        db_table = 'dim_devicesupplier'

    def __str__(self):
        return self.mccmnc


class DeviceLanguageDim(Dimension):
    """
    设备语言
    """

    language = models.CharField(max_length=15,
                                default=UNDEFINED,
                                blank=True,
                                db_index=True)

    class Meta:
        db_table = 'dim_devicelanguage'
        verbose_name = '设备语言'
        verbose_name_plural = '设备语言列表'

    def __str__(self):
        return self.language


class NetworkDim(Dimension):
    """
    网络类型
    """

    network = models.CharField(max_length=20,
                               db_index=True,
                               blank=True,
                               default=UNDEFINED)

    class Meta:
        db_table = 'dim_network'
        verbose_name = '网络类型'
        verbose_name_plural = '网络类型列表'

    def __str__(self):
        return self.network


class BaseUrlDim(Dimension):

    urlvalue = models.CharField(max_length=1024,
                                blank=True,
                                unique=True,
                                default=UNDEFINED)

    host = models.CharField(max_length=150,
                            db_index=True,
                            default='')

    path = models.CharField(max_length=500,
                            default='')

    query = models.CharField(max_length=500,
                             default='')

    def _get_page(self):
        return self.urlvalue

    def _set_page(self, url):
        from urllib.parse import urlparse, urlunparse
        part = urlparse(url)
        self.host = urlunparse(list(part)[0:2] + ['']*4)
        self.path = part.path
        self.query = part.query
        self.urlvalue = url

    page_url = property(_get_page, _set_page)

    class Meta:
        abstract = True

    def __str__(self):
        return self.page_name


class PageDim(BaseUrlDim):
    """
    页面
    """

    def _get_page_name(self):
        return self.urlvalue

    def _set_page_name(self, val):
        self.urlvalue = val

    page_name = property(_get_page_name, _set_page_name)

    is_url = models.BooleanField(blank=True,
                                 db_index=True,
                                 default=False)

    class Meta:
        db_table = 'dim_page'
        index_together = (
            ('host', 'path', ),
        )
        verbose_name = '页面'
        verbose_name_plural = '页面列表'


class MediaUrlDimManager(models.Manager):

    def get_or_create_by_page_url(self, page_url, is_static=False):
        inst = self.model()
        inst.page_url = page_url
        defaults = deepcopy(inst.__dict__)
        defaults['is_static'] = is_static
        del defaults['_state']
        return self.get_or_create(urlvalue=inst.urlvalue, defaults=defaults)


class MediaUrlDim(BaseUrlDim):

    objects = MediaUrlDimManager()

    is_static = models.BooleanField(default=False)

    class Meta:
        db_table = 'dim_downloadurl'
        index_together = (
            ('host', 'path', ),
        )
        verbose_name = '资源地址'
        verbose_name_plural = '资源地址列表'

    def __str__(self):
        return self.urlvalue


class LocationDim(Dimension):
    """
    地理位置
    """

    country = models.CharField(max_length=60,
                               db_index=True,
                               default=UNDEFINED)

    region = models.CharField(max_length=60,
                              db_index=True,
                              default=UNDEFINED)

    city = models.CharField(max_length=60,
                            db_index=True,
                            default=UNDEFINED)

    class Meta:
        db_table = 'dim_location'
        unique_together = (
            ('country', 'region', 'city')
        )
        verbose_name = '地理位置'
        verbose_name_plural = '地址位置列表'


class UsinglogSegmentDimManager(models.Manager):

    def create_segments_between(self, min_seconds, max_seconds, step=60):
        assert min_seconds >= 0
        assert min_seconds < max_seconds
        segments = list()
        i = 0
        while True:
            next_start = min_seconds + step * i
            next_end = min_seconds + step * (i + 1)
            if next_end > max_seconds:
                break
            inst = self.model(startsecond=next_start,
                       endsecond=next_end)
            segments.append(inst)
            i += 1
        self.model.bulk_create(*segments)

        return segments


class UsinglogSegmentDim(Dimension):
    """
    使用时长
    """

    objects = UsinglogSegmentDimManager()

    name = models.CharField(max_length=50, default=UNDEFINED)

    startsecond = models.PositiveIntegerField(max_length=10)

    endsecond = models.PositiveIntegerField(max_length=10)

    effective_date = models.DateField(blank=True, null=True)

    expiry_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'dim_usinglogsegment'
        verbose_name = '使用时长'
        verbose_name_plural = '使用时长列表'

    def clean(self):
        if self.endsecond <= self.startsecond:
            raise ValidationError('endsecond must great than startsecond:'
                                  'start: %s, end: %s' %(self.startsecond,
                                                         self.endsecond))

    def __str__(self):
        return "%s-%s" %(self.startsecond, self.endsecond)


class UsingcountSegmentDim(Dimension):

    name = models.CharField(max_length=50, default=UNDEFINED)

    startcount = models.PositiveIntegerField(max_length=10)

    endcount = models.PositiveIntegerField(max_length=10)

    class Meta:
        db_table = 'dim_usingcountsegment'
        verbose_name = '使用次数'
        verbose_name_plural = '使用次数列表'

    def clean(self):
        if self.endcount <= self.startcount:
            raise ValidationError('endcount must great than startcount:'
                                  'start: %s, end: %s' %(self.startcount,
                                                         self.endcount))

    def __str__(self):
        return "%s-%s" %(self.startcount, self.endcount)


class BaiduPushDim(Dimension):
    """
    百度推送
    """

    channel_id = models.CharField(max_length=25,
                                  db_index=True,
                                  blank=True,
                                  default=UNDEFINED)

    user_id = models.CharField(max_length=25,
                               default=UNDEFINED,
                               blank=True,
                               db_index=True)

    app_id = models.CharField(max_length=25,
                              db_index=True,
                              blank=True,
                              default=UNDEFINED)

    class Meta:
        db_table = 'dim_baidupush'

        unique_together = (
            ('channel_id', 'user_id', 'app_id')
        )

    def __str__(self):
        return "%s %s %s" %(self.channel_id, self.user_id, self.app_id)


# Facts
class Fact(models.Model):

    class Meta:
        abstract = True

    productkey = models.ForeignKey(ProductKeyDim,
                                   null=True,
                                   blank=True)

    product = models.ForeignKey(ProductDim)

    packagekey = models.ForeignKey(PackageKeyDim,
                                   null=True,
                                   blank=True)

    package = models.ForeignKey(PackageDim)

    device = models.ForeignKey(DeviceDim)

    date = models.ForeignKey(DateDim)

    hour = models.ForeignKey(HourDim)

    device_os = models.ForeignKey(DeviceOSDim)

    device_platform = models.ForeignKey(DevicePlatformDim)

    device_resolution = models.ForeignKey(DeviceResolutionDim)

    device_model = models.ForeignKey(DeviceModelDim)

    device_language = models.ForeignKey(DeviceLanguageDim)


class EventFact(Fact):

    class Meta:
        abstract = True

    doc_id = models.CharField(max_length=40, unique=True)

    event = models.ForeignKey(EventDim)

    subscriberid = models.ForeignKey(SubscriberIdDim)

    device_supplier = models.ForeignKey(DeviceSupplierDim)

    referer = models.ForeignKey(PageDim, related_name='+',
                                blank=True,
                                null=True)

    page = models.ForeignKey(PageDim, related_name='+',
                             blank=True,
                             null=True)

    location = models.ForeignKey(LocationDim, related_name='+',
                                 blank=True,
                                 null=True)

    network = models.ForeignKey(NetworkDim)

    baidu_push = models.ForeignKey(BaiduPushDim,
                                   related_name='+',
                                   blank=True,
                                   null=True)

    created_datetime = models.DateTimeField()

    @property
    def doc(self):
        if hasattr(self, '_doc'):
            return self._doc
        self._doc = Event.objects.get(pk=ObjectId(self.doc_id))
        return self._doc

    @doc.setter
    def doc(self, doc):
        self.doc_id = doc.pk
        self._doc = doc

    def event_from_doc(self, doc):
        self.event = EventDim.objects.get(eventtype=doc.get('eventtype'))

    def subscriberid_from_doc(self, doc):
        self.subscriberid = SubscriberIdDim.objects.get(imsi=doc.get('imsi') or UNDEFINED)

    def network_from_doc(self, doc):
        self.network = NetworkDim.objects\
            .get(network=doc.get('network') or UNDEFINED)

    def page_from_doc(self, doc):
        page_name = doc.get('current_uri') or doc.get('page_name') or UNDEFINED
        self.page = PageDim.objects.get(urlvalue=page_name)

    def referer_from_doc(self, doc):
        page_name = doc.get('referer') or UNDEFINED
        self.referer = PageDim.objects.get(urlvalue=page_name)

    def product_from_doc(self, doc):
        entrytype = doc.get('entrytype')
        productkey, created = ProductKeyDim.objects\
            .get_or_create(entrytype=entrytype,
                           defaults=dict(entrytype=entrytype))
        self.productkey = productkey
        self.product = ProductDim.objects\
            .get(entrytype=doc.get('entrytype'),
                 channel=doc.get('channel') or UNDEFINED)

    def package_from_doc(self, doc):
        platform = doc.get('platform') or PLATFORM_DEFAULT
        self.package = PackageDim.objects\
            .get(platform=platform,
                 package_name=doc.get('package_name') or UNDEFINED,
                 version_name=doc.get('version_name') or UNDEFINED)
        self.packagekey, created = PackageKeyDim.objects\
            .get_or_create_from_package_dim(self.package)

    def device_from_doc(self, doc):
        self.device = DeviceDim.objects.get(imei=doc.get('imei') or UNDEFINED)

    def device_os_from_doc(self, doc):
        self.device_os = DeviceOSDim.objects\
            .get(platform=doc.get('platform') or PLATFORM_DEFAULT,
                 os_version=doc.get('os_version') or UNDEFINED)

    def device_platform_from_doc(self, doc):
        self.device_platform = DevicePlatformDim.objects\
            .get(platform=doc.get('platform') or PLATFORM_DEFAULT)

    def device_supplier_from_doc(self, doc):
        cell = doc.get('cell', dict())
        mnc = cell.get('mnc')
        mcc = cell.get('mcc') or UNDEFINED
        if str(mnc).isnumeric():
            mnc = "%02d" % int(mnc)
        if UNDEFINED in (mnc, mcc):
            mccmnc = UNDEFINED
        else:
            mccmnc = "%s%s" % (mcc, mnc)
        self.device_supplier = DeviceSupplierDim.objects.get(mccmnc=mccmnc)

    def device_language_from_doc(self, doc):
        self.device_language = DeviceLanguageDim.objects\
            .get(language=doc.get('language') or UNDEFINED)

    def device_resolution_from_doc(self, doc):
        self.device_resolution = DeviceResolutionDim.objects\
            .get(orig_resolution=doc.get('resolution') or UNDEFINED)

    def device_model_from_doc(self, doc):
        self.device_model = DeviceModelDim.objects \
            .get(manufacturer=doc.get('manufacturer') or UNDEFINED,
                 device_name=doc.get('device_name') or UNDEFINED,
                 module_name=doc.get('module_name') or UNDEFINED,
                 model_name=doc.get('model_name') or UNDEFINED)

    def datehour_from_doc(self):
        dateval = self.fact_created_datetime()
        self.date = DateDim.objects\
            .get(year=dateval.year, month=dateval.month, day=dateval.day)
        self.hour = HourDim.objects.get(hour=dateval.hour)
        self.created_datetime = dateval

    def fact_created_datetime(self):
        return self.doc.created_datetime.replace(tzinfo=utc).astimezone()

    def baidu_push_from_doc(self, doc):
        self.baidu_push = BaiduPushDim.objects \
            .get(channel_id=doc.get('baidu_push_channel_id') or UNDEFINED,
                 user_id=doc.get('baidu_push_user_id') or UNDEFINED,
                 app_id=doc.get('baidu_push_app_id') or UNDEFINED)

    def transform_from_doc(self):
        doc = dictdata_strip_val(self.doc._data)
        self.event_from_doc(doc)
        self.product_from_doc(doc)
        self.package_from_doc(doc)
        self.subscriberid_from_doc(doc)
        self.device_from_doc(doc)
        self.device_os_from_doc(doc)
        self.device_model_from_doc(doc)
        self.device_supplier_from_doc(doc)
        self.device_platform_from_doc(doc)
        self.device_resolution_from_doc(doc)
        self.device_language_from_doc(doc)
        self.network_from_doc(doc)
        self.page_from_doc(doc)
        self.referer_from_doc(doc)
        self.baidu_push_from_doc(doc)
        self.datehour_from_doc()


class CreateFactByDocManagerMixin(object):

    def create_by_doc(self, doc):
        fact = self.model()
        fact.doc = doc
        fact.transform_from_doc()
        fact.save()
        return fact


class UsinglogFactManager(CreateFactByDocManagerMixin,
                          PassThroughManager):

    def find_open_event_by(self, close_fact):
        """
        if close_fact.event.eventtype != 'close':
            raise ValidationError('close_fact must be close eventtype '
                                  'but get %s' % close_fact.event.eventtype)
        """
        if not hasattr(self, '_open_event'):
            self._open_event = EventDim.objects.get(eventtype='open')

        min_start_datetime = close_fact.created_datetime - timedelta(days=1)
        qs = self.filter(device=close_fact.device,
                         event=self._open_event,
                         product=close_fact.product,
                         package=close_fact.package)\
            .filter(created_datetime__lte=close_fact.created_datetime)\
            .filter(created_datetime__gt=min_start_datetime)\
            .order_by('-created_datetime')
        try:
            open_fact = qs[0]
        except IndexError:
            raise UsinglogFact.DoesNotExist()
        return open_fact


class CreateFactByUsinglogFactManagerMixin(object):

    def create_by_usinglogfact(self, usinglog):
        fact = self.model(usinglog=usinglog)
        fact.transform_from_usinglog()
        fact.save()
        return fact


class UsinglogFactQuerySet(QuerySet):

    def in_days(self, datedims):
        return self.filter(date__in=datedims)

    def activate(self):
        events = ['open', 'activate']
        return self.filter(event__eventtype__in=events)

    def openclose(self):
        events = ['open', 'close']
        return self.filter(event__eventtype__in=events)

    def download(self):
        events = ['download', 'downloaded']
        return self.filter(event__eventtype__in=events)

    def by_product(self, entrytype):
        return self.filter(product__entrytype=entrytype)


class UsinglogFact(EventFact):
    """
    用户行为事实(所有(多次)操作行为，含下载)
        eventtype [activate, open, close, click, download, downloaded ...]
    """

    objects = UsinglogFactManager.for_queryset_class(UsinglogFactQuerySet)()

    class Meta:
        verbose_name = '事实日志 所有活动'
        verbose_name_plural = '事实日志 所有活动列表'
        db_table = 'fact_behaviour'
        index_together = (
            ('package', 'date', ),
            ('package', 'date', 'event', ),
            ('product', 'date'),
            ('product', 'date', 'event', ),
            ('event', 'product', 'device', 'package', 'date', ),
            ('event', 'product', 'device', 'package', 'created_datetime', ),

            ('packagekey', 'date', ),
            ('packagekey', 'date', 'event', ),
            ('productkey', 'date', ),
            ('productkey', 'date', 'event', ),
            ('event', 'productkey', 'device', 'packagekey', 'date', ),
            ('event', 'productkey', 'device', 'packagekey', 'created_datetime', ),
        )
        ordering = ('-date', )


def copy_model_instance(from_, to_):
    for k, v in from_.__dict__.items():
        if not k.startswith('_') and \
                        k != 'id' and k in to_.__dict__:
            to_.__dict__[k] = deepcopy(v)
    return to_


class OpenCloseDailyFactManager(models.Manager):

    def create_by_usinglogfact(self, start_usinglog, end_usinglog):
        fact = self.model()
        fact = copy_model_instance(start_usinglog, fact)
        fact.extract_from(start_usinglog, end_usinglog)
        fact.save()
        return fact


class OpenCloseDailyFact(Fact):
    """
#    每日打开关闭间使用时间事实
#        由BehaviourFact数据再次压缩处理
#        eventtype [open, close]
    """

    objects = OpenCloseDailyFactManager()

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    segment = models.ForeignKey(UsinglogSegmentDim)

    duration = models.PositiveIntegerField(default=0)

    start_usinglog = models.ForeignKey(UsinglogFact,
                                       unique=True,
                                       related_name='+')

    end_usinglog = models.ForeignKey(UsinglogFact,
                                     unique=True,
                                     related_name='+')

    class Meta:
        db_table = 'fact_openclose_daily'
        verbose_name = '事实日志 打开关闭'
        verbose_name_plural = '事实日志 打开关闭列表'
        unique_together = (
            ('start_usinglog', 'end_usinglog'),
        )
        index_together = (
            ('product', 'date', 'segment'),
            ('product', 'package', 'date', 'segment'),
            ('package', 'device', 'date', 'segment'),
        )

    def extract_from(self, start_usinglog, end_usinglog):
        self.start_usinglog = start_usinglog
        self.end_usinglog = end_usinglog
        self.start_datetime = start_usinglog.fact_created_datetime()
        self.end_datetime = end_usinglog.fact_created_datetime()
        td = self.end_datetime - self.start_datetime
        self.duration = td.total_seconds()

        qs = UsinglogSegmentDim.objects \
            .filter(startsecond__lte=self.duration,
                    endsecond__gt=self.duration) \
            .order_by('-startsecond')
        try:
            segment = qs[0]
        except IndexError:
            raise UsinglogSegmentDim.DoesNotExist()
        self.segment = segment


class ActivateFactQuerySet(QuerySet):

    def in_days(self, datedims):
        return self.filter(date__in=datedims)


class ActivateFactManager(CreateFactByUsinglogFactManagerMixin,
                          PassThroughManager):

    def check_is_new_device(self, activate, **queries):
        """
            ActivateFact.objects\
                .check_new_activate_device(inst, productkey=inst.productkey)
            返回true,代表是新的激活<imei-productkey>数

            ActivateFact.objects\
                .check_new_activate_status(inst, product__channel=inst.product.channel)
            返回true,代表是新的激活<imei-product.channel>数
        """
        _queries = dict(device=activate.device,
                        created_datetime__lte=activate.created_datetime)
        queries = dict(filter(lambda x: x[0] not in _queries, queries.items()))
        _queries.update(queries)

        qs = self.get_query_set()
        if activate.pk:
            qs = qs.exclude(pk=activate.pk)
        return not qs.filter(**_queries).exists()


class ActivateFact(EventFact):
    """
    用户活跃事实(多次open, activate的事件)
        eventtype [open, activate]
    """

    objects = ActivateFactManager.for_queryset_class(ActivateFactQuerySet)()

    usinglog = models.ForeignKey(UsinglogFact, unique=True, related_name='+')

    class Meta:
        verbose_name = '事实日志 开启活动'
        verbose_name_plural = '事实日志 开启活动列表'
        db_table = 'fact_activate'

        index_together = (
            ('device', 'date', ),
            ('package', 'date', ),
            ('device', 'package', 'date'),

            ('product', 'device'),
            ('product', 'device', 'package'),
            ('productkey', 'device'),
            ('productkey', 'packagekey'),
            ('productkey', 'device', 'packagekey'),
            ('productkey', 'package'),
            ('productkey', 'device', 'package'),

            ('device_platform', 'package', 'date', ),
            ('device_platform', 'device', 'package', 'date'),
            ('device_platform', 'product', 'device'),
            ('device_platform', 'product', 'device', 'package'),
            ('device_platform', 'productkey', 'device'),
            ('device_platform', 'productkey', 'packagekey'),
            ('device_platform', 'productkey', 'device', 'packagekey'),
            ('device_platform', 'productkey', 'package'),
            ('device_platform', 'productkey', 'device', 'package'),
        )
        ordering = ('-date', )

    def transform_from_usinglog(self):
        copy_model_instance(self.usinglog, self)


class ReserveBooleanField(models.BooleanField):

    group_fields = None

    cube_fields = None

    sum_fields = None

    def __init__(self, *args, **kwargs):
        try:
            self.group_fields = kwargs.pop('group_fields')
        except:
            self.group_fields = list()
        try:
            self.cube_fields = kwargs.pop('cube_fields')
        except:
            self.cube_fields = list()
        try:
            self.sum_fields = kwargs.pop('sum_fields')
        except:
            self.sum_fields = list()
        super(ReserveBooleanField, self).__init__(*args, **kwargs)


class ActivateNewReserveFactManager(ActivateFactManager):

    def _fetch_reserve_fields(self):
        if not hasattr(self, '_reserve_fields'):
            fields = self.model._meta.fields
            reserve_fields = list()
            for field in fields:
                if isinstance(field, ReserveBooleanField):
                    reserve_fields.append(field)
            self._reserve_fields = reserve_fields
        return self._reserve_fields

    def check_all_new_status(self, inst):
        statuses = dict()
        for field in self._fetch_reserve_fields():
            queries = {k: getattr(inst, k) for k in field.group_fields}
            statuses[field.name] = self.check_is_new_device(inst, **queries)
        return statuses

    @property
    def reserve_fields(self):
        return self._fetch_reserve_fields()


class ActivateNewReserveFactQuerySet(QuerySet):

    def in_days(self, datedims):
        return self.filter(date__in=datedims)

    def reserve_device_values(self, *fields, **flags):
        """
            激活数查询
              fields不能包括device统计单位
              flags激活的标识条件

            1.  productkey, is_new_product=True 产品的用户激活数查询
                result = ActivateNewReserveFact.objects.in_days(datedims)
                        .reserve_values('productkey', is_new_product=True)
                item = result[0]
                productkey_id = item['productkey']
                reserve_cnt = item['cnt']


            2.  productkey, packagekey, is_new_product_package=True 产品下应用的用户激活数查询
                result = ActivateNewReserveFact.objects.in_days(datedims)
                        .reserve_values('productkey', 'packagekey',
                                         is_new_product_package=True)
                item = result[0]
                productkey_id = item['productkey']
                packagekey_id = item['packagekey']
                reserve_cnt = item['cnt']

        """
        if 'device' in fields:
            fields = list(filter(lambda x: x != 'device', fields))

        return self.filter(**flags) \
            .values(*fields).order_by(*fields).annotate(cnt=Count('id'))

    def active_device_values(self, *fields):
        """
            活跃数查询
              fields需要加入device作为汇总的统计单位

            1.  productkey, device 产品的设备活跃数查询
                result = ActivateNewReserveFact.objects.in_days(datedims)
                        .active_values('productkey', 'device')
                productkey_id = item['productkey']
                active_cnt = item['cnt']

            2.  productkey, packagekey, device 产品-应用的设备活跃数查询
                result = ActivateNewReserveFact.objects.in_days(datedims)
                        .active_values('productkey', 'packagekey', 'device')
                item = result[0]
                productkey_id = item['productkey']
                packagekey_id = item['packagekey']
                reserve_cnt = item['cnt']

        """
        if 'device' not in fields:
            fields = list(filter(lambda x: x != 'device', fields))
        return self.values(*fields).order_by(*fields)\
            .annotate(cnt=Count('device', distinct=True))

    def open_values(self, *fields):
        """
            启动次数查询
            1. 产品的启动次数查询
                result = self.open_values('productkey')
                item = result[0]
                productkey_id = item['productkey']
                open_cnt = item['cnt']

            2. 产品下的应用启动次数查询
                result = self.open_values('productkey', 'packagekey')
                item = result[0]
                productkey_id = item['productkey']
                packagekey_id = item['packagekey']
                open_cnt = item['cnt']

            2. 产品下的应用版本启动次数查询
                result = self.open_values('productkey', 'package')
                item = result[0]
                productkey_id = item['productkey']
                package_id = item['package']
                open_cnt = item['cnt']
        """
        return self.values(*fields).order_by(*fields).annotate(cnt=Count('id'))


class ActivateNewReserveFact(ActivateFact):

    objects = ActivateNewReserveFactManager\
        .for_queryset_class(ActivateNewReserveFactQuerySet)()

    platform = models.ForeignKey(DevicePlatformDim,
                                 null=True)

    # 产品 新增
    is_new_product = ReserveBooleanField(
        verbose_name='产品 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey'),
        cube_fields=('device_platform', 'productkey'),
        group_fields=('device', 'device_platform', 'productkey')
    )

    # 产品-渠道 新增
    is_new_product_channel = ReserveBooleanField(
        verbose_name='产品-渠道 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey', 'product'),
        cube_fields=('device_platform', 'productkey', 'product'),
        group_fields=('device', 'device_platform', 'product')
    )

    # 产品-渠道-package 新增
    is_new_product_channel_package = ReserveBooleanField(
        verbose_name='产品-渠道-package 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey', 'product'),
        cube_fields=('device_platform', 'productkey', 'product', 'packagekey'),
        group_fields=('device', 'device_platform', 'product', 'packagekey')
    )

    # 产品-渠道-packge-version 新增
    is_new_product_channel_package_version = ReserveBooleanField(
        verbose_name='产品-渠道-package-version 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey', 'product'),
        cube_fields=('device_platform', 'productkey', 'product', 'packagekey', 'package'),
        group_fields=('device', 'device_platform', 'product', 'package')
    )

    # 产品-package_name 新增
    is_new_product_package = ReserveBooleanField(
        verbose_name='产品-package 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey'),
        cube_fields=('device_platform', 'productkey', 'packagekey'),
        group_fields=('device', 'device_platform', 'productkey', 'packagekey')
    )

    # 产品-package-version 新增
    is_new_product_package_version = ReserveBooleanField(
        verbose_name='产品-package-version 新增',
        default=False, db_index=True,
        sum_fields=('device_platform', 'productkey', ),
        cube_fields=('device_platform', 'productkey', 'package'),
        group_fields=('device', 'device_platform', 'productkey', 'package')
    )

    # 应用 新增
    is_new_package = ReserveBooleanField(
        verbose_name='package 新增',
        default=False, db_index=True,
        cube_fields=('device_platform', 'packagekey'),
        group_fields=('device', 'device_platform', 'packagekey')
    )

    # 应用-版本 新增
    is_new_package_version = ReserveBooleanField(
        verbose_name='package-version 新增',
        default=False, db_index=True,
        cube_fields=('device_platform', 'packagekey', 'package'),
        group_fields=('device', 'device_platform', 'package')
    )

    class Meta:
        db_table = 'fact_activate_newreserve'
        verbose_name = '事实日志 开启日志<新激活>'
        verbose_name_plural = '事实日志 开启日志<新激活>列表'
        index_together = (
            ('platform', 'is_new_product'),
            ('platform', 'is_new_product_channel'),
            ('platform', 'is_new_product_channel_package'),
            ('platform', 'is_new_product_channel_package_version'),
            ('platform', 'is_new_product_package'),
            ('platform', 'is_new_product_package_version'),

            ('platform', 'is_new_package'),
            ('platform', 'is_new_package_version'),
        )

    def _set_new_status(self, statuses):
        for f, v in statuses.items():
            setattr(self, f, v)

    def _fill_key(self):
        if not self.productkey:
            _defaults = dict(entrytype=self.product.entrytype)
            self.productkey, created = ProductKeyDim.objects \
                .get_or_create(defaults=_defaults, **_defaults)
        if not self.packagekey:
            self.packagekey, created = PackageKeyDim.objects\
                .get_or_create_from_package_dim(self.package)

    def transform_from_usinglog(self):
        copy_model_instance(self.usinglog, self)
        self._fill_key()
        self.platform = self.device_platform
        statuses = self.__class__.objects.check_all_new_status(self)
        self._set_new_status(statuses)


class DownloadFactQuerySet(QuerySet):

    def download_values(self, *fields):
        _fields = list(deepcopy(fields))
        if 'event' not in fields:
            _fields[0:0] = ['event']
        return self.values(*_fields).order_by(*_fields).annotate(cnt=Count('id'))

    def in_days(self, datedims):
        return self.filter(date__in=datedims)


class DownloadFactManager(CreateFactByUsinglogFactManagerMixin,
                          PassThroughManager):

    def find_start_by(self, end_fact):
        """
        if end_fact.event.eventtype != 'downloaded':
            raise ValidationError('end_fact must be downloaded eventtype '
                                  'but get %s' % end_fact.event.eventtype)
        """
        if not hasattr(self, '_start_event'):
            self._start_event = EventDim.objects.get(eventtype='download')

        min_start_datetime = end_fact.created_datetime - timedelta(days=1)
        qs = self.filter(device=end_fact.device,
                                 event=self._start_event,
                                 product=end_fact.product,
                                 package=end_fact.package,
                                 download_package=end_fact.download_package,
                                 download_url=end_fact.download_url,
                                 redirect_to=end_fact.redirect_to). \
            filter(created_datetime__lte=end_fact.created_datetime). \
            filter(created_datetime__gt=min_start_datetime). \
            order_by('-created_datetime')
        try:
            start_fact = qs[0]
        except IndexError:
            raise DownloadFact.DoesNotExist()
        return start_fact

    def find_downloads_by_dimensions(self,
                                     product,
                                     package,
                                     download_package,
                                     date):
        qs = self.filter(product=product,
                                package=package,
                                download_package=download_package,
                                date=date,
                                ) \
            .order_by('-created_datetime')
        try:
            open_fact = qs[0]
        except IndexError:
            raise DownloadFact.DoesNotExist()
        return open_fact

    def download_stats_by_dimensions(self, product, package,
                                     download_package, date):
        if not hasattr(self, '_start_event'):
            self._start_event = EventDim.objects.get(eventtype='download')
        if not hasattr(self, '_end_event'):
            self._end_event = EventDim.objects.get(eventtype='downloaded')

        qs = self.extra(select={
            'download_count': 'COUNT(event_id == %s )' % self._start_event.pk,
            'downloaded_count': 'COUNT(event_id == %s )' % self._end_event.pk,
        })
        qs = self.distinct('product', 'package', 'download_package', 'date')
        return qs


class DownloadFact(EventFact):

    objects = DownloadFactManager.for_queryset_class(DownloadFactQuerySet)()

    usinglog = models.ForeignKey(UsinglogFact, unique=True, related_name='+')

    download_package = models.ForeignKey(PackageDim,
                                         related_name='+',
                                         default=None,
                                         blank=True,
                                         null=True)

    download_packagekey = models.ForeignKey(PackageKeyDim,
                                            related_name='+',
                                            default=None,
                                            blank=True,
                                            null=True)

    download_url = models.ForeignKey(MediaUrlDim, related_name='+')

    redirect_to = models.ForeignKey(MediaUrlDim,
                                    related_name='+',
                                    default=None,
                                    blank=True,
                                    null=True)

    class Meta:
        db_table = 'fact_download'
        index_together = (
            ('download_package', 'date', ),
            ('download_packagekey', 'date', ),
            ('package', 'date', ),
            ('packagekey', 'date', ),
            ('event', 'package', 'date'),
            ('event', 'packagekey', 'date'),
            ('event', 'product', 'device', 'package', 'download_package', 'date',),
            ('event', 'product', 'device', 'package', 'download_package', 'created_datetime',),
            ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date',),
            ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime',),
            ('event', 'productkey'),
            ('event', 'product'),

        #    ('event', 'device_platform', 'productkey', 'packagekey'),
        #    ('event', 'device_platform', 'productkey', 'packagekey', 'date'),
        #    ('event', 'device_platform', 'productkey', 'packagekey', 'package'),
        #    ('event', 'device_platform', 'productkey', 'packagekey', 'package', 'date'),
        #    ('event', 'device_platform', 'productkey', 'download_package'),
        #    ('event', 'device_platform', 'productkey', 'download_package', 'date'),
        #    ('event', 'device_platform', 'productkey', 'download_packagekey'),
        #    ('event', 'device_platform', 'productkey', 'download_packagekey', 'date'),

        #    ('event', 'device_platform', 'productkey', 'product', 'packagekey'),
        #    ('event', 'device_platform', 'productkey', 'product', 'packagekey', 'date'),
        #    ('event', 'device_platform', 'productkey', 'product', 'packagekey', 'package'),
        #    ('event', 'device_platform', 'productkey', 'product', 'packagekey', 'package', 'date'),
        #    ('event', 'device_platform', 'productkey', 'product', 'download_packagekey'),
        #    ('event', 'device_platform', 'productkey', 'product', 'download_packagekey', 'date'),
        #    ('event', 'device_platform', 'productkey', 'product', 'download_packagekey', 'download_package'),
        #    ('event', 'device_platform', 'productkey', 'product', 'download_packagekey', 'download_package', 'date'),
        )

    def transform_from_usinglog(self):
        copy_model_instance(self.usinglog, self)
        self.download_dim_from_page()

    def download_dim_from_page(self):
        self.download_url, created = MediaUrlDim.objects\
            .get_or_create_by_page_url(page_url=self.page.urlvalue)
        doc_data = self.doc._data
        if 'redirect_to' in doc_data:
            redirect_to = str(self.doc.redirect_to).strip()
            self.redirect_to, created = MediaUrlDim.objects\
                .get_or_create_by_page_url(page_url=redirect_to, is_static=True)

        if 'download_package_name' in doc_data:
            self.fill_download_package_by_doc(doc_data)
        else:
            self.fill_download_package_by_url(self.download_url)

    def fill_download_package_by_doc(self, doc_data):
        package_name = doc_data.get('download_package_name') or UNDEFINED
        package_name = package_name.strip('"').strip()
        version_name = doc_data.get('download_version_name') or UNDEFINED
        version_name = version_name.strip()
        self.download_package = PackageDim.objects \
            .get(platform=self.device_platform.platform,
                 package_name=package_name,
                 version_name=version_name)
        self.download_packagekey, pk_created = PackageKeyDim.objects \
            .get_or_create_from_package_dim(self.download_package)

    def fill_download_package_by_url(self, url_dim):
        pv_names = self.get_download_packageversion_by_urlpath(url_dim.path)
        if not pv_names:
            return
        package_name, version_name = pv_names
        try:
            dw_pkg, created = PackageDim.objects \
                .get_or_create(platform=self.device_platform.platform,
                               package_name=package_name,
                               version_name=version_name)
            if created:
                dw_pkg = packagecategorydim_fill_to(dw_pkg)
                dw_pkg = packageversion_id_fill(dw_pkg)
                dw_pkg.save()
            self.download_package = dw_pkg
            self.download_packagekey, created = PackageKeyDim.objects \
                .get_or_create_from_package_dim(self.download_package)
        except ObjectDoesNotExist:
            logger.error(pv_names)
            logger.error("%s %s %s"% (self.device_platform.platform,
                                      package_name,
                                      version_name))
            raise

    def get_download_packageversion_by_urlpath(self, path):
        package_name = version_name = UNDEFINED
        if not path:
            return package_name, version_name
        try:
            resolver_match = resolve(path)
        except Resolver404:
            return package_name, version_name

        from warehouse.models import PackageVersion
        pk = resolver_match.kwargs.get('pk')
        if resolver_match.url_name == 'download_packageversion':
            try:
                version = PackageVersion.objects.get(pk=pk)
                package_name = version.package.package_name
                version_name = version.version_name
            except PackageVersion.DoesNotExist:
                return None
        else:
            return None

        return package_name, version_name


class DownloadBeginFinishManager(models.Manager):

    def create_by_download(self, begin_download, finish_download):
        fact = copy_model_instance(begin_download, self.model())
        fact.extract_from(begin_download, finish_download)
        fact.save()
        return fact


class DownloadBeginFinishFact(Fact):

    objects = DownloadFactManager()

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    segment = models.ForeignKey(UsinglogSegmentDim)

    duration = models.PositiveIntegerField(default=0)

    download_package = models.ForeignKey(PackageDim, related_name='+')

    download_url = models.ForeignKey(MediaUrlDim, related_name='+')

    redirect_to = models.ForeignKey(MediaUrlDim, related_name='+')

    start_download = models.ForeignKey(DownloadFact,
                                       unique=True,
                                       related_name='+')

    end_download = models.ForeignKey(DownloadFact,
                                        unique=True,
                                        related_name='+')

    class Meta:
        db_table = 'fact_downloadbeginfinish'
        unique_together = (
            ('start_download', 'end_download', ),
        )
        index_together = (
            ('download_package', 'date', ),
            ('package', 'date'),
            ('product', 'device', 'package', 'download_package', 'date',),
            ('product', 'device', 'download_package', 'date',),
            ('product', 'device', 'package', 'date'),
        )

    def extract_from_download(self, start_download, end_download):
        self.start_download = start_download
        self.end_download = end_download
        self.start_datetime = start_download.created_datetime
        self.end_datetime = end_download.created_datetime
        td = self.end_datetime - self.start_datetime
        self.duration = td.total_seconeds()

        segment_qs = UsinglogSegmentDim.objects \
            .filter(startsecond__gte=self.duration,
                    endsecond=self.duration)
        self.segment = segment_qs.get()


# Result
class BaseResult(models.Model):

    device_platform = models.ForeignKey(DevicePlatformDim, null=True)

    CYCLE_TYPES = (
        (0, 'all'),
        (1, 'daily'),
        (2, 'weekly'),
        (3, 'monthly'),
        (4, '3days'),
        (5, 'custom'),
    )

    cycle_type = models.PositiveSmallIntegerField('统计周期',
                                                  choices=CYCLE_TYPES,
                                                  db_index=True,
                                                  max_length=2)

    start_date = models.ForeignKey(DateDim, related_name='+')

    end_date = models.ForeignKey(DateDim, related_name='+')

    class Meta:
        abstract = True


class BaseSumActivateResult(BaseResult):

    total_reserve_count = models.PositiveIntegerField('累计激活',
                                                      default=0,
                                                      max_length=11,
                                                      )

    reserve_count = models.PositiveIntegerField('激活',
                                                default=0,
                                                max_length=11,
                                                )

    active_count = models.PositiveIntegerField('活跃',
                                               default=0,
                                               max_length=11,
                                               )

    open_count = models.PositiveIntegerField('启动次数',
                                             default=0,
                                             max_length=11,
                                             )

    class Meta:
        abstract = True


productkey_verbose_name = '产品类型'

def factory_sum_activate_result_model(flag_field_name,
                                      base_model=BaseSumActivateResult):
    bind_fields_map = {
        #'device_platform': models.ForeignKey(DevicePlatformDim, null=True, related_name='+'),
        'productkey': models.ForeignKey(ProductKeyDim, related_name='+'),
        'product': models.ForeignKey(ProductDim, related_name='+'),
        'packagekey': models.ForeignKey(PackageKeyDim, related_name='+'),
        'package': models.ForeignKey(PackageDim, related_name='+'),
    }
    reserve_fields = ActivateNewReserveFact.objects.reserve_fields

    flag_field = None
    for field in reserve_fields:
        if field.name == flag_field_name:
            flag_field = field

    if not flag_field:
        raise KeyError('field %s not found' %flag_field_name)

    if not flag_field.sum_fields:
        raise ValueError('field %s not supported' %flag_field_name)

    base_name = "".join([name.capitalize() \
                    for name in flag_field.name.lstrip('is_new_').split('_')])
    class_name = 'SumActivateDevice%sResult' % base_name

    index_fields1 = deepcopy(list(flag_field.sum_fields))
    index_fields2 = deepcopy(index_fields1)
    index_fields2.append('cycle_type')
    index_fields3 = deepcopy(index_fields2)
    index_fields3.append('start_date')
    index_fields4 = deepcopy(index_fields3)
    index_fields4.append('end_date')
    index_fields5 = ['cycle_type', 'start_date', 'end_date']

    class Meta:
        verbose_name = flag_field.verbose_name
        verbose_name_plural = flag_field.verbose_name
        db_table = 'result_sum_activate_%s' % base_name.lower()
        unique_together = (
            index_fields4,
        )
        index_together = (
            index_fields1,
            index_fields2,
            index_fields3,
            index_fields4,
            index_fields5,
        )

    class_attrs = {
        'Meta': Meta,
        '__module__': base_model.__module__,
    }
    new_model = type(base_model)(class_name, (base_model,), class_attrs)
    for bind_field_name in flag_field.sum_fields:
        if bind_field_name in bind_fields_map:
            bind_fields_map[bind_field_name].contribute_to_class(new_model,
                                                                 bind_field_name)

    new_model._sum_field_names = flag_field.sum_fields
    new_model._flag_field_name = flag_field.name
    return new_model

SumActivateDeviceProductChannelResult = factory_sum_activate_result_model('is_new_product_channel')
SumActivateDeviceProductChannelPackageResult = factory_sum_activate_result_model('is_new_product_channel_package')
SumActivateDeviceProductChannelPackageVersionResult = factory_sum_activate_result_model('is_new_product_channel_package_version')
SumActivateDeviceProductResult = factory_sum_activate_result_model('is_new_product')
SumActivateDeviceProductPackageResult = factory_sum_activate_result_model('is_new_product_package')
SumActivateDeviceProductPackageVersionResult = factory_sum_activate_result_model('is_new_product_package_version')


class BaseAnalysisResult(models.Model):

    date = models.ForeignKey(DateDim, related_name='+')


    d3au_count = models.PositiveIntegerField('3日活跃数D3AU',
                                             default=0,
                                             max_length=11)

    d3au_rate = models.DecimalField('3日活跃比D3AU-R',
                                    default=0,
                                    max_digits=5,
                                    decimal_places=2)

    dau_count = models.PositiveIntegerField('日活跃数DAU',
                                            default=0,
                                            max_length=11)

    dau_rate = models.DecimalField('日活跃比DAU-R',
                                   default=0,
                                   max_digits=5,
                                   decimal_places=2)

    wau_count = models.PositiveIntegerField('周活跃WAU',
                                            default=0,
                                            max_length=11)

    wau_rate = models.DecimalField('周活跃比WAU-R',
                                   default=0,
                                   max_digits=5,
                                   decimal_places=2)

    mau_count = models.PositiveIntegerField('月活跃MAU',
                                            default=0,
                                            max_length=11)

    mau_rate = models.DecimalField('月活跃比MAU-R',
                                   default=0,
                                   max_digits=5,
                                   decimal_places=2)

    class Meta:
        abstract = True


class BaseCubePackageActivateResult(BaseSumActivateResult):

    class Meta:
        abstract = True


def factory_cube_activate_package_result_model(flag_field_name, base_model=BaseCubePackageActivateResult):
    bind_fields_map = {
        #'device_platform': models.ForeignKey(DevicePlatformDim, related_name='+'),
        'packagekey': models.ForeignKey(PackageKeyDim, related_name='+'),
        'package': models.ForeignKey(PackageDim, related_name='+'),
        'productkey': models.ForeignKey(ProductKeyDim, related_name='+'),
        'product': models.ForeignKey(ProductDim, related_name='+'),
    }
    reserve_fields = ActivateNewReserveFact.objects.reserve_fields

    flag_field = None
    for field in reserve_fields:
        if field.name == flag_field_name:
            flag_field = field

    if not flag_field:
        raise KeyError('field %s not found' %flag_field_name)

    field_names_to_add = flag_field.cube_fields
    if not field_names_to_add:
        raise ValueError('field %s not supported' %flag_field_name)

    base_name = "".join([name.capitalize() \
                         for name in flag_field.name.lstrip('is_new_').split('_')])
    class_name = 'CubeActivateDevice%sResult' % base_name

    index_fields1 = deepcopy(list(field_names_to_add))
    index_fields2 = deepcopy(index_fields1)
    index_fields2.append('cycle_type')
    index_fields3 = deepcopy(index_fields2)
    index_fields3.append('start_date')
    index_fields4 = deepcopy(index_fields3)
    index_fields4.append('end_date')
    index_fields5 = ['cycle_type', 'start_date', 'end_date']

    class Meta:
        verbose_name = "Cube %s"% flag_field.verbose_name
        verbose_name_plural = "Cube %s"% flag_field.verbose_name
        db_table = 'result_cube_activate_%s' % base_name.lower()
        unique_together = (
            index_fields4,
        )
        index_together = (
            index_fields1,
            index_fields2,
            index_fields3,
            index_fields4,
            index_fields5,
        )

    class_attrs = {
        'Meta': Meta,
        '__module__': base_model.__module__,
    }

    new_model = type(base_model)(class_name, (base_model,), class_attrs)
    for bind_field_name in field_names_to_add:
        if bind_field_name in bind_fields_map:
            bind_fields_map[bind_field_name].contribute_to_class(new_model,
                                                                 bind_field_name)
    new_model._sum_field_names = field_names_to_add
    new_model._flag_field_name = flag_field.name
    return new_model


CubeActivateDeviceProductChannelPackageResult = factory_cube_activate_package_result_model('is_new_product_channel_package')
CubeActivateDeviceProductChannelPackageVersionResult = factory_cube_activate_package_result_model('is_new_product_channel_package_version')


class SumDownloadProductResult(BaseResult):

    productkey = models.ForeignKey(ProductKeyDim,
                                   verbose_name=productkey_verbose_name,
                                   related_name='+')

    total_download_count = models.PositiveIntegerField('累计下载次数',
                                                       default=0,
                                                       max_length=11,
                                                       )

    download_count = models.PositiveIntegerField('下载次数',
                                                 default=0,
                                                 max_length=11,
                                                 )

    total_downloaded_count = models.PositiveIntegerField('累计下载完成数',
                                                   default=0,
                                                   max_length=11,
                                                   )

    downloaded_count = models.PositiveIntegerField('下载完成数',
                                                   default=0,
                                                   max_length=11,
                                                   )

    class Meta:
        verbose_name = '应用下载'
        verbose_name_plural = '应用下载统计'
        db_table = 'result_sum_download_product'
        unique_together = (
            ('productkey', 'start_date', 'end_date',),
        )
        index_together = (
            ('productkey', 'cycle_type', 'end_date', ),
            ('productkey', 'cycle_type', 'start_date', ),
            ('productkey', 'cycle_type', 'start_date', 'end_date',),
            ('cycle_type', 'start_date', 'end_date', ),
        )
        ordering = ('-start_date', 'productkey')


class CubeDownloadResult(BaseResult):

    total_download_count = models.PositiveIntegerField('累计下载次数',
                                                       default=0,
                                                       max_length=11,
                                                       )

    download_count = models.PositiveIntegerField('下载次数',
                                                 default=0,
                                                 max_length=11,
                                                 )

    total_downloaded_count = models.PositiveIntegerField('累计下载完成数',
                                                         default=0,
                                                         max_length=11,
                                                         )

    downloaded_count = models.PositiveIntegerField('下载完成数',
                                                   default=0,
                                                   max_length=11,
                                                   )

    class Meta:
        abstract = True


def factory_cube_download_result_model(model_name, field_names_to_add, base_model=CubeDownloadResult):
    bind_fields_map = {
        #'device_platform': models.ForeignKey(DevicePlatformDim, related_name='+'),
        'packagekey': models.ForeignKey(PackageKeyDim, related_name='+'),
        'package': models.ForeignKey(PackageDim, related_name='+'),
        'productkey': models.ForeignKey(ProductKeyDim, related_name='+'),
        'product': models.ForeignKey(ProductDim, related_name='+'),
        'download_packagekey': models.ForeignKey(PackageKeyDim, related_name='+'),
        'download_package': models.ForeignKey(PackageDim, related_name='+'),
    }

    if not field_names_to_add:
        raise ValueError('fields must not empty')

    new_field_names_to_add = list(deepcopy(field_names_to_add))
    if 'device_platform' not in new_field_names_to_add:
        new_field_names_to_add.insert(0, 'device_platform')


    index_fields1 = deepcopy(list(new_field_names_to_add))
    index_fields2 = deepcopy(index_fields1)
    index_fields2.append('cycle_type')
    index_fields3 = deepcopy(index_fields2)
    index_fields3.append('start_date')
    index_fields4 = deepcopy(index_fields3)
    index_fields4.append('end_date')
    index_fields5 = ['cycle_type', 'start_date', 'end_date']

    class Meta:
        db_table = 'result_cube_download_%s' % model_name.lower()
        unique_together = (
            index_fields4,
        )
        index_together = (
            index_fields1,
            index_fields2,
            index_fields3,
            index_fields4,
            index_fields5,
        )

    class_attrs = {
        'Meta': Meta,
        '__module__': base_model.__module__,
    }

    class_name = 'CubeDownload%sResult' % model_name
    new_model = type(base_model)(class_name, (base_model,), class_attrs)
    for bind_field_name in field_names_to_add:
        if bind_field_name in bind_fields_map:
            bind_fields_map[bind_field_name].contribute_to_class(new_model,
                                                                 bind_field_name)
    new_model._sum_field_names = new_field_names_to_add
    return new_model


CubeDownloadProductResult = factory_cube_download_result_model('Product', ('productkey',))

# package/packagekey 分发出去的下载量
CubeDownloadProductPackageResult = factory_cube_download_result_model('ProductPackage', ('productkey', 'packagekey'))
CubeDownloadProductPackageVersionResult = factory_cube_download_result_model('ProductPackageVersion', ('productkey', 'packagekey', 'package'))

# download_package/download_packagekey自身被下载数量
CubeDownloadProductPackageIncomingResult = factory_cube_download_result_model('ProductPackageIncoming', ('productkey', 'download_packagekey'))
CubeDownloadProductPackageVersionIncomingResult = factory_cube_download_result_model('ProductPackageVersionIncoming', ('productkey', 'download_packagekey', 'download_package'))

from django.conf import settings

if "south" in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules(rules=[
            ((ReserveBooleanField,), [], {}),
        ],
                                patterns=["analysis\.models\."])
    except ImportError:
        pass
