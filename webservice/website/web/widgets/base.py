# -*- coding: utf-8 -*-
from django.conf import settings


class ProductPropertyWidgetMixin(object):

    def _get_product(self):
        ETS = settings.ENTRY_TYPES()
        if not hasattr(self, '_product'):
            self._product = ETS.web
        return self._product

    def _set_product(self, product):
        if product:
            self._product = product

    product = property(_get_product, _set_product)

