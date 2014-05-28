# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from . import base
from .package import BasePackageListWidget


class ItemListByTopicFilterBackend(base.BaseWidgetFilterBackend):

    topic_param = 'topic'

    def filter_queryset(self, request, queryset, widget):
        from taxonomy.models import TopicalItem
        if hasattr(widget, self.topic_param) \
            and getattr(widget, self.topic_param):
            topic = getattr(widget, self.topic_param)
            queryset = TopicalItem.objects \
                .filter_items_by_topic(topic=topic,
                                       item_model=queryset.model,
                                       queryset=queryset)
        else:
            return queryset.none()
        return queryset


class BaseTopicListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        from taxonomy.models import Topic, TopicalItem
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            return topic.children.published()
        except Topic.DoesNotExist:
            return list()


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


class BaseTopicPackageListWidget(BasePackageListWidget):

    filter_backends = (ItemListByTopicFilterBackend, )

    slug = None

    topic = None

    def get_topic(self):
        from taxonomy.models import Topic
        return Topic.objects.filter(slug=self.slug).published().get()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        try:
            self.topic = self.get_topic()
        except ObjectDoesNotExist:
            pass
        return super(BaseTopicPackageListWidget, self)\
            .get_context(value=value, options=options, context=context)
