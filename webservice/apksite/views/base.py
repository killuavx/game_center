# -*- coding: utf-8 -*-
from apksite.apis import ApiListPaginator, ApiListResultSet


PRODUCT = 'web'


class ApiParamFilterBackendViewMixin(object):

    filter_param_backends = ()

    paginator_class = ApiListPaginator

    api_list_result_class = ApiListResultSet

    def filter_params(self, request, *args, **kwargs):
        params = dict()
        for backend in self.filter_param_backends:
            result = backend().filter_params(request, *args, **kwargs)
            if result:
                params.update(result)
        return params

    def get_paginator(self, queryset, per_page, **kwargs):
        queryset.params['page_size'] = per_page
        return super(ApiParamFilterBackendViewMixin, self).get_paginator(queryset, per_page=per_page, **kwargs)


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