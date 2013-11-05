# -*- coding: utf-8 -*-
from fts.helpers import add_model_objects, SubFile
from warehouse.models import Package, PackageVersion
from taxonomy.models import *
from should_dsl import should, should_not
from django.core.management import call_command


class TaxonomyBaseDSL(object):

    @classmethod
    def category_tree_already_exists(self, context):
        call_command('loaddata', SubFile.fixture_filename('categories'))


class TaxonomyUsingBrowserDSL(TaxonomyBaseDSL):
    pass


class TaxonomyUsingNoUIClientDSL(TaxonomyBaseDSL):
    pass


def factory_dsl(context):
    if 'browser' in context.tags:
        return TaxonomyUsingBrowserDSL

    return TaxonomyUsingNoUIClientDSL
