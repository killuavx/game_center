# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from model_utils import Choices
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject


class PackageStorage(LazyObject):

    def _setup(self):
        self._wrapped = get_storage_class('toolkit.storage.QiniuPackageFileStorage')()


class QiniuPackageFileStorage(FileSystemStorage):

    HOST_MARK = 'http://%s.qiniudn.com/'

    BUCKET = Choices(
        ('sf-ios', 'ios', 'IOS'),
        ('sf-android', 'android', 'Android'),
    )

    def get_host_url(self, name):
        if name.startswith('ipackage'):
            return self.HOST_MARK % self.BUCKET.ios
        # android static
        return self.base_url

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.get_host_url(name), filepath_to_uri(name))

package_storage =  PackageStorage()