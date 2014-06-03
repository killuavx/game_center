# -*- coding: utf-8 -*-
from django.utils.timezone import now
from . import base


class BaseTopicListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        from taxonomy.models import Topic
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            return topic.children.published()
        except Topic.DoesNotExist:
            return Topic.objects.none()


class BaseTopicInformationWidget(object):

    slug = None

    def get_topic_informations(self):
        from taxonomy.models import Topic, TopicalItem
        from warehouse.models import Package
        timenow = now()
        topic = Topic.objects.filter(slug=self.slug).published().get()
        qs = TopicalItem.objects \
            .get_items_by_topic(topic=topic, item_model=Package).published()

        total_items_count = qs.count()
        month_items_count = qs.filter(released_datetime__month=timenow.month,
                                      released_datetime__year=timenow.year).count()
        return dict(
            topic=topic,
            total_items_count=total_items_count,
            month_items_count=month_items_count
        )

    def get_context(self, value=None, options=dict(), context=dict()):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        options.update(self.get_topic_informations())
        return options



class BaseCollectionTopicListWidget(BaseTopicListWidget):

    topic_max_items = 8

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.slug = options.get('slug')
        data = super(BaseCollectionTopicListWidget, self) \
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
