# -*- coding: utf-8 -*-
import json
from django.http import Http404
import requests
from requests import codes as status_codes


class ApiException(Exception):

    def __init__(self, msg=None, code=None):
        self.msg, self.code = msg, code

    def __str__(self):
        return self.msg


class ApiRequestException(ApiException):
    pass


class ApiResponseException(ApiException):
    pass


class ApiNotExists(ApiException):
    pass


class BaseApi(object):

    SUCCESS_CODE = '0000'

    def __init__(self, api_url, key, secret):
        self.api_url = api_url
        self.key, self.secret = key, secret

    def get_request_data(self, *args, **kwargs):
        raise NotImplementedError()

    def request(self, *args, **kwargs):
        response = requests.post(self.api_url,
                                 data=dict(data=json.dumps(self.get_request_data(*args, **kwargs))))
        if response.status_code != status_codes.OK:
            raise Http404()
        return response

    def get_response_data(self, response, name):
        result = response.json()[name]
        if result.get('code') == self.SUCCESS_CODE:
            return result['results']
        else:
            raise ApiException(msg=result.get('msg'), code=result.get('code'))

    def generate_access_params(self, params):
        api_access = list(dict(
            apiSecret=self.secret,
            apiKey=self.key,
            ).items())
        return dict(list(params.items()) + api_access)


class PackageDetailApi(BaseApi):

    detail_name = 'web.package.detail'
    detail_params = {
        'id': None,
    }

    related_name = 'web.package.relatedpackages'
    related_params = {
        'id': None,
        'page_size': 10,
    }

    def get_request_data(self, pk, *args, **kwargs):
        data = dict()
        data[self.detail_name] = self.generate_access_params(self.detail_params)
        data[self.detail_name]['id'] = pk

        data[self.related_name] = self.generate_access_params(self.related_params)
        data[self.related_name]['id'] = pk
        return data


class RankingListApi(BaseApi):

    ranking_name = 'web.rank.list'
    ranking_params = {
        'category': None,
        'ranking_slug': None,
    }

    def get_request_data(self, category_slug, ranking_slug='main', *args, **kwargs):
        data = dict()
        data[self.ranking_name] = self.generate_access_params(self.ranking_params)
        data[self.ranking_name]['category'] = category_slug
        data[self.ranking_name]['ranking_slug'] = ranking_slug
        return data


class ApiFactory(object):

    API_KEY = 'android.ccplay.com.cn'

    API_SECRET = 'e10adc3949ba59abbe56e057f20f883e'

    API_URL = 'http://192.168.5.101/content/'

    API_CLASSES = {
        'detail': PackageDetailApi,
        'ranking': RankingListApi,
    }

    @classmethod
    def factory(cls, name):
        api_cls = cls.API_CLASSES.get(name)
        if not api_cls:
            raise ApiNotExists(msg="api %s not exists" % name)
        return api_cls(api_url=cls.API_URL,
                       key=cls.API_KEY,
                       secret=cls.API_SECRET)


