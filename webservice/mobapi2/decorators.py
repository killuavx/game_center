# -*- coding: utf-8 -*-
from functools import wraps
from django.utils.cache import patch_cache_control
from django.utils.decorators import available_attrs


class CacheControlProcessor(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, func):
        this = self
        @wraps(func, assigned=available_attrs(func))
        def inner(self, request, *args, **kwargs):
            response = this.process_cachecontrol_response(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
                )
            return response
        return inner

    def process_cachecontrol_response(self,
                                      view_instance,
                                      view_method,
                                      request,
                                      args,
                                      kwargs):
        response = view_method(view_instance, request, *args, **kwargs)
        response = view_instance.finalize_response(request, response, *args, **kwargs)
        response.render()  # should be rendered, before picklining while storing to cache

        patch_cache_control(response, **self.kwargs)
        return response


cache_control = CacheControlProcessor


class DefaultCacheControlProcessor(CacheControlProcessor):

    def __init__(self, **kwargs):
        kwargs.setdefault('public', True)
        kwargs.setdefault('max_age', 3600)
        kwargs.setdefault('s_maxage', 3600)
        super(DefaultCacheControlProcessor, self).__init__(**kwargs)

default_cache_control = CacheControlProcessor

