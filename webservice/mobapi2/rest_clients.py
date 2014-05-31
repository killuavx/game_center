# -*- coding: utf-8 -*-
import drest


def api_factory(platform, version=2):
    api_url = 'http://%s.ccplay.com.cn/api/v%s/' % (platform, version)

    names = dict(ios='IOS',
                 android='Android')
    platform = platform.lower()
    if platform not in names:
        raise ValueError('platform must in [ios, android]')

    class RestApi(drest.API):
        _platform = platform

        class Meta:
            baseurl = api_url
            extra_headers = {
                'Cache-Control': 'max-age=3600, must-revalidate',
            }

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
