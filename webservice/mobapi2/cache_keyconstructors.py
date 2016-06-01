# -*- coding: utf-8 -*-
from copy import deepcopy

from django.utils.encoding import force_text
from rest_framework_extensions.key_constructor import (bits, constructors)
from django.core.cache import cache
from django.utils.timezone import now
from toolkit.helpers import released_hourly_datetime

from mobapi2.helpers import make_cache_key


class OrderingKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        kwargs['params'].append('ordering')
        data = super(OrderingKeyBit, self).get_data(**kwargs)
        return data


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


class KeyBitFlushKeyMixin(object):

    def flush(self):
        cache.delete(self.get_key())


class UpdatedAtKeyBit(bits.KeyBitBase, KeyBitFlushKeyMixin):

    content_type = 'default'

    hourly = True

    timeout = None

    def __init__(self, content_type=None, timeout=None, hourly=True, params=None):
        super(UpdatedAtKeyBit, self).__init__(params)
        if content_type:
            self.content_type = content_type
        if timeout:
            self.timeout = timeout
        self.hourly = hourly

    def get_key(self):
        return make_cache_key('updated_at_timestamp.%s' % self.content_type)

    def get_data(self, **kwargs):
        key = self.get_key()
        value = cache.get(key, None)
        if not value:
            value = released_hourly_datetime(now(), hourly=self.hourly)
            cache.set(key, value=value, timeout=self.timeout)
        return force_text(value)


class CommentUpdatedAtKeyBit(bits.QueryParamsKeyBit, KeyBitFlushKeyMixin):

    target = 'comment'

    content_object_params = ('content_type', 'object_pk')

    def get_data(self, **kwargs):
        kwargs['params'] = deepcopy(self.content_object_params)
        data = super(CommentUpdatedAtKeyBit, self).get_data(**kwargs)
        key = self.get_key(**data)
        return self.get_cache_value(key)

    def get_key(self, **data):
        return "-".join([self.get_prefix_key(), self.get_params_key(**data)])

    def get_prefix_key(self):
        return make_cache_key('updated_at_timestamp:%s' % self.target)

    def get_params_key(self, **params):
        _params = {}
        for k in self.content_object_params:
            v = params.get(k) if params.get(k) else 0
            _params[k] = v
        return ":".join([
            str(_params['content_type']),
            str(_params['object_pk']),
        ])

    def get_cache_value(self, key):
        value = cache.get(key, None)
        if not value:
            value = now().astimezone().isoformat()
            cache.set(key, value=value)
        return force_text(value)


class CommentListKeyConstructor(constructors.DefaultKeyConstructor):

    comment_updated_at = CommentUpdatedAtKeyBit()

    pagination = bits.PaginationKeyBit()


def update_at_key_constructor(key_constructor,
                              content_type='default',
                              timeout=None,
                              hourly=False,
                              update_at_keybit=UpdatedAtKeyBit
                              ):

    class _UpdatedAtKeyBitKeyConstructor(key_constructor):

        updated_at = update_at_keybit(content_type=content_type,
                                      timeout=timeout,
                                      hourly=hourly)

    return _UpdatedAtKeyBitKeyConstructor


class LookupObjectUpdatedAtKeyBit(UpdatedAtKeyBit):

    pk = None

    def __init__(self, pk=None, *args, **kwargs):
        self.pk = pk if pk else None
        super(LookupObjectUpdatedAtKeyBit, self).__init__(*args, **kwargs)

    def get_key(self):
        _k = super(LookupObjectUpdatedAtKeyBit, self).get_key()
        return "%s.%s" %(_k, self.pk)

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        self.pk = view_instance.kwargs[view_instance.lookup_field]
        return super(LookupObjectUpdatedAtKeyBit, self).get_data(params=params,
                                                                 view_instance=view_instance,
                                                                 view_method=view_method,
                                                                 request=request,
                                                                 args=args,
                                                                 kwargs=kwargs)


class UserUpdatedAtKeyBit(UpdatedAtKeyBit):

    pk = None

    view_use_kwargs_param = None

    def __init__(self, pk=None, use_kwargs_param=None, *args, **kwargs):
        self.pk = pk if pk else None
        self.view_use_kwargs_param = use_kwargs_param if use_kwargs_param else 'user'
        super(UserUpdatedAtKeyBit, self).__init__(*args, **kwargs)

    def get_key(self):
        _k = super(UserUpdatedAtKeyBit, self).get_key()
        key = "%s.user:%s" %(_k, self.pk)
        return key

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        if request.user and request.user.is_authenticated() and view_instance.kwargs.get(self.view_use_kwargs_param, False):
            self.pk = request.user.pk
        else:
            self.pk = None
        return super(UserUpdatedAtKeyBit, self).get_data(params=params,
                                                         view_instance=view_instance,
                                                         view_method=view_method,
                                                         request=request,
                                                         args=args,
                                                         kwargs=kwargs)


class IpKeyBit(bits.RequestMetaKeyBit):

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        if hasattr(request, 'get_client_ip'):
            return request.get_client_ip()
        else:
            from webservice.middlewares import get_client_ip
            return get_client_ip(request)

