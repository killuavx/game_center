# -*- coding: utf-8 -*-
from website.widgets.common.package import BaseCategoryComplexPackageList
from website.widgets.pc.base import ProductPropertyWidgetMixin
from website.widgets.common.category import BaseCategorySelectorWidget
from django_widgets import Widget


__all__ = ['PCCategorySelectorWidget', 'PCCategoryComplexPackageList']


class PCCategorySelectorWidget(ProductPropertyWidgetMixin,
                               BaseCategorySelectorWidget,
                               Widget):
    pass


class PCCategoryComplexPackageList(BaseCategoryComplexPackageList,
                                   ProductPropertyWidgetMixin,
                                   Widget):
    pass
