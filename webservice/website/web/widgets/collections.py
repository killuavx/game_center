# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.topic import BaseCollectionTopicListWidget
from website.widgets.common.package import BaseTopicalPackageListWidget
from website.web.widgets.base import ProductPropertyWidgetMixin


__all__ = ['WebCollectionTopicListWidget', 'WebCollectionPackageListWidget']


class WebCollectionTopicListWidget(BaseCollectionTopicListWidget,
                                   ProductPropertyWidgetMixin,
                                   Widget):

    topic_max_items = 8


class WebCollectionPackageListWidget(BaseTopicalPackageListWidget,
                                     ProductPropertyWidgetMixin,
                                     Widget):
    pass
