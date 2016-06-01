# -*- coding: utf-8 -*-
import os
import hashlib
import collections
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

    def __len__(self):
        return len(self._current_object_list) if self._current_object_list else 0


class BaseApi(object):

    SUCCESS_CODE = '0000'

    name = None

    params = None

    def __init__(self, api_url, key, secret):
        self.api_url = api_url
        self.key, self.secret = key, secret

    def request(self, *args, **kwargs):
        req_params = dict()
        for api_key, params in self.get_request_data(**kwargs).items():
            req_params[api_key] = self.filter_params(**params)

        api_params = self.append_token_to_apis(req_params)
        api_url = os.path.join(self.api_url, self.get_multi_api_uri(api_params))
        data_str = json.dumps(api_params)
        response = requests.post(api_url, data=dict(data=data_str))
        if response.status_code != status_codes.OK:
            raise Http404()
        return response

    def get_response_data(self, response, name, success_code=SUCCESS_CODE):
        result = response.json()[name]
        if result.get('code') == success_code:
            return result.get('results')
        else:
            raise ApiResponseException(msg=result.get('msg'),
                                       code=result.get('code'))

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
            raise ApiResponseException(msg="%s: %s" % (result.get('msg'), name),
                                       code=result.get('code'))

    def generate_access_params(self, params):
        api_access = list(dict(
            #apiSecret=self.secret,
            apiKey=self.key,
        ).items())
        return dict(list(params.items()) + api_access)

    def filter_params(self, **kwargs):
        if self.params is None:
            return kwargs
        return dict(filter(lambda x: (x[0] in self.params or x[0] == 'apiKey') and x[1] is not None, kwargs.items()))

    def get_request_data(self, **kwargs):
        data = dict()
        params = deepcopy(self.params)
        params = params if params else dict()
        params.update(kwargs)
        data[self.name] = self.generate_access_params(params)
        return data

    def get_api_secret_token(self, api_name, params):
        if not params:
            params = dict()
        _ordered = collections.OrderedDict(sorted(params.items()))

        _bits = []
        for k, v in _ordered.items():
            _bits.append("=".join([k, str(v)]))
        query_str = "&".join(_bits)
        q2hash = "&".join([query_str, api_name, self.secret])
        token = hashlib.md5(q2hash.encode()).hexdigest()
        return token

    def append_token_to_apis(self, api_params):
        for key, params in api_params.items():
            api_params[key]['token'] = self.get_api_secret_token(key, params)
        return api_params

    def get_multi_api_uri(self, api_params):
        if len(api_params) == 1:
            k = list(api_params.keys())[0]
            token = api_params[k]['token']
            return "/".join([k, token])

        api_names = []
        tokens = []
        for key, params in api_params.items():
            api_names.append(key)
            tokens.append(params['token'])

        ts = "&".join(tokens)
        return "/".join([",".join(api_names),
                         hashlib.md5(ts.encode()).hexdigest()])


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
        'rank_slugs': None,
        'cycle': 0,
    }

    def get_request_data(self, category_slug, rank_slugs='main', *args, **kwargs):
        data = dict()
        data[self.name] = self.generate_access_params(self.params)
        data[self.name]['category'] = category_slug
        data[self.name]['rank_slugs'] = rank_slugs
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

    name = search_name = 'web.search.packageList'
    params = search_params = {
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
        'package_type': None,
    }

    PKG_TYPES = [
        'crack'
    ]

    def get_request_data(self, **kwargs):
        data = dict()
        data[self.search_name] = self.generate_access_params(kwargs)
        return data


class CategoryListApi(BaseApi):

    name = category_name = 'web.category.getLeafsList'
    params = category_params = {
        'parent_id': None,
        'parent_slug': None,
    }

    def get_request_data(self, **kwargs):
        data = dict()
        params = deepcopy(self.params)
        params.update(kwargs)
        data[self.name] = self.generate_access_params(params)
        return data


class CollectionListApi(BaseApi):

    COLLECTION_SLUG = 'ios_spec_title'

    name = 'web.topic.children'
    params = {
        'topic_slug': COLLECTION_SLUG,
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
        'topic_slug': None,
    }


class AdvertisementListApi(BaseApi):

    name = 'web.advertisement.advList'
    params = {
        'slugs': None,
    }


class AuthorPackageListApi(BaseApi):

    name = 'web.topic.authorPackages'
    params = {
        'author_id':None,
        'page': None,
        'page_size': None,
    }


class VendorListApi(BaseApi):

    name = 'web.topic.authors'
    params = {
        'topic_slug': 'ios-spec-top-author',
    }


class PackageLatestListApi(BaseApi):

    name = 'web.package.getReleasedPackages'
    params = {
        'page': 1,
        'page_size': 10,
    }


class PackageCrackListApi(BaseApi):

    name = 'web.category.packages'
    params = {
        'slug': 'crack-game',
        'page': 1,
        'page_size': 150,
    }


class FriendLinkListApi(BaseApi):

    name = 'web.friendlink.linkList'
    params = {
        'slug': 'www',
        'page_size': None,
    }


class ClientListApi(BaseApi):

    name = 'web.ccplayClient.list'
    params = dict(
        packageName='com.ccplay.helper',
        page_size=None,
    )


class UserLoginApi(BaseApi):

    name = 'user.login'
    params = {
        'username': None,
        'password': None,
        'app': None,
    }


class UserProfileApi(BaseApi):

    name = 'user.getProfile'
    params = {
        'user_id': None,
        'authorization_token': None,
    }


class UserRegisterApi(BaseApi):

    SUCCESS_CODE = '0000'

    name = 'user.register'
    params = {
        'signup_type': None,
        'username': None,
        'password': None,
        'email': None,
        'phone': None,
        'code': None,
    }

    def get_response_data(self, response, name, success_code=SUCCESS_CODE):
        return super(UserRegisterApi, self)\
            .get_response_data(response=response,
                               name=name,
                               success_code=success_code)


class UserPostCommentApi(BaseApi):

    SUCCESS_CODE = '0000'

    name = 'user.postComment'
    params = {
        'authorization_token': None,
        # warehouse.packageversion: 17
        'content_type': 17,
        'object_pk': None,
        'comment': None,
        'star': None,
        'ip_address': None,
    }

    def get_response_data(self, response, name, success_code=SUCCESS_CODE):
        return super(UserPostCommentApi, self) \
            .get_response_data(response=response,
                               name=name,
                               success_code=success_code)


class CommentListApi(BaseApi):
    name = 'web.comment.list'
    params = {
        'content_type': None,
        'object_pk': None,
        'page': None,
        'page_size': None,
    }


class ApiFactory(object):

    API_KEY = 'ios_web'

    API_SECRET = '1397eb666b0d7fe6653cb57b872639e3'

    #API_URL = 'http://192.168.1.21/content/'
    API_URL = 'http://10.10.53.176:81/content/'
    #API_URL = 'http://ios-api.ccplay.com.cn/apicenter/'

    API_CLASSES = {
        'detail': PackageDetailApi,
        'ranking': RankingListApi,
        'search.packageList': PackageSearchApi,
        'author.packageList': AuthorPackageListApi,
        'vendor.getList': VendorListApi,
        'category.getList': CategoryListApi,
        'collection.getList': CollectionListApi,
        'topic.info': TopicInfoApi,
        'topic.packageList': TopicPackageListApi,
        'latest.crackList': PackageCrackListApi,
        'latest.releaseList': PackageLatestListApi,

        'comment.list': CommentListApi,
    }

    #COMMON_API_URL = 'http://192.168.1.21/commonservice/'
    COMMON_API_URL = 'http://10.10.53.176:83/commonservice/'
    #COMMON_API_URL = 'http://ios-api.ccplay.com.cn/apicenter/'
    COMMON_API_CLASSES = {
        'advList': AdvertisementListApi,
        'friendLinkList': FriendLinkListApi,
        'clientList': ClientListApi,
    }

    #USER_API_URL = 'http://192.168.1.21/user/'
    USER_API_URL = 'http://10.10.53.176:82/user/'
    #USER_API_URL = 'http://ios-api.ccplay.com.cn/apicenter/'
    USER_API_CLASSES = {
        'user.login': UserLoginApi,
        'user.getProfile': UserProfileApi,
        'user.register': UserRegisterApi,

        'user.postComment': UserPostCommentApi,
    }

    @classmethod
    def factory(cls, name):
        if cls.USER_API_CLASSES.get(name):
            api_cls = cls.USER_API_CLASSES.get(name)
            api_url = cls.USER_API_URL
        elif cls.COMMON_API_CLASSES.get(name):
            api_cls = cls.COMMON_API_CLASSES.get(name)
            api_url = cls.COMMON_API_URL
        elif cls.API_CLASSES.get(name):
            api_cls = cls.API_CLASSES.get(name)
            api_url = cls.API_URL
        else:
            raise ApiNotExists(msg="api %s not exists" % name)
        return api_cls(api_url=api_url,
                       key=cls.API_KEY,
                       secret=cls.API_SECRET)
