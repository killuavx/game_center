# -*- coding: utf-8 -*-
import json
from django.http import Http404
import requests
from requests import codes as status_codes
from copy import deepcopy
from django.core.paginator import Paginator, Page


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


class ApiListResultSet(object):

    def __init__(self, api, name, params):
        self.api = api
        self.name = name
        self.params = params

        self._count = None
        self._current_object_list = None
        self._current_page = None
        self._total_pages = None
        self._page_size = None

    def _request(self):
        response = self.api.request(**self.params)
        response_list = self.api.get_response_list(response=response,
                                                   name=self.name)
        self._count = response_list['count']
        self._current_object_list = response_list['object_list']
        self._current_page = response_list['current_page']
        self._page_size = response_list['page_size']
        self._total_pages = response_list['total_pages']

    def count(self):
        if self._count is None:
            self._request()
        return self._count

    def page_result(self, number):
        if number == self.current_page():
            return self

        cls = self.__class__
        return cls(api=self.api, name=self.name, params=self.params)

    def num_pages(self):
        if self._total_pages is None:
            self._request()
        return self._total_pages

    def current_page(self):
        if self._current_page is None:
            self._request()
        return self._current_page

    def page_size(self):
        if self._page_size is None:
            self._request()
        return self._page_size

    def __bool__(self):
        return bool(self.count())

    def __iter__(self):
        if self._current_object_list is None:
            self._request()
        return iter(self._current_object_list)


class BaseApi(object):

    SUCCESS_CODE = '0000'

    def __init__(self, api_url, key, secret):
        self.api_url = api_url
        self.key, self.secret = key, secret

    def get_request_data(self, *args, **kwargs):
        raise NotImplementedError()

    def request(self, *args, **kwargs):
        data_str = json.dumps(self.get_request_data(*args, **kwargs))
        response = requests.post(self.api_url, data=dict(data=data_str))
        if response.status_code != status_codes.OK:
            raise Http404()
        return response

    def get_response_data(self, response, name):
        result = response.json()[name]
        if result.get('code') == self.SUCCESS_CODE:
            return result.get('results')
        else:
            raise ApiResponseException(msg=result.get('msg'), code=result.get('code'))

    def get_response_list(self, response, name):
        result = response.json()[name]
        if result.get('code') == self.SUCCESS_CODE:
            current_page = result.get('curPage')
            page_size = result.get('pageSize')
            total_pages = result.get('totalPages')
            count = result.get('count')
            object_list = result.get('results', list())
            return dict(
                current_page=current_page if current_page else 1,
                page_size=page_size if page_size else 1,
                total_pages=total_pages if total_pages else 1,
                count=count if count else 0,
                object_list=object_list if object_list else list(),
            )
        else:
            raise ApiResponseException(msg=result.get('msg'), code=result.get('code'))

    def generate_access_params(self, params):
        api_access = list(dict(
            apiSecret=self.secret,
            apiKey=self.key,
            ).items())
        return dict(list(params.items()) + api_access)

    def filter_params(self, **kwargs):
        return dict(filter(lambda x: x[0] in self.params and x[1] is not None, kwargs.items()))

    def get_request_data(self, **kwargs):
        data = dict()
        params = deepcopy(self.params)
        params.update(kwargs)
        params = self.generate_access_params(params)
        data[self.name] = self.generate_access_params(params)
        return data


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

    name = ranking_name = 'web.rank.list'
    params = ranking_params = {
        'category': None,
        'rank_slug': None,
        'cycle': 0,
    }

    def get_request_data(self, category_slug, rank_slug='main', *args, **kwargs):
        data = dict()
        data[self.name] = self.generate_access_params(self.params)
        data[self.name]['category'] = category_slug
        data[self.name]['rank_slug'] = rank_slug
        return data


class ApiListPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        super(ApiListPaginator, self).__init__(*args, **kwargs)
        self.object_list.params['page_size'] = self.per_page

    def _get_count(self):
        return self.object_list.count()

    count = property(_get_count)

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        result = self.object_list.page_result(number)
        return Page(object_list=result, number=number, paginator=self)

    def _get_num_pages(self):
        return self.object_list.num_pages()

    num_pages = property(_get_num_pages)


class PackageSearchApi(BaseApi):

    search_name = 'web.search.packageList'
    search_params = {
        'q': None,
        'language': None,
        'download_size': None,
        'reported_network': None,
        'reported_adv': None,
        'reported_root': None,
        'reported_gplay': None,
        'category_id': None,
        'category_slugs': None,
        'category_name': None,
        'topic_id': None,
        'topic_slug': None,
        'topic_name': None,
        'page': None,
        'page_size': None,
    }

    def filter_params(self, **kwargs):
        return dict(filter(lambda x: x[0] in self.search_params and x[1] is not None, kwargs.items()))

    def get_request_data(self, **kwargs):
        data = dict()
        search_params = self.generate_access_params(kwargs)
        data[self.search_name] = self.generate_access_params(search_params)
        return data


class CategoryListApi(BaseApi):

    category_name = 'web.category.getList'
    category_params = {
        'parent_id': None,
        'parent_slug': None,
        'recursive_flag': 'true',
    }

    def filter_params(self, **kwargs):
        return dict(filter(lambda x: x[0] in self.category_params and x[1] is not None, kwargs.items()))

    def get_request_data(self, **kwargs):
        data = dict()
        params = deepcopy(self.category_params)
        params.update(kwargs)
        data[self.category_name] = self.generate_access_params(params)
        return data


class CollectionListApi(BaseApi):

    COLLECTION_SLUG = 'spec-choice-topic'

    name = 'web.topic.children'
    params = {
        'slug': COLLECTION_SLUG,
        'item_size': 10,
        'page': 1,
        'page_size':None,
    }


class TopicPackageListApi(BaseApi):

    name = 'web.topic.package'
    params = {
        'topic_slugs': None,
        'page': 1,
        'page_size':24,
    }


class TopicInfoApi(BaseApi):

    name = 'web.topic.info'
    params = {
        'slug': None,
    }


class ApiFactory(object):

    API_KEY = 'android.ccplay.com.cn'

    API_SECRET = 'e10adc3949ba59abbe56e057f20f883e'

    API_URL = 'http://192.168.5.101/content/'

    API_CLASSES = {
        'detail': PackageDetailApi,
        'ranking': RankingListApi,
        'search.packageList': PackageSearchApi,
        'category.getList': CategoryListApi,
        'collection.getList': CollectionListApi,
        'topic.info': TopicInfoApi,
        'topic.packageList': TopicPackageListApi,
    }

    @classmethod
    def factory(cls, name):
        api_cls = cls.API_CLASSES.get(name)
        if not api_cls:
            raise ApiNotExists(msg="api %s not exists" % name)
        return api_cls(api_url=cls.API_URL,
                       key=cls.API_KEY,
                       secret=cls.API_SECRET)


