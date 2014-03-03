# -*- coding: utf-8 -*-
from taxonomy.models import Topic, TopicalItem
from . import base
from warehouse.models import Package
from django.utils.timezone import now
from django_widgets import Widget


class BaseTopicWidget(base.BaseListWidget):

    slug = 'spec-choice-topic'

    def get_list(self):
        if self.slug is None:
            return list()
        try:
            topic = Topic.objects.published().get(slug=self.slug)
            return topic.children.published()
        except Topic.DoesNotExist:
            return list()


class TopicsListWidget(base.BaseListWidget):

    slug = 'spec-choice-topic'

    def get_list(self):
        try:
            choice = Topic.objects.filter(slug=self.slug).published().get()
        except Topic.DoesNotExist:
            return list()

        topics = choice.children.all().published()
        return topics


class TopicsInformationWidget(Widget):

    slug = 'spec-choice-topic'

    def get_topic_informations(self):
        timenow = now()
        choice = Topic.objects.filter(slug=self.slug).published().get()
        qs = choice.children.all().published()
        total_items_count = qs.count()
        month_items_count = qs.filter(released_datetime__month=timenow.month,
                                      released_datetime__year=timenow.year).count()
        return dict(
            topic=choice,
            total_items_count=total_items_count,
            month_items_count=month_items_count
        )

    def get_context(self, value=None, options=dict(), context=dict()):
        options.update(self.get_topic_informations())
        return options


class TopicsTopicInformationWidget(Widget):

    slug = None

    def get_topic_informations(self):
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
        self.slug =  options.get('slug') if options.get('slug') else self.slug
        options.update(self.get_topic_informations())
        return options


class TopicsTopicPackageVersionListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            packages = TopicalItem.objects\
                .get_items_by_topic(topic=topic, item_model=Package)
            return packages
        except (Topic.DoesNotExist, Package.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        return super(TopicsTopicPackageVersionListWidget, self)\
            .get_context(value=value, options=options, context=context)
