# -*- coding: utf-8 -*-
import io
import os
from os.path import join
import shutil
from django.core.files import File
from warehouse import settings as warehouse_settings
from warehouse.models import Package, Author
from django.core.exceptions import ObjectDoesNotExist


class ParsePackageVersion(object):

    _version = None

    _pkgparser = None

    package_class = Package

    def __init__(self, packageversion, parser=None):
        self._pkgparser = parser
        self._version = packageversion

    def can_parse_appfile(self):
        return self._version.download and self._pkgparser

    def parse_to_package(self):
        try:
            pkg = self._version.package
        except ObjectDoesNotExist:
            pkg = Package()
            pkg.author, is_new = Author.objects \
                .get_or_create(pk=-1,
                               name='default',
                               email='default@ccplay.com.cn')
            self._version.package = pkg

        pkginfo = self._pkgparser.package
        if pkg.pk and pkg.package_name != pkginfo.get('package_name'):
            raise Exception('Different package_name '
                            'between Package and PackageVersion')

        pkg.package_name = pkginfo.get('package_name')
        pkg.title = self._pkgparser.application_labels['']
        return self._version.package

    def parse_to_version(self):
        pkgparser = self._pkgparser
        pkginfo = pkgparser.package
        version = self._version
        if not version.version_code:
            version.version_code = pkginfo.get('version_code')
        if not version.version_name:
            version.version_name = pkginfo.get('version_name')

        return version

    def fetch_icon_to_version(self):
        pkgparser = self._pkgparser
        package_name = pkgparser.package.get('package_name')
        tmpdir = join(warehouse_settings.UNZIP_FILE_TEMP_DIR, package_name)
        os.makedirs(tmpdir, exist_ok=True)

        resource_name = pkgparser.application_icons['160']
        tmpfile = pkgparser.fetch_file(resource_name, to_path=tmpdir)
        self._version.icon = File(io.FileIO(tmpfile))
        shutil.rmtree(tmpdir)

        return self._version
