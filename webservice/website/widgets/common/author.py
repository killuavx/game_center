# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from warehouse.models import Author
from taxonomy.models import Topic, TopicalItem
from . import base


class BaseTopicAuthorPanelWidget(base.BaseListWidget):

    slug = 'spec-top-author'

    def get_more_url(self):
        return reverse('mezzanine.pages.views.page', kwargs=dict(slug='developers'))

    def get_list(self):
        slug = self.slug
        try:
            topic = Topic.objects.published().get(slug=slug)
            return TopicalItem.objects.get_items_by_topic(topic=topic,
                                                          item_model=Author)
        except (Topic.DoesNotExist, Author.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self.slug)
        options.update(dict(
            slug=self.slug,
        ))
        return super(BaseTopicAuthorPanelWidget, self)\
            .get_context(value=value, options=options, context=context)

