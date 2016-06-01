# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from apksite.apis import ApiListPaginator, ApiListResultSet, ApiFactory


PRODUCT = 'web'


class ApiParamFilterBackendViewMixin(object):

    filter_param_backends = ()

    paginator_class = ApiListPaginator

    api_list_result_class = ApiListResultSet

    query_params = None

    def filter_params(self, request, *args, **kwargs):
        params = dict()
        for backend in self.filter_param_backends:
            result = backend().filter_params(request, *args, **kwargs)
            if result:
                params.update(result)
        self.query_params = params
        return params

    def get_paginator(self, queryset, per_page, **kwargs):
        queryset.params['page_size'] = per_page
        return super(ApiParamFilterBackendViewMixin, self).get_paginator(queryset, per_page=per_page, **kwargs)


class ApiSearchPackageViewMixin(object):

    def get_queryset(self):
        api = ApiFactory.factory('search.packageList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        return self.api_list_result_class(api=api, name=self.api_name, params=params)


def pageobj_with_visible_range(page_obj, max_paging_links=10):
    """
    Return a paginated page for the given objects, giving it a custom
    ``visible_page_range`` attribute calculated from ``max_paging_links``.
    """
    page_range = page_obj.paginator.page_range
    if len(page_range) > max_paging_links:
        start = min(page_obj.paginator.num_pages - max_paging_links,
                    max(0, page_obj.number - (max_paging_links // 2) - 1))
        page_range = page_range[start:start + max_paging_links]
    page_obj.visible_page_range = page_range
    return page_obj


def is_ajax_request(request):
    return request.is_ajax() or request.GET.get('is_ajax') or request.POST.get('is_ajax')


def previous_url(request):
    previous = request.META.get('HTTP_REFERER', '')
    host = request.get_host()
    return previous if previous and is_safe_url(previous, host=host) else None


def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.REQUEST.get("next", "")
    host = request.get_host()
    return next if next and is_safe_url(next, host=host) else None


def login_redirect(request):
    next = next_url(request) or ""
    return redirect(next)


from django.views.decorators.cache import cache_page as django_cache_page
from django.utils.decorators import method_decorator

method_cache_page = lambda *args, **kwargs: method_decorator(django_cache_page(*args, **kwargs))


cache_page = django_cache_page
CACHE_APKSITE_ALIAS = 'apksite'
CACHE_APKSITE_TIMEOUT = 0
