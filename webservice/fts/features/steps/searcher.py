# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.features.app_dsls.searcher import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl


@given('tipswords exists such below')
def create_tipswords_already_exists(context):
    SearcherDSL = factory_dsl(context)
    for row in context.table:
        SearcherDSL.create_tipsword_already_exists(context, **row.as_dict())

@when('I visit tipswords page')
def visit_tipswords_page(context):
    SearcherDSL = factory_dsl(context)
    SearcherDSL.visit_tipswords_page(context)

    factory_web_dsl(context).response_to_world(context)

@when('I create tipswords below')
def create_tipsword_in_admin(context):
    SearcherDSL = factory_dsl(context)
    for row in context.table:
        SearcherDSL.create_tipsword(context, **row.as_dict())

@when('I visit tipsword create page')
def visit_tipsword_admin_create_page(context):
    SearcherDSL = factory_dsl(context)
    SearcherDSL.goto_tipsword_create_page(context)

    factory_web_dsl(context).response_to_world(context)

@when('I visit tipsword list page')
def visit_tipsword_admin_list_page(context):
    SearcherDSL = factory_dsl(context)
    SearcherDSL.goto_tipsword_list_page(context)

    factory_web_dsl(context).response_to_world(context)


