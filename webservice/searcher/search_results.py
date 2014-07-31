# -*- coding: utf-8 -*-
from haystack.models import SearchResult
from toolkit.model_url_mixin import PackageAbsoluteUrlMixin


class PackageSearchResult(SearchResult, PackageAbsoluteUrlMixin):

    def _get_module_name(self):
        return 'package'

    # for ios
    @property
    def is_free(self):
        return self.is_free_b

    @property
    def formatted_price(self):
        return self.formatted_price_s

    @property
    def support_ipad(self):
        return self.support_ipad_b

    @property
    def support_iphone(self):
        return self.support_iphone_b

    @property
    def support_idevices(self):
        return self.support_idevices_b
