import json
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now


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

    def set_analysised(self, version):
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


