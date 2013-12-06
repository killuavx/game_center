# -*- coding: utf-8 -*-
from behave import *
from fts.features.app_dsls.analysis import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl

@when('I post event to analysis webservice on below')
def post_event(context):
    AnalysisDSL = factory_dsl(context)
    for row in context.table:
        AnalysisDSL.post_event(context, **row.as_dict())

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

