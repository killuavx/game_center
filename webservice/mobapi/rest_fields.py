# -*- coding: utf-8 -*-
from easy_thumbnails.exceptions import InvalidImageFormatError
from rest_framework import serializers


class ImageUrlField(serializers.ImageField):
    size_alias = 'middle'

    def to_native(self, obj):
        if not obj:
            return None
        try:
            if self.size_alias is None:
                return obj.url
            return obj[self.size_alias].url
        except (ValueError, KeyError, InvalidImageFormatError):
            return None

    def from_native(self, data):
        pass


class FileUrlField(serializers.FileField):
    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass


def factory_imageurl_field(size_alias='middle'):
    field = ImageUrlField()
    field.size_alias = size_alias
    return field