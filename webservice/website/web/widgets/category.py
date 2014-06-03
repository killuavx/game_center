# -*- coding: utf-8 -*-
from website.widgets.common.package import BaseCategoryComplexPackageList
from website.web.widgets.base import ProductPropertyWidgetMixin
from website.widgets.common.category import BaseCategorySelectorWidget
from django_widgets import Widget


__all__ = ['WebCategorySelectorWidget', 'WebCategoryComplexPackageList']


class WebCategorySelectorWidget(ProductPropertyWidgetMixin,
                                BaseCategorySelectorWidget,
                                Widget):
    pass


class WebCategoryComplexPackageList(BaseCategoryComplexPackageList,
                                    ProductPropertyWidgetMixin,
                                    Widget):
    pass
