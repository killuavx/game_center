# -*- coding: utf-8 -*-
from django.core import serializers
from cache_tagging.django_cache_tagging import cache as tagging_cache
from memoize import Memoizer as BaseMemoizer, memoize, delete_memoized, delete_memoized_verhash


DEFAULT_TIMEOUT = 3600


class DjORMMemoizerProxy(BaseMemoizer):

    def __init__(self):
        self.cache = tagging_cache
        self.cache_prefix = 'cache_tagging'

    def get(self, key):
        value = self.cache.get(key)
        if value:
            result = list()
            for item in serializers.deserialize('json', value):
                result.append(item.object)
            return result
        return value

    def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        tags = []
        for m in value:
            if hasattr(m, 'get_all_cache_identifier_tags'):
                tags.extend(m.get_all_cache_identifier_tags())
        val = serializers.serialize('json', value)
        print(tags)
        self.cache.set(key, value=val, tags=tags, timeout=timeout)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT):
        tags = []
        for m in value:
            if hasattr(m, 'get_all_cache_identifier_tags'):
                tags.extend(m.get_all_cache_identifier_tags())
        print(tags)
        val = serializers.serialize('json', value)
        self.cache.set(key, value=val, tags=tags, timeout=timeout)

_memoizer = DjORMMemoizerProxy()
orms_memoize = _memoizer.memoize

