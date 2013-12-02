# -*- coding: utf-8 -*-
from behave import *
from fts.features.app_dsls.promotion import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl


@given('place "{slug}" exists')
def exists_place(context, slug):
    PromotionDSL = factory_dsl(context)
    PromotionDSL.create_place(context, slug)

@given('advertisement exists on place "{slug}" with content on below')
def exists_advertisement(context, slug):
    PromotionDSL = factory_dsl(context)


    rows = list(map(lambda r: r.as_dict(), context.table))
    PromotionDSL.create_advertisements(context,
                                       content_rows=rows,
                                       place_slug=slug)

@when('I visit advertisements on place "{slug}"')
@when('I visit advertisements with no place')
def visit_on_place(context, slug=None):
    PromotionDSL = factory_dsl(context)
    PromotionDSL.visit_advertisements_page(context, place_slug=slug)

    factory_web_dsl(context).response_to_world(context)
