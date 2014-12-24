# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic.list import ListView
from apksite.views.base import ApiParamFilterBackendViewMixin, ApiSearchPackageViewMixin, PRODUCT, pageobj_with_visible_range
from apksite.views.filters import PaginatorParamFilterBackend, BaseParamFilterBackend
from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page


class MasterpieceFilterBackend(BaseParamFilterBackend):

    def filter_params(self, request, *args, **kwargs):
        return dict(topic_slug='masterpiece')


class FillContextViewMixin(object):

    product = PRODUCT

    def get_context_data(self, **kwargs):
        data = super(FillContextViewMixin, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['page_obj'] = pageobj_with_visible_range(data['page_obj'],
                                                      max_paging_links=10)
        return data


class MasterpieceView(ApiParamFilterBackendViewMixin,
                      ApiSearchPackageViewMixin,
                      FillContextViewMixin,
                      ListView):

    context_object_name = 'packages'
    paginate_by = 12

    api_name = 'web.search.packageList'

    filter_param_backends = (
        MasterpieceFilterBackend,
        PaginatorParamFilterBackend,
    )

    template_name = 'apksite/pages/masterpiece/index.html'

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='masterpiece')
    def get(self, request, *args, **kwargs):
        return super(MasterpieceView, self).get(request, *args, **kwargs)


class CollectionView(ApiParamFilterBackendViewMixin,
                     FillContextViewMixin,
                     ListView):

    filter_param_backends = [
        PaginatorParamFilterBackend,
    ]

    paginate_by = 4

    context_object_name = 'topics'

    api_name = 'web.topic.children'

    template_name = 'apksite/pages/collections/index.html'

    def get_queryset(self):
        api = ApiFactory.factory('collection.getList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        return self.api_list_result_class(api=api, name=self.api_name, params=params)

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='collection-list')
    def get(self, request, *args, **kwargs):
        return super(CollectionView, self).get(request, *args, **kwargs)


class CollectionDetailView(ApiParamFilterBackendViewMixin,
                           ListView):
    product = PRODUCT

    template_name = 'apksite/pages/collections/detail.haml'

    paginate_by = 24

    filter_param_backends = [
        PaginatorParamFilterBackend,
    ]

    slug_url_param = 'slug'

    def get_queryset(self):
        api = ApiFactory.factory('topic.packageList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        params['topic_slugs'] = self.kwargs.get(self.slug_url_param)
        return self.api_list_result_class(api=api, name=api.name, params=params)

    def get_object(self):
        api = ApiFactory.factory('topic.info')
        params = dict(slug=self.kwargs.get(self.slug_url_param))
        try:
            res = api.request(**params)
            obj = api.get_response_data(response=res, name=api.name)
        except ApiResponseException:
            raise Http404()

        if not obj:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        data = dict()
        data['topic'] = data['object'] = self.get_object()
        _data = super(CollectionDetailView, self).get_context_data(**kwargs)
        data.update(_data)
        data['product'] = self.product
        data['packages'] = data['object_list'] = self.object_list
        data['page_obj'] = pageobj_with_visible_range(data['page_obj'],
                                                      max_paging_links=10)
        return data

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='collection-detail')
    def get(self, request, *args, **kwargs):
        return super(CollectionDetailView, self).get(request, *args, **kwargs)
