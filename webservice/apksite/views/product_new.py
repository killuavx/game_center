from django.views.generic import TemplateView
from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import PRODUCT, CACHE_APKSITE_TIMEOUT, CACHE_APKSITE_ALIAS, method_cache_page

class ProductHelperView(TemplateView):

    product = PRODUCT

    template_name = 'apksite/pages/product/index-helper.html'

    def get_context_data(self, **kwargs):
        data = super(ProductHelperView, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['clients'] = self.get_client_apps()
        try:
            data['latest'] = data['clients'][0]
        except:
            pass
        return data

    def get_client_apps(self):
        api = ApiFactory.factory('clientList')
        response = api.request()
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []
        return result


    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductHelperView, self).get(request, *args, **kwargs)


class ProductUnionView(TemplateView):

    product = PRODUCT

    template_name = 'apksite/pages/product/index-union.html'

    def get_context_data(self, **kwargs):
        data = super(ProductUnionView, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['clients'] = self.get_client_apps()
        try:
            data['latest'] = data['clients'][0]
        except:
            pass
        return data

    def get_client_apps(self):
        api = ApiFactory.factory('clientList')
        response = api.request()
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []
        return result


    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductUnionView, self).get(request, *args, **kwargs)


class ProductMobileView(TemplateView):

    product = PRODUCT

    template_name = 'apksite/pages/product/mobile-new.html'

    def get_context_data(self, **kwargs):
        data = super(ProductMobileView, self).get_context_data(**kwargs)
        data['product'] = self.product
        return data
        data['clients'] = self.get_client_apps()
        try:
            data['latest'] = data['clients'][0]
        except:
            pass
        return data

    def get_client_apps(self):
        api = ApiFactory.factory('clientList')
        response = api.request()
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = []
        return result


    @method_cache_page(CACHE_APKSITE_TIMEOUT,
                       cache=CACHE_APKSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductMobileView, self).get(request, *args, **kwargs)

