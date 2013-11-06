# -*- coding: utf-8 -*-
from fts.helpers import add_model_objects, SubFile
from warehouse.models import Package, PackageVersion
from taxonomy.models import *
from should_dsl import should, should_not
from django.core.management import call_command


class TaxonomyBaseDSL(object):

    @classmethod
    def category_tree_already_exists(self, context):
        call_command('loaddata', SubFile.fixture_filename('categories2'))

    @classmethod
    def visit_the_package_list_of_category(cls, context, page_size=None, **kwargs):
        category = Category.objects.get(**kwargs)
        api_url = '/api/categories/%s/packages/' % category.slug
        full_url = "%s%s"% (context.base_url, api_url)
        if page_size and page_size > 0:
            full_url = "%s?page_size=%d" %(full_url, page_size)
        context.browser.visit(full_url)


class TaxonomyUsingBrowserDSL(TaxonomyBaseDSL):
    pass


class TaxonomyUsingNoUIClientDSL(TaxonomyBaseDSL):
    pass


def factory_dsl(context):
    if 'browser' in context.tags:
        return TaxonomyUsingBrowserDSL

    return TaxonomyUsingNoUIClientDSL
