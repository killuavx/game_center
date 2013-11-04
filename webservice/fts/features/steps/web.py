# -*- coding: utf-8 -*-
from behave import *
from fts.features.app_dsls.web import factory_dsl

@given('a browser or client')
def step_browser_or_client(context):
    WebDSL = factory_dsl(context)
    WebDSL.browser_or_client(context)

@then('I should see "{message} in json response detail"')
def step_should_see_message(context, message):
    WebDSL = factory_dsl(context)
    WebDSL.should_see(context, message)

@then('I should receive {status_code:d} {reason:upper}')
def step_should_receive_status(context, status_code, reason):
    WebDSL = factory_dsl(context)
    WebDSL.should_receive_status(context, status_code, reason)

@then('I should see nothing')
def step_should_see_nothing(context):
    WebDSL = factory_dsl(context)
    WebDSL.should_see_nothing(context)

@then('I should see message below')
def step_see_message_below(context):
    WebDSL = factory_dsl(context)
    WebDSL.should_see(context, context.text)
