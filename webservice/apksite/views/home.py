# -*- coding: utf-8 -*-
from copy import deepcopy
from django.http import Http404
from django.utils.datastructures import SortedDict
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import PRODUCT
from apksite.views.topic import MasterpieceFilterBackend
from apksite.views.base import CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page


class BaseWidget(object):

    def __init__(self, view):
        self.view = view

    def request(self):
        pass

    def get_context(self):
        self.request()
        return self


class MasterpieceWidget(BaseWidget):

    template_name = 'apksite/includes/home/roll-masterpiece.haml'

    page_size = 10

    items = None

    def request(self):
        api = ApiFactory.factory('search.packageList')
        params = MasterpieceFilterBackend().filter_params(self.view.request,
                                                          *self.view.args,
                                                          **self.view.kwargs)
        params['page_size'] = self.page_size
        response = api.request(**params)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException:
            result = []

        self.items = result


class FriendLinkWidget(BaseWidget):

    title = '友情链接'

    template_name = 'apksite/includes/home/friend_links.html'

    items = None

    page_size = 100

    def request(self):
        api = ApiFactory.factory('friendLinkList')
        params = dict()
        params['page_size'] = self.page_size
        response = api.request(**params)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        self.items = result


class VendorWidget(BaseWidget):

    title = '厂商'

    template_name = 'apksite/includes/home/vendor-list.haml'

    page_size = 8

    items = None

    def request(self):
        api = ApiFactory.factory('vendor.getList')
        response = api.request(page_size=self.page_size)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        items = []
        page_url = reverse(viewname='vendor')
        for v in result:
            v['url'] = "%s?author=%s" %(page_url, v['id'])
            items.append(v)
        self.items = items
        self.more_url = page_url


class CollectionWidget(BaseWidget):

    title = '合集'

    template_name = 'apksite/includes/home/collections-panel.haml'

    page_size = 8

    items = None

    def request(self):
        api = ApiFactory.factory('collection.getList')
        response = api.request(page_size=self.page_size)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        self.items = result
        self.more_url = self.get_more_url()

    def get_more_url(self):
        return reverse(viewname='collection-list')


class LatestWidget(BaseWidget):

    title = '最新发布'

    template_name = 'apksite/includes/home/latest-list.haml'

    page_size = 10

    items = None

    def request(self):
        api = ApiFactory.factory('latest.releaseList')
        response = api.request(page_size=self.page_size)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        self.items = result
        self.more_url = reverse(viewname='latest')


class BaseTopicPackageListWidget(BaseWidget):

    title = None

    template_name = None

    page_size = None

    items = None

    topic_slug = 'web-home-first-crack'

    def request(self):
        api = ApiFactory.factory('topic.packageList')
        response = api.request(page_size=self.page_size,
                               topic_slugs=self.topic_slug)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        self.items = result
        self.more_url = self.get_more_url()

    def get_more_url(self):
        return reverse(viewname='collection-detail', kwargs=dict(slug=self.topic_slug))


class CrackWidget(BaseTopicPackageListWidget):

    title = '首发破解'

    template_name = 'apksite/includes/home/crack-list.haml'

    page_size = 6


class NetworkWidget(BaseTopicPackageListWidget):

    title = '网游专区'

    template_name = 'apksite/includes/home/network-list.haml'

    page_size = 8

    topic_slug = 'home-network-game'


class BaseRankingWidget(BaseWidget):

    template_name = 'apksite/includes/package/ranking-list.haml'

    title = '总榜'

    more_url = None

    category_slug = None

    ranking_slug = 'main'

    page_size = 10

    def request(self):
        api = ApiFactory.factory('ranking')
        response = api.request(page_size=self.page_size,
                               category_slug=self.category_slug,
                               rank_slugs=self.ranking_slug)
        try:
            ranking = api.get_response_data(response=response, name=api.name)[0]
        except (ApiResponseException, IndexError) as e:
            ranking = None

        self.ranking = ranking
        self.more_url = reverse(viewname='ranking-list',
                                kwargs=dict(category_slug=self.category_slug))


class ApplicationRankingWidget(BaseRankingWidget):

    category_slug = 'application'


class GameRankingWidget(BaseRankingWidget):

    category_slug = 'game'


class BaseCategoryPackagePanelWidget(BaseWidget):

    template_name = 'apksite/includes/home/category-package-panel.haml'

    title = None

    category_slug = None

    topic_slug = 'hotdown'

    topic_id = 9

    topic_name = '最热下载'

    page_size = 27

    groups = None

    def request(self):
        api = ApiFactory.factory('search.packageList')
        groups = SortedDict()
        response = api.request(page_size=self.page_size,
                               category_slugs=self.category_slug)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []

        page_url = reverse('category-%s' % self.category_slug)
        groups['latest'] = dict(
            more_url=page_url,
            name='最新发布',
            packages=result,
        )

        response = api.request(page_size=self.page_size,
                               topic_slug=self.topic_slug,
                               category_slugs=self.category_slug)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []
        groups[self.topic_slug] = dict(
            more_url="%s?topic=%s" %(page_url, self.topic_id),
            name=self.topic_name,
            packages=result,
        )
        self.groups = list(groups.values())


class GamePanelWidget(BaseCategoryPackagePanelWidget):

    title = '游戏'

    category_slug = 'game'


class ApplicationPanelWidget(BaseCategoryPackagePanelWidget):

    title = '软件'

    category_slug = 'application'


class HomeView(TemplateView):

    template_name = 'apksite/pages/home/index.haml'

    banner_slug = None

    product = PRODUCT

    WIDGETS = {
        'masterpiece': MasterpieceWidget,
        'latest': LatestWidget,
        'crack': CrackWidget,
        'network': NetworkWidget,
        'application_ranking': ApplicationRankingWidget,
        'application_panel': ApplicationPanelWidget,
        'game_ranking': GameRankingWidget,
        'game_panel': GamePanelWidget,
        'friendlink': FriendLinkWidget,
        'vendor': VendorWidget,
        'collection': CollectionWidget,
    }

    adv_template_name = 'apksite/includes/single-adv.haml'

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['adv'] = self.get_adv_list()
        data['adv']['template_name'] = self.adv_template_name
        data['widgets'] = self.get_widgets()
        return data

    ADV_MAP = {
        "banner-mainsite": 'banner_list',
        "home-a2": 'a2',
        "home-a3": 'a3',
        "home-a4": 'a4',
        "home-a5": 'a5',
        "home-a6": 'a6',
        "home-a7": 'a7',
    }

    def get_adv_list(self):
        api = ApiFactory.factory('advList')
        place_slugs = list(self.ADV_MAP.keys())
        response = api.request(slugs=",".join(place_slugs))

        all_advs = dict()
        try:
            result = api.get_response_data(response=response, name=api.name)
            for slug, advs in result.items():
                idx = self.ADV_MAP.get(slug)
                if idx:
                    all_advs[idx] = advs
        except ApiResponseException:
            pass
        return all_advs

    def get_widgets(self):
        widgets = dict()
        for key, widget_cls in self.WIDGETS.items():
            widgets[key] = widget_cls(view=self)
        return widgets

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='home')
    def get(self, request, *args, **kwargs):
        return super(HomeView, self).get(request, *args, **kwargs)
