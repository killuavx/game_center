import json
import os
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from model_utils import Choices
from toolkit.fields import PkgFileField
import requests


class IOSAppData(models.Model):

    appid = models.CharField(max_length=100, db_index=True)

    package_name = models.CharField(max_length=200, null=True, blank=True)

    version_name = models.CharField(max_length=200, null=True, blank=True)

    mainclass = models.CharField(max_length=50, db_index=True)

    subclass = models.CharField(max_length=50, db_index=True)

    device = models.IntegerField()

    is_free = models.IntegerField(db_column='isfree')

    is_analysised = models.BooleanField()

    content = models.TextField(db_column='download_content')

    packageversion_id = models.IntegerField(db_index=True,
                                            null=True, blank=True)

    analysised = models.DateTimeField(null=True, blank=True)

    is_image_downloaded = models.BooleanField(default=False)

    image_downloaded = models.DateTimeField(null=True, blank=True)

    # package version duplication
    ANALYSIS_PACKAGEVERSION_DUPLICATION = -1

    # lookup data is empty
    ANALYSIS_PACKAGEVERSION_EMPTY = 0

    def _get_packageversion(self):
        if self.packageversion_id:
            from warehouse.models import IOSPackageVersion
            return IOSPackageVersion.objects.get(pk=self.packageversion_id)
        return None

    def _set_packageversion(self, packageversion):
        from warehouse.models import (IOSPackageVersion, PackageVersion)
        if isinstance(packageversion, int):
            packageversion = IOSPackageVersion.objects.get(pk=packageversion)
            self.packageversion_id = packageversion.pk
        elif isinstance(packageversion, IOSPackageVersion):
            self.packageversion_id = packageversion.pk
        elif isinstance(packageversion, PackageVersion):
            try:
                iospackageversion = packageversion.iospackageversion
                self.packageversion_id = iospackageversion.pk
            except ObjectDoesNotExist:
                raise TypeError('version must instance of IOSPackageVersion: %s' % packageversion)
        else:
            raise TypeError('version must instance of IOSPackageVersion')

    packageversion = property(_get_packageversion, _set_packageversion)

    @classmethod
    def convert_normal_version(cls, pv):
        from warehouse.models import PackageVersion
        print(type(pv))
        print(pv)
        pv.__class__ = PackageVersion
        return pv

    def set_analysised(self, version=None):
        if isinstance(version, int) and version <=0:
            self.packageversion_id = version
            self.package_name = self.version_name = None
        elif version and hasattr(version, 'pk'):
            self.packageversion = version
            self.package_name = version.package.package_name
            self.version_name = version.version_name
        self.analysised = now()
        self.is_analysised = True

    class Meta:
        index_together = (
            ('is_free', ),
            ('analysised', ),
            ('is_analysised', ),
            ('is_image_downloaded', ),
            ('image_downloaded', ),
            ('mainclass', 'subclass'),
        )
        unique_together = (
            ('appid', 'package_name', 'version_name'),
        )

    def _get_content_json(self):
        if not hasattr(self, '_content_data'):
            try:
                content = json.loads(self.content)['results'][0]
            except:
                content = None
            self._content_data = content
        return self._content_data
    content_data = property(_get_content_json)


    LOOKUP_URL_MARK = 'https://itunes.apple.com/%(location)slookup?id=%(track_id)s'

    @classmethod
    def lookup_url(cls, appid, location=''):
        if len(location):
            location = location + '/'
        return cls.LOOKUP_URL_MARK % {'location': location, 'track_id': appid}

    @classmethod
    def lookup_request(cls, appid, location=''):
        url = cls.lookup_url(appid, location)
        response = requests.get(url)
        if response.status_code == 200:
            return response
        return None


def iosapp_upload_to_path(instance, filename):
    version_code = 1
    basename = os.path.basename(filename)
    appid = int(instance.appid)
    path = "ipackage/%d/v%d" % (appid, version_code)
    return "%s/%s" %(path, basename)


class IOSBuyInfo(models.Model):

    appdata = models.ForeignKey(IOSAppData, blank=True, null=True)

    appid = models.CharField(max_length=100)

    BUY_STATUS = Choices(
        (-1, 's01', 's01'),
        (0, 's0', 's0'),
        (1, 's1', 's1'),
        (2, 's2', 's2'),
        (3, 's3', 's3'),
        (4, 'ok', 'ok'),
    )

    buy_status = models.IntegerField(choices=BUY_STATUS, default=0)

    buy_info = models.TextField(default=None, null=True, blank=True)

    ipafile = PkgFileField(upload_to=iosapp_upload_to_path,
                           max_length=500,
                           null=True,
                           blank=True)

    ipafile_name = models.CharField(default=None,
                                    null=True,
                                    blank=True,
                                    max_length=300)

    version = models.CharField(max_length=200, null=True, blank=True)

    short_version = models.CharField(max_length=200, null=True, blank=True)

    account = models.CharField(max_length=255, default=None)

    created = models.DateTimeField(auto_created=True)

    updated = models.DateTimeField(auto_created=True,
                                   auto_now=True,
                                   auto_now_add=True)

    class Meta:
        index_together = (
            ('appid', ),
            ('buy_status',),
            ('updated', ),
            ('buy_status', 'updated', ),
        )

