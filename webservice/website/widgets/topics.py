# -*- coding: utf-8 -*-
from django.utils.timezone import datetime, now, timedelta
from django_widgets import Widget
from taxonomy.models import Topic

from .common.topic import BaseTopicPackageListWidget, BaseTopicListWidget


class TopicsInformationWidget(Widget):

    slug = 'spec-choice-topic'

    template = 'pages/widgets/topics/information.haml'

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


class TopicsDetailInformationWidget(Widget):

    slug = None

    template = 'pages/widgets/topics/detail-information.haml'

    def get_topic_informations(self):
        topic = Topic.objects.filter(slug=self.slug).published().get()
        return dict(
            topic=topic
        )

    def get_context(self, value=None, options=dict(), context=dict()):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        options.update(self.get_topic_informations())
        return options


class TopicsTopicListWidget(BaseTopicListWidget):

    slug = 'spec-choice-topic'

    per_page = 8

    template = 'pages/widgets/topics/topic-list.haml'


class TopicsPackageListWidget(BaseTopicPackageListWidget):

    per_page = 24

    template = 'pages/widgets/topics/package-list.haml'

