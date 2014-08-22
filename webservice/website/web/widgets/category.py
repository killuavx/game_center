# -*- coding: utf-8 -*-
from website.widgets.common.package import BaseCategoryComplexPackageList,\
    BaseCategoryComplexPackageBySearchListWidget
from website.web.widgets.base import ProductPropertyWidgetMixin
from website.widgets.common.category import BaseCategorySelectorWithPackageSearchCountWidget
from django_widgets import Widget


__all__ = ['WebCategorySelectorWidget', 'WebCategoryComplexPackageList', 'WebCategoryComplexPackageBySearchList']



class WebCategorySelectorWidget(ProductPropertyWidgetMixin,
                                BaseCategorySelectorWithPackageSearchCountWidget,
                                Widget):
    pass


class WebCategoryComplexPackageList(BaseCategoryComplexPackageList,
                                    ProductPropertyWidgetMixin,
                                    Widget):
    pass


class WebCategoryComplexPackageBySearchList(BaseCategoryComplexPackageBySearchListWidget,
                                            ProductPropertyWidgetMixin,
                                            Widget):
    pass
