# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
from rest_framework_extensions.key_constructor import (bits, constructors)
from django.core.cache import cache
from django.utils.timezone import now
from toolkit.helpers import current_site_id


class OrderingKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        if hasattr(kwargs['view_instance'], 'ordering'):
            kwargs['params'].append('ordering')
        return super(OrderingKeyBit, self).get_data(**kwargs)


class LookupKeyBit(bits.KeyBitBase):

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        lookup_value = view_instance.kwargs[view_instance.lookup_field]
        return force_text(lookup_value)


class LookupListKeyConstructor(constructors.DefaultKeyConstructor):
    lookup = LookupKeyBit()
    pagination = bits.PaginationKeyBit()


class LookupOrderingListKeyConstructor(LookupListKeyConstructor):
    ordering = OrderingKeyBit()


class ContentObjectKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        kwargs['params'].append('content_type')
        kwargs['params'].append('object_pk')
        return super(ContentObjectKeyBit, self).get_data(**kwargs)


class ContentObjectListKeyConstructor(constructors.DefaultKeyConstructor):

    content_object = ContentObjectKeyBit()

    pagination = bits.PaginationKeyBit()


class PackageFilterKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        kwargs['params'].append('package_name')
        kwargs['params'].append('version_name')
        return super(PackageFilterKeyBit, self).get_data(**kwargs)


class PackageFilterKeyConstructor(constructors.DefaultKeyConstructor):

    package = PackageFilterKeyBit()


class PackageLookupKeyBit(bits.KeyBitBase):

    def get_data(self, **kwargs):
        _kwargs = kwargs.get('kwargs')
        p = _kwargs.get('package_name')
        v = _kwargs.get('version_name')
        p = p if p else ''
        v = v if v else ''
        pv_txt = force_text(":".join([p,v]))
        return pv_txt


class PackageLookupConstructor(constructors.DefaultKeyConstructor):

    package = PackageLookupKeyBit()


def make_cache_key(prefix):
    return "%s.%s.%s" %('api', current_site_id(), prefix)


class UpdatedAtKeyBit(bits.KeyBitBase):

    content_type = 'default'

    def __init__(self, content_type=None, params=None):
        super(UpdatedAtKeyBit, self).__init__(params)
        if content_type:
            self.content_type = content_type

    def get_key(self):
        return make_cache_key('updated_at_timestamp.%s' % self.content_type)

    def get_data(self, **kwargs):
        key = self.get_key()
        value = cache.get(key, None)
        if not value:
            value = now()
            cache.set(key, value=value)
        return force_text(value)


class ContentObjectUpdatedAtContructor(constructors.DefaultKeyConstructor):

    content_object = ContentObjectKeyBit()

    updated_at = UpdatedAtKeyBit()

    def __init__(self, content_type=None, **kwargs):
        super(ContentObjectUpdatedAtContructor, self).__init__(**kwargs)
        self.updated_at = UpdatedAtKeyBit(content_type=content_type)
