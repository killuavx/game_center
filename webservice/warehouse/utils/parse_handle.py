# -*- coding: utf-8 -*-
import io
import os
from os.path import join
import shutil
from django.core.files import File
from django.conf import settings
from warehouse.models import Package, Author
from django.core.exceptions import ObjectDoesNotExist
from warehouse.utils.parser import set_package_parser_exe

set_package_parser_exe(settings.AAPT_CMD)

class DiffPackageNameFromApkInfo(Exception):
    pass

class ParsePackageVersion(object):

    _version = None

    _pkgparser = None

    package_class = Package

    _opts = {
        'unzip_file_temp_dir': getattr(settings,
                                       'UNZIP_FILE_TEMP_DIR',
                                       '/tmp/warehouse-uploader'),
        'icon_priority_density': 320,
        'locale_priority': ['zh', 'zh_CN', 'zh_TW', 'en', 'en_GB'],
    }

    def __init__(self, packageversion, parser=None):
        self._pkgparser = parser
        self._version = packageversion

    def can_parse_appfile(self):
        return self._version.download and self._pkgparser

    def parse_to_package(self):
        pkg = self._get_or_new_package_of_version()
        pkginfo = self._pkgparser.package
        self._check_package_name_between_package_and_profile()
        pkg.package_name = pkginfo.get('package_name')
        if not pkg.title:
            locale = self.choose_locale()
            pkg.title = self._pkgparser.application_labels[locale or '']

        return self._version.package

    def _get_or_new_package_of_version(self):
        try:
            pkg = self._version.package
        except ObjectDoesNotExist:
            pkg = Package()
            pkg.author = self._get_default_author()
            self._version.package = pkg
        return pkg

    def _get_default_author(self):
        author, is_new = Author.objects \
            .get_or_create(pk=-1,
                           name='default',
                           email='default@ccplay.com.cn')
        return author

    def _check_package_name_between_package_and_profile(self):
        package = self._version.package;
        pkginfo = self._pkgparser.package
        if package.pk and package.package_name != pkginfo.get('package_name'):
            raise DiffPackageNameFromApkInfo(
                'Package:%s Name Different from Apk pacakge name:%s'% \
                (package.package_name, pkginfo.package_name))

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
        tmpdir = join(self._opts.get('unzip_file_temp_dir'), package_name)
        os.makedirs(tmpdir, exist_ok=True)

        density = self.choose_icon_density()
        resource_name = pkgparser.application_icons[str(density)]
        tmpfile = pkgparser.fetch_file(resource_name, to_path=tmpdir)
        self._version.icon = File(io.FileIO(tmpfile))
        shutil.rmtree(tmpdir)

        return self._version

    def choose_icon_density(self):
        """
        choose icon density:
            priority:
             1. 320
             2. 240
             3. 160
             4. 120
             5. 480
             6. ...
        """
        icons = self._pkgparser.application_icons
        if len(icons) == 0:
            raise ValueError('application icons should not be empty')

        priority_density = self._opts.get('icon_priority_density')
        keys = list(icons.keys())
        keys.sort()
        if str(priority_density) in keys:
            return priority_density

        keys.append(str(priority_density))
        keys.sort()
        idx = keys.index(str(priority_density))
        if idx == 0:
            return int(keys[idx+1])
        else:
            return int(keys[idx-1])

    def choose_locale(self):
        for l in self._opts.get("locale_priority"):
            if l in self._pkgparser.locales:
                return l
        return None
