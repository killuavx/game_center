# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BasePackageSearchListWidget
from website.widgets.pc.base import ProductPropertyWidgetMixin

__all__ = ['PCSearchPackageListWidget']


class PCSearchPackageListWidget(BasePackageSearchListWidget,
                                ProductPropertyWidgetMixin,
                                Widget):
    search_param = 'q'

