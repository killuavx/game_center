# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import *
from behaving.web.steps import *
from django.test.client import Client
from should_dsl import should

class WebDSL(object):

    client_initial_params = dict(HTTP_ACCEPT='application/json',
                                 HTTP_CACHE_CONTROL='no-cache')

    @classmethod
    def should_receive_status(cls, context, code, reason):
        status = context.world.get('status')
        (status.code, status.reason) |should| equal_to((code, reason))

    @classmethod
    def should_see_message(cls, context, message):
        message |should| equal_to(context.world.get('content').get('detail'))

    @classmethod
    def should_see_nothing(cls, context):
        context.world.get('content') |should| be('')

    @classmethod
    def browser_or_client(cls, context):
        if 'browser' in context.tags:
            context.execute_steps("""
            Given a browser
            """)
        else:
            context.client_initial_params = cls.client_initial_params
            context.client = Client(cls.client_initial_params)


@given('a browser or client')
def step_browser_or_client(context):
    WebDSL.browser_or_client(context)

@then('I should see "{message}"')
def step_should_see_message(context, message):
    WebDSL.should_see_message(context, message)

@then('I should receive {status_code:d} {reason:upper}')
def step_should_receive_status(context, status_code, reason):
    WebDSL.should_receive_status(context, status_code, reason)

@then('I should see nothing')
def step_should_see_nothing(context):
    WebDSL.should_see_nothing(context)
