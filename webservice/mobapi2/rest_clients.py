# -*- coding: utf-8 -*-
import drest
from toolkit import helpers


def api_factory(platform, version=2):
    names = dict(ios='IOS',
                 android='Android')
    platform = platform.lower()
    if platform not in names:
        raise ValueError('platform must in [ios, android]')

    if platform == 'android':
        site = helpers.get_global_site(helpers.SITE_ANDROID)
    elif platform == 'ios':
        site = helpers.get_global_site(helpers.SITE_IOS)
    api_url = 'http://%s/api/v%s/' % (site.domain, version)

    class RestApi(drest.API):
        _platform = platform

        def auth(self, token_key=None, *args, **kwargs):
            key = 'Authorization'
            if token_key:
                value = 'Token %s' % token_key
                self.request.add_header(key, value)
            else:
                if hasattr(self.request, 'remove_header'):
                    self.request.remove_header(key)
                elif hasattr(self.request, 'headers'):
                    del self.request.headers[key]

        class Meta:
            trailing_slash = True
            baseurl = api_url

    api = RestApi()
    api.add_resource('packages')
    api.add_resource('topics')
    api.add_resource('search')
    api.add_resource('advertisements')
    api.add_resource('rankings')
    api.add_resource('authors')
    api.add_resource('categories')
    api.add_resource('activities')
    api.add_resource('bulletins')
    return api

ios_api = api_factory('ios')
android_api = api_factory('android')


class AndroidHomeApi(object):
    _api = android_api
    # 精选应用列表
    _get_recommend_list = lambda self: self._api.packages.get(params=dict(
        topic_slug='home-recommend-game',
        ordering='topical'
    ))
    recommend_list = property(_get_recommend_list)
    # 精选广告
    _get_recommend_advs = lambda self: self._api.advertisements.get(params=dict(
        place='home-recommend-game'
    ))
    recommend_advs = property(_get_recommend_advs)
    # 网络游戏列表
    _get_netgame_list = lambda self: self._api.packages.get(params=dict(
        topic_slug='home-network-game',
        ordering='topical'
    ))
    netgame_list = property(_get_netgame_list)
    # 网络游戏广告
    _get_netgame_advs = lambda self: self._api.advertisements.get(params=dict(
        place='home-network-game'
    ))
    netgame_advs = property(_get_netgame_advs)

android_home_api = AndroidHomeApi()
