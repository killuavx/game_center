# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from apksite.views.base import ApiParamFilterBackendViewMixin, ApiSearchPackageViewMixin, PRODUCT, pageobj_with_visible_range
from apksite.views.filters import PaginatorParamFilterBackend, BaseParamFilterBackend


class MasterpieceFilterBackend(BaseParamFilterBackend):

    def filter_params(self, request, *args, **kwargs):
        return dict(topic_slug='masterpiece')


class MasterpieceView(ApiParamFilterBackendViewMixin,
                      ApiSearchPackageViewMixin,
                      ListView):

    context_object_name = 'packages'
    paginate_by = 12

    api_name = 'web.search.packageList'

    filter_param_backends = (
        MasterpieceFilterBackend,
        PaginatorParamFilterBackend,
    )

    template_name = 'apksite/pages/masterpiece/index.html'

    product = PRODUCT

    def get_context_data(self, **kwargs):
        data = super(MasterpieceView, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['page_obj'] = pageobj_with_visible_range(data['page_obj'],
                                                      max_paging_links=10)
        return data
