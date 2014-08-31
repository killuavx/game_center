# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from django.utils.timezone import make_aware, get_default_timezone
from model_utils import Choices
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject
from django.conf import settings
from toolkit.helpers import import_from
import os
import sh
import json


class QBoxCtl(object):

    CMD = settings.QINIU_CMD

    QUSERNAME = os.environ.get('QINIU_USERNAME')

    QPASSWORD = os.environ.get('QINIU_PASSWORD')

    def __init__(self):
        self.ctl = sh.Command(self.CMD)
        """
        try:
            self.ctl.login(self.QUSERNAME, self.QPASSWORD)
        except:
            pass
        """

    def __getattr__(self, key):
        if key == 'delete':
            key = 'del'
        action = getattr(self.ctl, key)
        def _wrapper(*args, **kwargs):
            try:
                result = str(action(*args, **kwargs))
                return json.loads(result)
            except sh.ErrorReturnCode as e:
                if 'no such file or directory' in str(e):
                    raise FileNotFoundError(
                        'no such file or directory: %s %s' %(args, kwargs))
                else:
                    raise
        return _wrapper


class QBoxCtlLazy(LazyObject):

    def _setup(self):
        self._wrapped = QBoxCtl()


qboxctl = QBoxCtlLazy()


class PackageStorage(LazyObject):

    def _setup(self):
        self._wrapped = get_storage_class('toolkit.storage.QiniuPackageWithRandomHostFileStorage')()


class QiniuPackageFileStorageMixin(object):

    ctl = qboxctl

    HOST_MARK = 'http://m-%s.ccplay.com.cn/'

    BUCKET = Choices(
        ('ios', 'ios', 'IOS'),
        ('android', 'android', 'Android'),
    )

    BUCKET_NAME = Choices(
        ('sf-ios', 'ios', 'IOS Bucket'),
        ('sf-android', 'android', 'Android Bucket'),
    )

    _cache_file_stat = {}

    def __init__(self, location=None, base_url=None):
        super(QiniuPackageFileStorageMixin, self).__init__(location=location,
                                                           base_url=base_url)

    def _file_stat(self, bucket_name, name):
        return self.ctl.stat(bucket_name, name)
        key = "%s:%s" % (bucket_name, name)
        if key not in self._cache_file_stat:
            try:
                stat = self.ctl.stat(bucket_name, name)
                self._cache_file_stat[key] = stat
            except Exception as e:
                self._cache_file_stat[key] = e

        if isinstance(self._cache_file_stat[key], Exception):
            raise self._cache_file_stat[key]
        else:
            return self._cache_file_stat[key]

    def is_qiniu_file(self, name):
        return name.startswith('ipackage')

    def get_host_url(self, name):
        if self.is_qiniu_file(name):
            return self.HOST_MARK % self.BUCKET.ios
            # android static
        return self.base_url

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.get_host_url(name), filepath_to_uri(name))

    def remote_exists(self, name):
        try:
            self._file_stat(self.BUCKET_NAME.ios, name)
            return True
        except FileNotFoundError:
            return False

    def remote_size(self, name):
        return self._file_stat(self.BUCKET_NAME.ios, name)['fsize']

    def remote_delete(self, name):
        return self.ctl.delete(self.BUCKET_NAME.ios, name)

    def remote_accessed_time(self, name):
        return self.remote_created_time(name)

    def remote_created_time(self, name):
        ts = self._file_stat(self.BUCKET_NAME.ios, name)['putTime']/10000000
        return make_aware(datetime.fromtimestamp(ts), get_default_timezone())

    def remote_modified_time(self, name):
        return self.remote_created_time(name)

    def remote_save(self, name):
        try:
            self._file_stat(self.BUCKET_NAME.ios, name)
        except FileNotFoundError:
            self.ctl.put('-c', self.BUCKET_NAME.ios, name, name)


class QiniuPackageFileStorage(QiniuPackageFileStorageMixin, FileSystemStorage):
    pass


class QiniuPackageWithRandomHostFileStorage(QiniuPackageFileStorage):

    host_subname = 'd{0}.media'

    host_sequeue_min = 1

    host_sequeue_max = 4

    use_random_source = True

    def get_host_url(self, name):
        if self.use_random_source:
            if not self.is_qiniu_file(name):
                new_host = self.host_subname.format(randint(self.host_sequeue_min,
                                                            self.host_sequeue_max))
                return self.base_url.replace('//media', '//%s' % new_host)
        return super(QiniuPackageWithRandomHostFileStorage, self).get_host_url(name)


package_storage = PackageStorage()


FileSystemStorageMixin = import_from("%s.storage.FileSystemStorageMixin" % settings.PACKAGE_NAME_FILEBROWSER)


from easy_thumbnails.storage import ThumbnailFileSystemStorage


class QiniuThumbnailImageStorage(QiniuPackageFileStorageMixin,
                                 ThumbnailFileSystemStorage):
    pass


from random import randint


class QiniuThumbnailImageWithRandomHostStorage(QiniuThumbnailImageStorage):

    host_subname = 'i{0}.media'

    host_sequeue_min = 1

    host_sequeue_max = 4

    use_random_source = True

    def get_host_url(self, name):
        if self.use_random_source:
            if not self.is_qiniu_file(name):
                new_host = self.host_subname.format(randint(self.host_sequeue_min,
                                                            self.host_sequeue_max))
                return self.base_url.replace('//media', '//%s' % new_host)
        return super(QiniuThumbnailImageWithRandomHostStorage, self).get_host_url(name)


class ImageRandomHostStorage(LazyObject):

    def _setup(self):
        self._wrapped = get_storage_class('toolkit.storage.QiniuThumbnailImageWithRandomHostStorage')()


screenshot_thumbnail_storage = image_storage = ImageRandomHostStorage()


class QiniuResourceFileStorage(QiniuPackageFileStorageMixin,
                               FileSystemStorageMixin,
                               FileSystemStorage):
    pass


class ResourceStorage(LazyObject):

    def _setup(self):
        self._wrapped = get_storage_class('toolkit.storage.QiniuResourceFileStorage')()


resource_storage = ResourceStorage()



