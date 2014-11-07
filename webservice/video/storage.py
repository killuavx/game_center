# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.functional import LazyObject
from django.core.files.storage import FileSystemStorage
from urllib.parse import urljoin
from django.utils.encoding import filepath_to_uri
from django.core.files.storage import get_storage_class


class LocalFileStorageMixin(object):

    def get_host_url(self, name):
        return 'http://192.168.5.6:8080/media/'

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.get_host_url(name), filepath_to_uri(name))


class VideoFileStorage(LocalFileStorageMixin, FileSystemStorage):
    pass


class VideoStorage(LazyObject):

    def _setup(self):
        self._wrapped = get_storage_class('video.storage.VideoFileStorage')()


default_storage = VideoStorage()
