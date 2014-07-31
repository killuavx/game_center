# -*- coding: utf-8 -*-
from django.core import serializers
from memoize import Memoizer as BaseMemoizer, memoize, delete_memoized, delete_memoized_verhash


DEFAULT_TIMEOUT = 3600


class DjORMMemoizerProxy(BaseMemoizer):

    def get(self, key):
        value = self.cache.get(key=key)
        if value:
            result = list()
            for item in serializers.deserialize('json', value):
                result.append(item.object)
            return result
        return value

    def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        val = serializers.serialize('json', value)
        self.cache.set(key=key, value=val, timeout=timeout)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT):
        val = serializers.serialize('json', value)
        self.cache.add(key=key, value=val, timeout=timeout)

_memoizer = DjORMMemoizerProxy()
orms_memoize = _memoizer.memoize

