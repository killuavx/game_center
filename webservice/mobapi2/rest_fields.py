# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from easy_thumbnails.exceptions import InvalidImageFormatError
from rest_framework import serializers
from rest_framework.fields import DateTimeField as RFDateTimeField


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


class DateTimeField(RFDateTimeField):

    def from_native(self, value):
        from django.conf import settings
        if isinstance(value, datetime.datetime):
            if settings.USE_TZ:
                default_timezone = timezone.get_default_timezone()
                if timezone.is_aware(value):
                    return value.astimezone(default_timezone)
                else:
                    return timezone.make_aware(value, default_timezone)
        return super(DateTimeField, self).from_native(value)