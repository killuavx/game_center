# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common import author as awidget
from website.widgets.pc.base import ProductPropertyWidgetMixin

__all__ = ['PCVendorNavListWidget', 'PCVendorPackageListWidget']


class PCVendorNavListWidget(awidget.BaseVendorNavListWidget,
                            ProductPropertyWidgetMixin,
                            Widget):
    per_page = 8


class PCVendorPackageListWidget(awidget.BaseVendorPackageListWidget,
                                ProductPropertyWidgetMixin,
                                Widget):

    per_page = 18

