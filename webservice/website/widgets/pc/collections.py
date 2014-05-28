# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.topic import BaseTopicListWidget, BaseTopicPackageListWidget


__all__ = ['PCCollectionTopicListWidget', 'PCCollectionPackageListWidget']


class PCCollectionTopicListWidget(BaseTopicListWidget, Widget):

    topic_max_items = 8

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.slug = options.get('slug')
        data = super(PCCollectionTopicListWidget, self)\
            .get_context(value=value,
                         options=options,
                         context=context,
                         pagination=pagination)

        from taxonomy.models import TopicalItem
        from warehouse.models import Package
        for topic in data['items']:
            packages = TopicalItem.objects.get_items_by_topic(topic, Package).published()
            topic.packages = packages[0:self.topic_max_items]
            topic.packages_count = packages.count()

        return data


class PCCollectionPackageListWidget(BaseTopicPackageListWidget, Widget):
    pass
