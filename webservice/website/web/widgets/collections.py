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

    item_orderby_topical = False

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        data = super(WebCollectionTopicListWithSearchPackageWidget, self) \
            .get_context(value=value, options=options,
                         context=context, pagination=pagination)

        sqs = get_default_package_query(PackageSearchResult)\
            .filter(site=get_global_site().pk)
        for topic in data['items']:
            item_qs = sqs.filter(topic_ids=topic.pk)
            topic.packages_count = item_qs.count()
            if self.item_orderby_topical:
                topic.packages = item_qs.order_by('topic_%d_ordering_i'%topic.pk)[0:self.topic_max_items]
            else:
                topic.packages = item_qs.order_by('-released_datetime')[0:self.topic_max_items]
        return data


class WebCollectionPackageBySearchListWidget(BaseTopicalPackageBySearchListWidget,
                                             ProductPropertyWidgetMixin,
                                             Widget):
    pass
