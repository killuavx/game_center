from django.views.generic import TemplateView
from django.http import Http404
from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import PRODUCT, CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page
from toolkit.ios_apis import ApiFactory as IOSApiFactory, ApiResponseException as IOSApiResponseException


IOS_LAST_HELPER = dict(
    platformName='苹果版',
    versionName='1.0.3',
    releasedDatetime='2015-08-12',
    whatsnew="""1.全新界面风格，视觉更美观；
2.海量资源，一触即得；
3.随时随地，发现世界的精彩；
4.独家首发，抢先体验巨作；
5.精选专题，玩机生活精品不断。""",
    download='http://itunes.apple.com/cn/app/id1017180641?mt=8',
)

class ProductTimeLineView(TemplateView):
    product = PRODUCT

    iosclient_package_name = None

    androidclient_package_name = None

    def get_ios_client_apps(self):
        if not self.iosclient_package_name:
            return []

        api = IOSApiFactory.factory('clientList')
        response = api.request(packageName=self.iosclient_package_name)
        try:
            result = api.get_response_data(response=response, name=api.name)
            for app in result:
                app['platformName'] = '苹果版'
        except IOSApiResponseException as e:
            result = []
        return result

    def get_android_client_apps(self):
        if not self.androidclient_package_name:
            return []

        api = ApiFactory.factory('clientList')
        response = api.request(packageName=self.androidclient_package_name)
        try:
            result = api.get_response_data(response=response, name=api.name)
            for app in result:
                app['platformName'] = '安卓版'
        except ApiResponseException as e:
            result = []
        return result

    def merge_client_apps(self, ioslist, apklist):
        apps = ioslist + apklist
        new_apps = sorted(apps, key=lambda x: x['releasedDatetime'], reverse=True)
        return new_apps

    def get_last_client_app(self, apps):
        try:
            return apps[0]
        except:
            pass

    def get_context_data(self, **kwargs):
        data = super(ProductTimeLineView, self).get_context_data(**kwargs)
        try:
            data['product'] = self.product
            data['ios_clients'] = self.get_ios_client_apps()
            data['android_clients'] = self.get_android_client_apps()
            data['clients'] = self.merge_client_apps(data['ios_clients'], data['android_clients'])
            data['ios_last'] = self.get_last_client_app(data['ios_clients'])
            data['android_last'] = self.get_last_client_app(data['android_clients'])
        except Exception as e:
            pass
        return data


class ProductHelperView(ProductTimeLineView):

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductHelperView, self).get(request, *args, **kwargs)


    template_name = 'apksite/pages/product/index-helper.html'

    iosclient_package_name = 'com.ccplay.helper'

    androidclient_package_name = 'com.lion.market'

    def get_ios_client_apps(self):
        return [IOS_LAST_HELPER]


class ProductUnionView(ProductTimeLineView):

    template_name = 'apksite/pages/product/index-union.html'

    iosclient_package_name = None

    androidclient_package_name = 'com.lion.gameUnion'

    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductUnionView, self).get(request, *args, **kwargs)

    def get_ios_client_apps(self):
        return []


class ProductMobileView(TemplateView):

    product = PRODUCT

    template_name = 'apksite/pages/product/mobile-new.html'

    ios_helper_package_name = 'com.ccplay.helper'

    ios_union_package_name = None

    android_helper_package_name = 'com.lion.market'

    android_union_package_name = 'com.lion.gameUnion'

    def get_client_api(self, platform):
        if platform  == 'ios':
            api = IOSApiFactory.factory('clientList')
        else:
            api = ApiFactory.factory('clientList')
        return api

    def get_last_app(self, api, package_name, platformName=''):
        if not package_name:
            return None
        response = api.request(packageName=package_name, page_size=1)
        try:
            result = api.get_response_data(response=response, name=api.name)
            app = result[0]
            app['platformName'] = platformName
            return app
        except IOSApiResponseException as e:
            return None
        except:
            return None

    def get_ios_last_app(self, *args, **kwargs):
        return IOS_LAST_HELPER

    def get_context_data(self, **kwargs):
        from django.core.urlresolvers import reverse

        data = super(ProductMobileView, self).get_context_data(**kwargs)
        data['product'] = self.product

        ios_api = self.get_client_api('ios')
        platformName = '苹果版'
        #data['ios_helper'] = None # self.get_last_app(ios_api, self.ios_helper_package_name, platformName)
        data['ios_helper'] = self.get_ios_last_app()
        data['ios_union'] = None # self.get_last_app(ios_api, self.ios_union_package_name, platformName)

        api = self.get_client_api('android')
        platformName = '安卓版'
        data['android_helper'] = self.get_last_app(api, self.android_helper_package_name, platformName)
        data['android_union'] = self.get_last_app(api, self.android_union_package_name, platformName)
        return data


    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductMobileView, self).get(request, *args, **kwargs)

