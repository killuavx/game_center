# -*- coding: utf-8 -*-
from taxonomy.models import Topic


class BaseTopicWidget(object):

    slug = 'spec-choice-topic'

    more_url = None

    def get_more_url(self):
        return self.more_url

    def get_list(self, slug):
        if slug is None:
            return list()
        try:
            topic = Topic.objects.published().get(slug=slug)
            return topic.children.published()
        except Topic.DoesNotExist:
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        max_items = options.get('max_items', 5)
        slug = options.get('slug', self.slug)
        items = self.get_list(slug=slug)
        options.update(
            more_url=self.get_more_url(),
            max_items=max_items,
            items=items[0:max_items]
        )
        return options
