# -*- coding: utf-8 -*-
from copy import deepcopy
from django.http import Http404
from django.views.generic import ListView

from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import ApiParamFilterBackendViewMixin, ApiSearchPackageViewMixin, pageobj_with_visible_range, PRODUCT
from apksite.views.filters import BaseParamFilterBackend, LanguageParamFilterBackend, PkgSizeParamFilterBackend, PkgReportsParamFilterBackend, PaginatorParamFilterBackend
from apksite.views.base import CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page
from apksite.views.common import page_not_found


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


class CategoryView(ApiParamFilterBackendViewMixin,
                   ApiSearchPackageViewMixin,
                   ListView):

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

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='category')
    def get(self, request, *args, **kwargs):
        try:
            return super(CategoryView, self).get(request, *args, **kwargs)
        except Http404:
            return page_not_found(request=request)


class SearchCategoryParamFilterBackend(BaseParamFilterBackend):

    root_category_slugs = ['game', 'application']

    root_param = 'cat'

    query_param = 'q'

    def filter_params(self, request, *args, **kwargs):
        q = request.GET.get(self.query_param)
        if q is None:
            raise Http404()

        root_slug = request.GET.get(self.root_param)
        root_slug = root_slug if root_slug in self.root_category_slugs else self.root_category_slugs[0]

        return dict(
            q=q,
            root_slug=root_slug,
            cat_slug=root_slug,
            category_slugs=root_slug,
            category_id=None,
        )


class SearchView(CategoryView):

    template_name = 'apksite/pages/category/search.haml'

    filter_param_backends = (
        SearchCategoryParamFilterBackend,
        LanguageParamFilterBackend,
        PkgSizeParamFilterBackend,
        PkgReportsParamFilterBackend,
        PaginatorParamFilterBackend,
    )

    def get_context_category_data(self, request, *args, **kwargs):
        api = ApiFactory.factory('category.getList')
        backend = SearchCategoryParamFilterBackend()
        params = backend.filter_params(request, *args, **kwargs)

        try:
            res = api.request(parent_slug=params['root_slug'])
            category_list = api.get_response_data(res, name=api.category_name)
        except ApiResponseException as e:
            category_list = []

        data = dict()
        data['category_selectlist'] = category_list
        #data['current_category_id'] = params['category_id']
        data['current_root_slug'] = params['root_slug']
        data['current_category_slug'] = params['cat_slug']

        data['current_root'] = None
        for cat in category_list:
            if cat['slug'] == data['current_root_slug']:
                kwargs['current_root'] = cat
                break

        data['current_category'] = None
        for cat in category_list:
            if cat['slug'] == data['current_category_slug']:
                data['current_category'] = cat
                break

        return data

    def get_context_data(self, **kwargs):
        kwargs = super(ListView, self).get_context_data(**kwargs)
        kwargs['product'] = self.product

        cat_kwargs = self.get_context_category_data(self.request,
                                                    *self.args,
                                                    **self.kwargs)
        kwargs.update(cat_kwargs)
        filter_kwargs = self.get_context_filter_select_data(self.request,
                                                            *self.args,
                                                            **self.kwargs)
        kwargs.update(filter_kwargs)
        kwargs['filter_selector'] = self.get_filter_select_list()

        kwargs['page_obj'] = pageobj_with_visible_range(kwargs['page_obj'],
                                                        max_paging_links=10)
        return kwargs

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='search')
    def get(self, request, *args, **kwargs):
        try:
            return super(SearchView, self).get(request, *args, **kwargs)
        except Http404:
            return page_not_found(request=request)
