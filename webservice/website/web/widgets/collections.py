# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.topic import BaseCollectionTopicListWidget, BaseCollectionTopicListWithPackageWidget
from website.widgets.common.package import BaseTopicalPackageListWidget, BaseTopicalPackageBySearchListWidget
from website.web.widgets.base import ProductPropertyWidgetMixin
from searcher.helpers import get_default_package_query
from searcher.search_results import PackageSearchResult
from toolkit.helpers import get_global_site


__all__ = ['WebCollectionTopicListWithSearchPackageWidget',
           'WebCollectionPackageBySearchListWidget',
           ]


class WebCollectionTopicListWidget(BaseCollectionTopicListWithPackageWidget,
                                   ProductPropertyWidgetMixin,
                                   Widget):

    topic_max_items = 8


class WebCollectionPackageListWidget(BaseTopicalPackageListWidget,
                                     ProductPropertyWidgetMixin,
                                     Widget):
    pass


class WebCollectionTopicListWithSearchPackageWidget(BaseCollectionTopicListWidget,
                                                    ProductPropertyWidgetMixin,
                                                    Widget):

    topic_max_items = 8

    slug = None

    def get_list(self):
        from website.models import TopicProxy
        try:
            topic = TopicProxy.objects.filter(slug=self.slug).published().get()
            return topic.children.published()
        except TopicProxy.DoesNotExist:
            return TopicProxy.objects.none()


class WebCollectionPackageBySearchListWidget(BaseTopicalPackageBySearchListWidget,
                                             ProductPropertyWidgetMixin,
                                             Widget):
    pass
