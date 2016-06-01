# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common import author as awidget
from website.web.widgets.base import ProductPropertyWidgetMixin

__all__ = ['WebVendorNavListWidget',
           'WebVendorPackageBySearchListWidget',
           ]


class WebVendorNavListWidget(awidget.BaseVendorNavListWidget,
                             ProductPropertyWidgetMixin,
                             Widget):
    per_page = 8


class WebVendorPackageListWidget(awidget.BaseVendorPackageListWidget,
                                 ProductPropertyWidgetMixin,
                                 Widget):

    per_page = 18


class WebVendorPackageBySearchListWidget(awidget.BaseVendorPackageBySearchListWidget,
                                         ProductPropertyWidgetMixin,
                                         Widget):

    per_page = 18

