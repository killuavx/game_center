# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from iossite.apis import ApiFactory, ApiResponseException
from iossite.views.base import PRODUCT, CACHE_IOSSITE_TIMEOUT, CACHE_IOSSITE_ALIAS, method_cache_page


class ProductView(TemplateView):

    product = PRODUCT

    template_name = 'iossite/pages/product/index.html'

    def get_context_data(self, **kwargs):
        data = super(ProductView, self).get_context_data(**kwargs)
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


    @method_cache_page(CACHE_IOSSITE_TIMEOUT,
                       cache=CACHE_IOSSITE_ALIAS,
                       key_prefix='product')
    def get(self, request, *args, **kwargs):
        return super(ProductView, self).get(request, *args, **kwargs)
