# -*- coding: utf-8 -*-
from fts.helpers import (add_model_objects,
                         clear_data,
                         SubFile,
                         create_category,
                         create_topic)
from taxonomy.models import *
from should_dsl import should
from django.utils.timezone import now, timedelta
from django.core.management import call_command


class TaxonomyBaseDSL(object):

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        clear_data()

    @classmethod
    def create_topic(cls, context, name, **kwargs):
        yesterday = now() - timedelta(days=1)
        kwargs.setdefault('status', 'published')
        kwargs.setdefault('released_datetime', yesterday)
        return create_topic(name=name, **kwargs)

    @classmethod
    def add_to_topic(cls, context, topic, content, ordering=None):
        if ordering is not None:
            topicItem = TopicalItem.objects.create(topic=topic,
                                                   content_object=content,
                                                   ordering=ordering)
        else:
            topicItem = TopicalItem.objects.create(topic=topic,
                                                   content_object=content)
        add_model_objects(topicItem)
        return topicItem

    @classmethod
    def get_taxonomy_by(cls, slug):
        return Topic.objects.get(slug=slug)

    @classmethod
    def create_category(cls, context, name, **kwargs):
        return create_category(name=name, **kwargs)

    @classmethod
    def category_tree_already_exists(self, context):
        call_command('loaddata', SubFile.fixture_filename('categories2'))

    @classmethod
    def get_category_by(cls, name):
        return Category.objects.get(name=name)

    @classmethod
    def visit_the_package_list_of_category(cls, context, page_size=None, **kwargs):
        category = Category.objects.get(**kwargs)
        api_url = '/api/categories/%s/packages/' % category.slug
        full_url = "%s%s"% (context.base_url, api_url)
        if page_size and page_size > 0:
            full_url = "%s?page_size=%d" %(full_url, page_size)
        context.browser.visit(full_url)

    @classmethod
    def hide_the_category(cls, context, category, hide=True):
        category.is_hidden = hide
        category.save()

    _api_category_url = '/api/categories/'

    @classmethod
    def visit_category_page(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'visit_category_page'
        ))

    _api_topic_url = '/api/topics/'

    @classmethod
    def visit_category_detail_page(cls, context, category):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'visit_category_detail_page'
        ))

    @classmethod
    def visit_topic_detail_page(cls, context, topic):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'visit_category_detail_page'
        ))


class TaxonomyUsingBrowserDSL(TaxonomyBaseDSL):

    @classmethod
    def visit_category_page(cls, context):
        context.execute_steps('When I visit "%s"' % cls._api_category_url)

    @classmethod
    def visit_category_detail_page(cls, context, category):
        api_url = "%s%s/" % (cls._api_category_url, category.slug)
        context.execute_steps('When I visit "%s"' % api_url)

    @classmethod
    def visit_topic_detail_page(cls, context, topic):
        api_url = "%s%s/" % (cls._api_topic_url, topic.slug)
        context.execute_steps('When I visit "%s"' % api_url)


class TaxonomyUsingNoUIClientDSL(TaxonomyBaseDSL):

    @classmethod
    def visit_category_page(cls, context):
        api_url = "%s%s" % (context.base_url, cls._api_category_url)
        context.client.get(api_url)

    @classmethod
    def visit_category_detail_page(cls, context, category):
        api_url = "%s%s%s/" % (context.base_url,
                              cls._api_category_url,
                              category.slug)
        context.client.get(api_url)

    @classmethod
    def visit_topic_detail_page(cls, context, topic):
        api_url = "%s%s%s/" % (context.base_url,
                               cls._api_topic_url,
                               topic.slug)
        context.client.get(api_url)


def factory_dsl(context):
    if 'browser' in context.tags:
        return TaxonomyUsingBrowserDSL

    return TaxonomyUsingNoUIClientDSL


def setup(context):
    factory_dsl(context).setup(context)


def teardown(context):
    factory_dsl(context).setup(context)
