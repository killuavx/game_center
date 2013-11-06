# -*- coding: utf-8 -*-
from behave import *
from fts.features.app_dsls.web import factory_dsl
from should_dsl import should


# override step 'I choose "{value}" form "{options}"'
@when('I select "{option_value}" from "{select_name}"')
def select_from(context, select_name, option_value):
    context.browser.find_by_name(select_name).first.select(option_value)


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

@then('I should see empty list result with{is_within:in?out} pagination')
def step_should_see_empty_reuslt_list(context, is_within):
    WebDSL = factory_dsl(context)
    WebDSL.should_see_empty_result(context, is_within)


@then('I should see list result with{is_within:in?out} pagination '
      'contains the {field} of element is "{value}"')
def result_list_should_contains_package(context, is_within, field, value):
    WebDSL = factory_dsl(context)
    WebDSL.should_result_contains(
        context, is_within,
        find_func=lambda obj: str(obj.get(field))==value)

@then('I should see list result with{is_within:in?out} pagination '
      '{field} equal "{value}"')
def result_list_field_should_equal(context, is_within, field, value):
    WebDSL = factory_dsl(context)
    results = WebDSL.response_structure_content(context)
    if is_within:
        WebDSL.should_see_field_in_result_within_pagination(
            context, field, value)
    elif field == 'count':
        len(results) |should| equal_to(int(value))
    else:
        assert False, "Matcher Error"



@then('I should see list result with{is_within:in?out} pagination '
      'paginate by "{page_size:d}" items')
def result_list_should_paginate_by(context, is_within, page_size):
    WebDSL = factory_dsl(context)
    WebDSL.should_result_paginate_by(context, is_within, page_size)
