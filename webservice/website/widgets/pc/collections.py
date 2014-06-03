# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.topic import BaseCollectionTopicListWidget
from website.widgets.common.package import BaseTopicalPackageListWidget
from website.widgets.pc.base import ProductPropertyWidgetMixin


__all__ = ['PCCollectionTopicListWidget', 'PCCollectionPackageListWidget']


class PCCollectionTopicListWidget(BaseCollectionTopicListWidget,
                                  ProductPropertyWidgetMixin,
                                  Widget):

    topic_max_items = 8


class PCCollectionPackageListWidget(BaseTopicalPackageListWidget,
                                    ProductPropertyWidgetMixin,
                                    Widget):
    pass
