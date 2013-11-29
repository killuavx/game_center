# -*- coding: utf-8 -*-
from django.core.management import call_command
from searcher.models import TipsWord
from fts.helpers import add_model_objects, clear_data
from django.utils.timezone import now
from datetime import timedelta
from django.core.urlresolvers import reverse
from urllib.parse import urlencode

import sh
from os.path import join, dirname, exists
from django.conf import settings
import time


class SearcherService(object):

    script_path = settings.SEARCHER_SCRIPT_DIR

    @classmethod
    def start(cls, wait=5):
        if not cls.is_runing():
            cls.set_script('start')
            cls.solr_start()
            time.sleep(wait)

    @classmethod
    def stop(cls):
        cls.set_script('stop')
        cls.solr_stop()

    @classmethod
    def is_runing(cls):
        return exists('/tmp/solr.pid')

    @classmethod
    def set_script(cls, name):
        name = 'solr_%s' % name
        if not hasattr(cls, name):
            setattr(cls,
                    name,
                    sh.Command("%s/%s.sh" % (cls.script_path, name))
            )


class SearcherBaseDSL(object):

    _tipwrolds_url = '/api/tipswords/'

    _search_url = '/api/search/'

    @classmethod
    def get_admin_tipsword_uri(cls, type):
        return reverse('admin:%s_%s_%s' % (
            TipsWord._meta.app_label,
            TipsWord._meta.module_name,
            type
        ))

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        clear_data()

    @classmethod
    def create_tipsword_already_exists(cls, context, **kwargs):
        yesterday = now() - timedelta(days=1)
        kwargs.setdefault('status', 'published')
        kwargs.setdefault('released_datetime', yesterday)
        world = TipsWord.objects.create(**kwargs)
        add_model_objects(world)

    @classmethod
    def visit_tipswords_page(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'visit_tipswords_page'))

    @classmethod
    def create_tipsword(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'create_tipsword'))

    @classmethod
    def goto_tipsword_create_page(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'goto_tipswords_create_page'))

    @classmethod
    def goto_tipsword_list_page(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'goto_tipswords_list_page'))

    @classmethod
    def search_package(cls, context, keyword):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'search_package'))

    @classmethod
    def rebuild_index(cls, context):
        call_command('rebuild_index', interactive=False)


class SearcherWithNoUIClient(SearcherBaseDSL):

    @classmethod
    def visit_tipswords_page(cls, context):
        api_url = "%s%s" %(context.base_url, cls._tipwrolds_url)
        context.client.get(api_url)

    @classmethod
    def goto_tipsword_create_page(cls, context):
        url = "%s%s" %(context.base_url, cls.get_admin_tipsword_uri(type='add'))
        context.client.get(url)

    @classmethod
    def goto_tipsword_list_page(cls, context):
        url = "%s%s" %(context.base_url, cls.get_admin_tipsword_uri(type='changelist'))
        context.client.get(url)

    @classmethod
    def create_tipsword(cls, context, **kwargs):
        return cls.create_tipsword_already_exists(context, **kwargs)

    @classmethod
    def search_package(cls, context, keyword):
        api_url = '%s%s?%s' %(context.base_url,
                              cls._search_url,
                              urlencode(dict(q=keyword)))
        context.client.get(api_url)


class SearcherUsingBrowserDSL(SearcherBaseDSL):

    @classmethod
    def visit_tipswords_page(cls, context):
        context.execute_steps('When I visit "%s"' % cls._tipwrolds_url)

    @classmethod
    def goto_tipsword_create_page(cls, context):
        create_uri = cls.get_admin_tipsword_uri(type='add')
        if create_uri in context.browser.url:
            return
        else:
            context.execute_steps("""
                When I click the link to a url that contains "%(create_uri)s"
            """ % dict(
                create_uri=create_uri,
                ))

    @classmethod
    def goto_tipsword_list_page(cls, context):
        context.execute_steps('When I visit "%s"' %\
                              cls.get_admin_tipsword_uri(type='changelist'))

    @classmethod
    def create_tipsword(cls, context, **kwargs):
        yesterday = now() - timedelta(days=1)
        relased_datetime = kwargs.get('released_datetime', yesterday)
        d, t = str(relased_datetime).split(' ')
        t = t.split('.')[0]

        context.execute_steps("""
            When I fill in "keyword" with "%(keyword)s"
             And I select "%(status)s" from "status"
             And I fill in "released_datetime_0" with "%(date)s"
             And I fill in "released_datetime_1" with "%(time)s"
             And I press "%(btn)s"
        """ % dict(
            keyword=kwargs.get('keyword'),
            status=kwargs.get('status', 'published'),
            date=d,
            time=t,
            btn="保存并增加另一个",
        ))

    @classmethod
    def search_package(cls, context, keyword):
        api_url = '%s?%s' %(cls._search_url, urlencode(dict(q=keyword)))
        context.execute_steps('When I visit "%s"' % api_url)


def factory_dsl(context):
    if 'browser' in context.tags:
        return SearcherUsingBrowserDSL

    return SearcherWithNoUIClient


def setup(context):
    return factory_dsl(context).setup(context)


def teardown(context):
    return factory_dsl(context).teardown(context)
