# -*- coding: utf-8 -*-
from behave import *
from fts.features import support
from fts.features.app_dsls.web import factory_dsl
from should_dsl import should, should_not
from collections.abc import Iterable


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
      '{be_contains:contains?} the {field} of element is "{value}"')
def result_list_should_contains_package(context,
                                        is_within,
                                        field,
                                        value,
                                        be_contains=True):
    WebDSL = factory_dsl(context)
    WebDSL.should_result_contains(
        context=context,
        be_or_not=be_contains,
        within_pagination=is_within,
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
      'have {count:d} elements')
def result_list_should_have_elements(context, is_within, count):
    WebDSL = factory_dsl(context)
    results = WebDSL.response_structure_content(context)
    if is_within:
        results = results.get('results')

    results |should| have(count).elements


@then('I should see response contains field "{name}"')
def should_contains_field(context, name):
    WebDSL = factory_dsl(context)
    result = WebDSL.response_structure_content(context)
    result.get(name) |should_not| be(None)

@then('I should see response with {field} "{value}"')
def should_see_field(context, field, value):
    WebDSL = factory_dsl(context)
    content = WebDSL.response_structure_content(context)
    content.get(field) |should_not| be(None)
    str(content.get(field)) |should| equal_to(value)

@then('I should see response field {field} endswith "{endstr}"')
def should_see_field_endswith(context, field, endstr):
    WebDSL = factory_dsl(context)
    content = WebDSL.response_structure_content(context)
    content.get(field) |should_not| be(None)
    content.get(field) |should| end_with(endstr)


@then('I should see response contains with {field} on below')
def should_see_field_contains_below_value(context, field):
    WebDSL = factory_dsl(context)
    content = WebDSL.response_structure_content(context)

    data_sequeue = content.get(field)
    data_sequeue |should_not| be(None)
    data_sequeue |should| be_kind_of(Iterable)
    data_sequeue = list(map(lambda e: str(e), data_sequeue))

    expect_sequeue = list(map(lambda row: str(row['value']), context.table))
    data_sequeue |should| have_at_least(len(expect_sequeue)).items
    data_sequeue |should| include_all_of(expect_sequeue)

@then('I should see list result with{is_within:in?out} pagination '
      'paginate by "{page_size:d}" items')
def result_list_should_paginate_by(context, is_within, page_size):
    WebDSL = factory_dsl(context)
    WebDSL.should_result_paginate_by(context, is_within, page_size)

@then('I should see list result with{is_within:in?out} pagination '
      'sequence like below')
def reuslt_list_should_sequence_like(context, is_within):
    WebDSL = factory_dsl(context)
    WebDSL.should_result_list_sequence_like(context, is_within)

@when('I follow {url_field} of the element {find_field} "{find_value}" '
      'in list result of the response with{is_within:in?out} pagination')
def follow_url_in_response_list_result(context,
                                       url_field,
                                       find_field,
                                       find_value,
                                       is_within=True):
    WebDSL = factory_dsl(context)
    WebDSL.follow_url_in_response_list_result(context=context,
                                              url_field=url_field,
                                              find_field=find_field,
                                              find_value=find_value,
                                              within_pagination=is_within)
    WebDSL.response_to_world(context)

@when('I follow {url_field} on response')
def follow_url_on_response(context, url_field):
    WebDSL = factory_dsl(context)
    WebDSL.follow_url_on_response(context=context, url_field=url_field)
    WebDSL.response_to_world(context)


@when('I move row contains "{text}" {updown:up?down} {times:d} times')
def move_row_contains(context, text, updown, times):
    updown = 'up' if updown else 'down'
    xpath = '//tr//*[contains(text(),"%s")]//ancestor-or-self::tr' \
            '//a[contains(@class, "sortable-%s")]' %(text, updown)
    btn = context.browser.find_by_xpath(xpath)
    for i in range(times):
        btn.click()

@when('I fill row contains "{text}" in name "{pattern}" with "{value}"')
def fill_row(context, text, pattern, value):
    xpath = '//tr//*[contains(text(),"%(text)s")]//ancestor-or-self::tr' \
            '//*[contains(@name, "%(pattern)s")]' % dict(text=text,
                                                         pattern=pattern)
    input = context.browser.find_by_xpath(xpath).first
    input.fill(value)
