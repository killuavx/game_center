# -*- coding: utf-8 -*-
from behave import *
from should_dsl import should, should_not
from fts.features.app_dsls.selfupdate import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl


@given('clientapp has version below')
def step_create_client_versions(context):
    SelfUpdateDSL = factory_dsl(context)
    for row in context.table:
        SelfUpdateDSL.clientversion_already_exists(
            context,
            version_code=row['version_code'],
            version_name=row['version_name'],
            status=row['status']
        )

@given('nothing can selfupdate')
def step_nothing_can_update(context):
    SelfUpdateDSL = factory_dsl(context)
    SelfUpdateDSL.clientversion_count(context) |should| equal_to(0)

@when('I visit selfupdate')
def step_visit_selfupdate(context):
    SelfUpdateDSL = factory_dsl(context)
    SelfUpdateDSL.visit_selfupdate(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

@then('I should receive client version code "{version_code:d}"')
def step_client_version_code(context, version_code):
    SelfUpdateDSL = factory_dsl(context)
    version = SelfUpdateDSL.receive_latest_client_version(context)
    version |should_not| be(None)
    version.get('version_code') |should| equal_to(version_code)
