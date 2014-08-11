# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BaseTopicalPackageListWidget, BaseTopicalPackageBySearchListWidget
from website.web.widgets.base import ProductPropertyWidgetMixin
from website.widgets.common import filters

__all__ = ['WebMasterpiecePackageBySearchListWidget']


class WebMasterpiecePackageListWidget(BaseTopicalPackageListWidget,
                                      ProductPropertyWidgetMixin,
                                      Widget):
    pass


class WebMasterpiecePackageBySearchListWidget(BaseTopicalPackageBySearchListWidget,
                                              ProductPropertyWidgetMixin,
                                              Widget):
    filter_backends = (
        filters.SearchByTopicFilterBackend,
        filters.SearchOrderByTopicalFilterBackend,
    )
