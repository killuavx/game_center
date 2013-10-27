# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import *
from behaving.web.steps import *
from fts.helpers import ApiDSL
from should_dsl import should

@then('I should see "{message}"')
def step_should_see_message(context, message):
    message |should| equal_to(context.world.get('content').get('detail'))

@then('I should receive {status_code:d} {status_desc}')
def step_should_receive_status(context, status_code, status_desc):
    ApiDSL.Then_i_should_receive_response_with(context,
                                               status_code=status_code)

