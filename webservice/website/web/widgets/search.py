# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BasePackageSearchListWidget
from website.widgets.common.category import BaseCategorySelectorWithPackageSearchCountWidget
from website.web.widgets.base import ProductPropertyWidgetMixin

__all__ = ['WebSearchPackageListWidget', 'WebSearchCategorySelectorWidget']


class WebSearchPackageListWidget(BasePackageSearchListWidget,
                                 ProductPropertyWidgetMixin,
                                 Widget):
    search_param = 'q'


class WebSearchCategorySelectorWidget(ProductPropertyWidgetMixin,
                                      BaseCategorySelectorWithPackageSearchCountWidget,
                                      Widget):

    def get_second_selectlist(self, slugs=None, **kwargs):
        return list()
