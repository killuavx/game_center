# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django_widgets import Widget
from . import base


class BaseTopicListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        from taxonomy.models import Topic, TopicalItem
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            return topic.children.published()
        except Topic.DoesNotExist:
            return list()


class BaseTopicInformationWidget(Widget):

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


class BaseTopicPackageListWidget(base.BaseListWidget):

    slug = None

    def get_list(self):
        from taxonomy.models import Topic, TopicalItem
        from warehouse.models import Package
        try:
            topic = Topic.objects.filter(slug=self.slug).published().get()
            packages = TopicalItem.objects\
                .get_items_by_topic(topic=topic, item_model=Package)
            return packages
        except (Topic.DoesNotExist, Package.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug') if options.get('slug') else self.slug
        return super(BaseTopicPackageListWidget, self)\
            .get_context(value=value, options=options, context=context)
