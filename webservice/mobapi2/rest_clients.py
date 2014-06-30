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
    return api

ios_api = api_factory('ios')
android_api = api_factory('android')

