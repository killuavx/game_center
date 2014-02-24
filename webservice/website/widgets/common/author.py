# -*- coding: utf-8 -*-
from warehouse.models import Author
from taxonomy.models import Topic, TopicalItem


class BaseTopicAuthorPanelWidget(object):

    slug = 'spec-top-author'

    more_url = None

    def get_more_url(self):
        return self.more_url

    def get_list(self, slug):
        try:
            topic = Topic.objects.published().get(slug=slug)
            return TopicalItem.objects.get_items_by_topic(topic=topic,
                                                          item_model=Author)
        except (Topic.DoesNotExist, Author.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self.slug)
        max_items = options.get('max_items', 5)
        items = self.get_list(slug=self.slug)
        options.update(
            slug=self.slug,
            title=options.get('title'),
            items=options.get('items', items[0:max_items]),
            max_items=max_items,
            more_url=self.get_more_url()
        )
        return options

