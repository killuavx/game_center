# -*- coding: utf-8 -*-
from toolkit.helpers import get_global_site
from toolkit.memoizes import orms_memoize
from cache_tagging.django_cache_tagging import cache, caches
import logging

DEFAULT_TIMEOUT = 3600


class CacheTaggingMixin(object):

    _tagging_cache = cache

    def _get_tagging_cache(self):
        return self._tagging_cache

    def get_cache_identifier(self):
        raise NotImplementedError()

    def get_cache_identifier_alias(self):
        raise NotImplementedError()

    def get_all_cache_identifier_tags(self):
        return (self.get_cache_identifier(), self.get_cache_identifier_alias(),)

    def _get_site_id(self):
        if getattr(self, 'site_id', None):
            return self.site_id
        if getattr(self, 'site', None):
            return self.site if isinstance(self.site, int) else self.site.pk
        return get_global_site().pk

    def invalidate_tagging_cache(self):
        tags = self.get_all_cache_identifier_tags()
        self._get_tagging_cache().invalidate_tags(*tags)


class CacheManagerMixin(object):

    def cache_object_in_list(self, pk):
        try:
            return [self.get(pk=pk)]
        except:
            return []

    def get_cache_by(self, pk=None):
        try:
            return self.cache_object_in_list(pk)[0]
        except IndexError:
            return None

    def get_cache_by_alias(self, *args, **kwargs):
        raise NotImplementedError


class PackageCacheManagerMixin(CacheManagerMixin):

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_object_in_list(self, pk):
        try:
            return [self.get(pk=pk)]
        except:
            return []

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_object_in_list_by_alias(self, site_id, package_name):
        try:
            return [self.get(site_id=site_id, package_name=package_name)]
        except:
            return []

    def get_cache_by_alias(self, site_id, package_name, **kwargs):
        try:
            return self.cache_object_in_list_by_alias(site_id, package_name)[0]
        except IndexError:
            return None


class PackageTaggingMixin(CacheTaggingMixin):

    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT * 3

    def get_cache_identifier(self):
        return 'warehouse.package.{0}'.format(self.pk)

    def get_cache_identifier_alias(self):
        return 'warehouse.package.{0}:{1}'.format(self._get_site_id(),
                                                  self.package_name)

    def get_cache_latest_version(self):
        if self.latest_version_id:
            version_cls = self.__class__.latest_version.field.rel.to
            version = version_cls.all_objects.get_cache_by(self.latest_version_id)
            version.package = self
            return version
        return None

    def get_cache_version_alias(self, version_name):
        version_cls = self.__class__.latest_version.field.rel.to
        version_cls.all_objects.get_cache_by_
        pass


class PackageWithLatestVersionTaggingMixin(PackageTaggingMixin):

    def get_cache_latestversion_identifier(self):
        return 'warehouse.packageversion.{0}'.format(self.latest_version_id)

    def get_cache_latestversion_identifier_alias(self):
        return 'warehouse.packageversion.{0}:{1}:{2}'.format(self._get_site_id(),
                                                             self.package_name,
                                                             self.version_name)

    def get_all_cache_identifier_tags(self):
        tags = super(PackageWithLatestVersionTaggingMixin, self).get_all_cache_identifier_tags()
        return tags + (self.get_cache_latestversion_identifier(),
                       self.get_cache_latestversion_identifier_alias(), )


class PackageVersionTaggingMixin(CacheTaggingMixin):

    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT * 3

    def get_cache_identifier(self):
        return 'warehouse.packageversion.{0}'.format(self.pk)

    def get_cache_identifier_alias(self):
        return 'warehouse.packageversion.{0}:{1}:{2}'.format(self._get_site_id(),
                                                  self.package.package_name,
                                                  self.version_name)

    def get_cache_package(self):
        pkg_cls = self.__class__.package.field.rel.to
        package = pkg_cls.all_objects.get_cache_by(self.package_id)
        package.latest_version = self
        return package


class PackageVersionCacheManagerMixin(CacheManagerMixin):

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_object_in_list(self, pk):
        try:
            return [self.get(pk=pk)]
        except:
            return []

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_list_by_alias(self, package_id=None, **kwargs):
        try:
            return self.filter(package_id=package_id, **kwargs)
        except:
            return []

    def get_cache_by_alias(self, **kwargs):
        try:
            return self.cache_list_by_alias(**kwargs)[0]
        except IndexError:
            return None


class TaxonomyTaggingMixin(CacheTaggingMixin):

    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT*24*7

    @classmethod
    def _module_name(cls):
        return cls.__name__.lower()

    def get_cache_identifier(self):
        return 'taxonomy.{0}.{1}'.format(self._module_name(),
                                         self.pk)

    def get_cache_identifier_alias(self):
        return 'taxonomy.{0}.{1}:{2}'.format(self._module_name(),
                                             self._get_site_id(),
                                             self.slug)


class TaxonomyCacheManagerMixin(CacheManagerMixin):

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_object_in_list(self, pk):
        try:
            return [self.get(pk=pk)]
        except:
            return []

    @orms_memoize(timeout=DEFAULT_TIMEOUT)
    def cache_object_in_list_by_alias(self, site_id, slug):
        try:
            return [self.get(site_id=site_id, slug=slug)]
        except:
            return []

    def get_cache_by_alias(self, site_id, slug, **kwargs):
        try:
            return self.cache_object_in_list_by_alias(site_id, slug)[0]
        except IndexError:
            return None

    def get_cache_by_slug(self, site_id, slug):
        return self.get_cache_by_alias(site_id, slug)


from datetime import timedelta
from django.utils.encoding import force_str
from toolkit import helpers
from cache_tagging.tagging import tag_prepare_name
from itertools import chain

default_cache = cache


class CacheLocationHandler(object):

    timeout = timedelta(days=1)

    def __init__(self, cache=None):
        self.cache = cache if cache else default_cache
        self.key_mark = 'tag_location:%s:%s'

    def get_site_name(self):
        site = helpers.get_global_site()
        if not site:
            return None
        if site.pk == helpers.SITE_IOS:
            return 'ios'
        elif site.pk == helpers.SITE_ANDROID:
            return 'android'
        else:
            return 'unknown'

    def get_key(self, tag, site_name=None):
        return self.key_mark % (site_name, tag_prepare_name(tag))

    def register(self, url, *tags, **kwargs):
        tags = set(tags)
        if kwargs.get('tags'):
            tags.update(kwargs.get('tags'))
        site_name = self.get_site_name()
        pip = self.cache.raw_client.pipeline()
        for tag in tags:
            key = self.get_key(tag, site_name)
            pip.sadd(key, url)
            pip.expire(key, self.timeout)
        pip.execute()

    def get_urls(self, *tags, **kwargs):
        tags = set(tags)
        if kwargs.get('tags'):
            tags.update(kwargs.get('tags'))
        site_name = self.get_site_name()
        pip = self.cache.raw_client.pipeline()
        for tag in tags:
            key = self.get_key(tag, site_name)
            pip.smembers(key)
        for url in set(chain.from_iterable(pip.execute())):
            yield force_str(url)

    def remove_urls(self, *tags, **kwargs):
        tags = set(tags)
        if kwargs.get('tags'):
            tags.update(kwargs.get('tags'))
        site_name = self.get_site_name()
        self.cache.raw_client.delete(*[self.get_key(tag, site_name)
                                       for tag in tags])


cache_locator = CacheLocationHandler()
