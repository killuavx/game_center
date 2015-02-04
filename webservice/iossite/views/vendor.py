# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import ListView

from iossite.apis import ApiFactory, ApiResponseException
from iossite.views.base import ApiParamFilterBackendViewMixin, pageobj_with_visible_range, PRODUCT
from iossite.views.common import page_not_found
from iossite.views.filters import BaseParamFilterBackend, PaginatorParamFilterBackend
from iossite.views.base import CACHE_IOSSITE_TIMEOUT, CACHE_IOSSITE_ALIAS, method_cache_page


class VendorParamFilterBackend(BaseParamFilterBackend):

    def filter_params(self, request, *args, **kwargs):
        author_id = request.GET.get('author') or kwargs.get('author_id')
        if not author_id:
            raise Http404()
        return dict(author_id=author_id)


class VendorView(ApiParamFilterBackendViewMixin,
                 ListView):

    context_object_name = 'packages'
    paginate_by = 18

    filter_param_backends = (
        VendorParamFilterBackend,
        PaginatorParamFilterBackend,
    )

    template_name = 'iossite/pages/vendor/index.html'

    product = PRODUCT

    def get_queryset(self):
        api = ApiFactory.factory('author.packageList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        return self.api_list_result_class(api=api, name=api.name, params=params)

    def get_vendor_list(self):
        api = ApiFactory.factory('vendor.getList')
        try:
            resposne = api.request()
            vendors = api.get_response_data(response=resposne, name=api.name)
        except ApiResponseException as e:
            raise Http404()

        return vendors

    def get_context_data(self, **kwargs):
        kwargs = super(VendorView, self).get_context_data(**kwargs)
        kwargs['product'] = self.product
        kwargs['page_obj'] = pageobj_with_visible_range(kwargs['page_obj'],
                                                        max_paging_links=10)
        return kwargs

    def pre_context_data(self):
        kwargs = dict()
        kwargs['vendor_list'] = self.get_vendor_list()
        author_id = self.request.GET.get('author') or self.kwargs.get('author_id')
        try:
            if not author_id:
                kwargs['author_id'] = kwargs['vendor_list'][0]['id']
            else:
                self.kwargs['author_id'] = kwargs['author_id'] = int(author_id)
        except:
            raise Http404()
        kwargs['current_author_id'] = kwargs.get('author_id')
        return kwargs

    @method_cache_page(CACHE_IOSSITE_TIMEOUT,
                       cache=CACHE_IOSSITE_ALIAS,
                       key_prefix='vendor')
    def get(self, request, *args, **kwargs):
        try:
            return self._get(request, *args, **kwargs)
        except Http404:
            return page_not_found(request=request)

    def _get(self, request, *args, **kwargs):
        context_kwargs = self.pre_context_data()
        self.kwargs['author_id'] = context_kwargs['author_id']
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404()
        context = self.get_context_data(object_list=self.object_list, **context_kwargs)
        return self.render_to_response(context)
