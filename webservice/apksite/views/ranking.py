# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from apksite.views.base import PRODUCT
from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page


class RankingView(TemplateView):

    template_name = 'apksite/pages/ranking/index.html'

    product = PRODUCT

    RANKING_MAP = {
        # 总榜
        'main': 'c1',
        # 推荐榜
        'tuijianbang': 'c2',
        # 最热榜
        'zuirebang': 'c3',
    }

    root_category_slugs = ['game', 'application']

    cat_slug_param = 'category_slug'

    def filter_params(self, request, *args, **kwargs):
        cat_slug = kwargs.get(self.cat_slug_param, self.root_category_slugs[0])
        if cat_slug and cat_slug not in self.root_category_slugs:
            return Http404()

        return dict(category_slug=cat_slug)

    def get_context_data(self, **kwargs):
        data = super(RankingView, self).get_context_data(**kwargs)
        params = self.filter_params(request=self.request, *self.args, **self.kwargs)
        data['product'] = self.product
        data['rankings'] = self.get_rankings(category_slug=params['category_slug'])
        return data

    def get_rankings(self, category_slug):
        api = ApiFactory.factory('ranking')
        ranking_slugs = ",".join(list(self.RANKING_MAP.keys()))
        res = api.request(category_slug=category_slug, rank_slugs=ranking_slugs)

        rankings = dict()
        try:
            ranking_list = api.get_response_data(response=res, name=api.name)
            for r in ranking_list:
                idx = self.RANKING_MAP.get(r['ranking_slug'])
                if idx:
                    rankings[idx] = r
        except (ApiResponseException, IndexError) as e:
            raise Http404()
        return rankings

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='ranking')
    def get(self, request, *args, **kwargs):
        return super(RankingView, self).get(request, *args, **kwargs)
