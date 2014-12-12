# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, InvalidPage
from django.http import Http404
from django.views.generic import DetailView, TemplateView, ListView
from apksite.apis import ApiFactory, ApiException, ApiListResultSet, ApiListPaginator, ApiResponseException
from copy import deepcopy

PRODUCT = 'web'

class BaseParamFilterBackend(object):

    def filter_params(self, request, *args, **kwargs):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")


class LanguageParamFilterBackend(BaseParamFilterBackend):

    language_param = 'lang'

    choices = [
        {'code': 'ZH', 'name': '中文'},
        {'code': 'EN', 'name': '英文'},
        ]

    lang_choices = {}
    for c in choices:
        lang_choices[c['code']] = c['code']

    def filter_params(self, request, *args, **kwargs):
        lang = request.GET.get(self.language_param)
        lang = lang.upper() if lang is not None else None
        if lang not in self.lang_choices:
            return dict()
        return dict(language=lang)


class PkgSizeParamFilterBackend(BaseParamFilterBackend):

    M = 1024 * 1024

    G = M * 1024

    size_param = 'size'

    choices = [
        {'code': '0-10m', 'name': '10M以内', 'value': (0, 10*M)},
        {'code': '10-50m', 'name': '10-50M', 'value': (10*M, 50*M)},
        {'code': '50-100m', 'name': '50-100M', 'value': (50*M, 100*M)},
        {'code': '100-300m', 'name': '100-300M', 'value': (100*M, 300*M)},
        {'code': '300-500m', 'name': '300-500M', 'value': (300*M, 500*M)},
        {'code': '500-800m', 'name': '500-800M', 'value': (500*M, 800*M)},
        {'code': '800m-1g', 'name': '800M-1G', 'value': (800*M, 1*G)},
        {'code': '1g', 'name': '1G以上', 'value': (1*G, None)},
        ]

    size_choices = {}
    for c in choices:
        size_choices[c['code']] = c['value']

    def filter_params(self, request, *args, **kwargs):
        size = request.GET.get(self.size_param)
        size = size.lower() if size is not None else None
        if size not in self.size_choices:
            return None
        min_size, max_size = self.size_choices[size]

        size_range = []
        if min_size is not None:
            size_range.append(str(min_size))
        if max_size is not None:
            size_range.append(str(max_size))

        return dict(download_size="-".join(size_range))


class PkgReportsParamFilterBackend(BaseParamFilterBackend):

    reports_param = 'reps'

    choices = [
        {'code': 'no-network', 'name': '无需网络'},
        {'code': 'no-adv', 'name': '无广告'},
        {'code': 'no-gplay', 'name': '无需谷歌市场'},
        {'code': 'no-root', 'name': '无需root权限'},
        ]

    report_choices = {}
    for c in choices:
        report_choices[c['code']] = c['code']

    def filter_params(self, request, *args, **kwargs):
        reps = request.GET.getlist(self.reports_param)
        lookups = {}
        for r in reps:
            r = r.lower()
            if r in self.report_choices:
                name = r.replace('no-', '')
                lookups['reported_%s' % name] = 'false'

        return lookups


class CategoryParamFilterBackend(BaseParamFilterBackend):

    root_category_slugs = ['game', 'application']

    root_slug_param = 'root_slug'

    cat_slug_param = 'category_slug'

    cat_id_param = 'category'

    def filter_params(self, request, *args, **kwargs):
        root_slug = kwargs.get(self.root_slug_param)
        if root_slug and root_slug not in self.root_category_slugs:
            return Http404()

        cat_slug = kwargs.get(self.cat_slug_param)

        cat_id = request.GET.get(self.cat_id_param)
        cat_id = int(cat_id) if str(cat_id).isnumeric() else None
        category_slugs=cat_slug if cat_slug else root_slug
        return dict(
            root_slug=root_slug,
            cat_slug=cat_slug,
            category_slugs=category_slugs if cat_id is None else category_slugs,
            category_id=cat_id,
        )


class TopicParamFilterBackend(BaseParamFilterBackend):

    topic_slug_param = 'topic_slug'

    topic_id_param = 'topic'

    def filter_params(self, request, *args, **kwargs):
        topic_slug = kwargs.get('topic_slug')
        topic_id = request.GET.get('topic')
        topic_id = int(topic_id) if str(topic_id).isnumeric() else None
        return dict(topic_id=topic_id,
                    topic_slug=topic_slug)


class PaginatorParamFilterBackend(BaseParamFilterBackend):

    page_param = 'page'

    def filter_params(self, request, *args, **kwargs):
        page = request.GET.get(self.page_param)
        return dict(page=page)


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


class CategoryView(ApiParamFilterBackendViewMixin, ListView):

    context_object_name = 'packages'
    paginate_by = 27

    api_name = 'web.search.packageList'

    filter_param_backends = (
        CategoryParamFilterBackend,
        TopicParamFilterBackend,
        LanguageParamFilterBackend,
        PkgSizeParamFilterBackend,
        PkgReportsParamFilterBackend,
        PaginatorParamFilterBackend,
    )

    template_name = 'apksite/pages/category/index.haml'

    product = PRODUCT

    def get_template_names(self):
        return [self.template_name]

    def get_queryset(self):
        api = ApiFactory.factory('search.packageList')
        params = self.filter_params(self.request, *self.args, **self.kwargs)
        return self.api_list_result_class(api=api, name=self.api_name, params=params)

    def get_context_data(self, **kwargs):
        kwargs = super(CategoryView, self).get_context_data(**kwargs)
        kwargs['product'] = self.product

        cat_kwargs = self.get_context_category_data(self.request,
                                                    *self.args,
                                                    **self.kwargs)
        kwargs.update(cat_kwargs)

        topic_kwargs = self.get_context_topic_data(self.request,
                                                   *self.args,
                                                   **self.kwargs)
        kwargs.update(topic_kwargs)
        topic_selectlist = self.get_topic_select_list()
        kwargs['topic_selectlist'] = topic_selectlist

        filter_kwargs = self.get_context_filter_select_data(self.request,
                                                            *self.args,
                                                            **self.kwargs)
        kwargs.update(filter_kwargs)
        kwargs['filter_selector'] = self.get_filter_select_list()

        kwargs['page_obj'] = pageobj_with_visible_range(kwargs['page_obj'],
                                                        max_paging_links=10)
        return kwargs

    def get_context_topic_data(self, request, *args, **kwargs):
        backend = TopicParamFilterBackend()
        params = backend.filter_params(self.request, *self.args, **self.kwargs)
        return dict(
            current_topic_id=params['topic_id'],
            current_topic_slug=params['topic_slug'],
        )

    def get_topic_select_list(self):
        return [
            dict(id=0, name='最新发布', slug='release'),
            dict(id=9, name='最热下载', slug='hotdown'),
        ]

    def get_context_filter_select_data(self, request, *args, **kwargs):
        current_reps = [code.lower() for code in request.GET.getlist(PkgReportsParamFilterBackend.reports_param)]
        return dict(
            current_lang=request.GET.get(LanguageParamFilterBackend.language_param),
            current_size=request.GET.get(PkgSizeParamFilterBackend.size_param),
            current_reps=current_reps,
        )

    def get_filter_select_list(self):
        lang_choices = deepcopy(LanguageParamFilterBackend.choices)
        report_choices = deepcopy(PkgReportsParamFilterBackend.choices)
        size_choices = deepcopy(PkgSizeParamFilterBackend.choices)
        return dict(
            langs=lang_choices,
            reports=report_choices,
            sizes=size_choices,
        )

    def get_context_category_data(self, request, *args, **kwargs):
        api = ApiFactory.factory('category.getList')
        backend = CategoryParamFilterBackend()
        params = backend.filter_params(request, *args, **kwargs)

        try:
            res = api.request(parent_slug=params['root_slug'])
            category_list = api.get_response_data(res, name=api.category_name)
        except ApiResponseException as e:
            category_list = []

        data = dict()
        data['category_selectlist'] = category_list
        data['current_category_id'] = params['category_id']
        data['current_root_slug'] = params['root_slug']
        data['current_category_slug'] = params['cat_slug']

        data['current_root'] = None
        for cat in category_list:
            if cat['slug'] == data['current_root_slug']:
                kwargs['current_root'] = cat
                break

        data['current_category'] = None
        for cat in category_list:
            if cat['slug'] == data['current_category_slug'] \
                or cat['id'] == data['current_category_id']:
                data['current_category'] = cat
                break

        return data
