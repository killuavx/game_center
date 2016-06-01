# -*- coding: utf-8 -*-
from django.utils.timezone import now
from . import base


class BaseTopicListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        from taxonomy.models import Topic
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            qs = topic.children.published()
            return qs
        except Topic.DoesNotExist:
            return Topic.objects.none()

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        return super(BaseTopicListWidget, self).get_context(value=value,
                                                     options=options,
                                                     context=context,
                                                     pagination=pagination)


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


class BaseCollectionTopicListWidget(base.FilterWidgetMixin, BaseTopicListWidget):

    filter_backends = (
        base.OrderingFitler,
    )

    ordering = ('-released_datetime', )

    topic_max_items = 8

    def get_list(self):
        qs = super(BaseCollectionTopicListWidget, self).get_list()
        return self.filter_queryset(qs)


class BaseCollectionTopicListWithPackageWidget(BaseCollectionTopicListWidget):

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        data = super(BaseCollectionTopicListWithPackageWidget, self)\
            .get_context(value=value, options=options, context=context, pagination=pagination)
        for topic in data['items']:
            topic.packages = topic.get_packages().published()[0:self.topic_max_items]
            topic.packages_count = topic.get_packages().published().count()
        return data
