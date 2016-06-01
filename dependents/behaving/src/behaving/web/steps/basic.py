import time
from behave import step

from behaving.personas.persona import persona_vars


@step('I wait for {timeout:d} seconds')
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step('I show the element with id "{id}"')
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="inline";' % id)


@step('I hide the element with id "{id}"')
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="none";' % id)


@step('I should see "{text}"')
def should_see(context, text):
    assert context.browser.is_text_present(text), 'Text not found'


@step('I should not see "{text}"')
def should_not_see(context, text):
    assert context.browser.is_text_not_present(text), 'Text was found'


@step('I should see "{text}" within {timeout:d} seconds')
def should_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_present(text, wait_time=timeout), 'Text not found'


@step('I should not see "{text}" within {timeout:d} seconds')
def should_not_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_not_present(text, wait_time=timeout), 'Text was found'


@step('I should see an element with id "{id}"')
def should_see_element_with_id(context, id):
    assert context.browser.is_element_present_by_id(id), 'Element not present'


@step('I should not see an element with id "{id}"')
def should_not_see_element_with_id(context, id):
    assert context.browser.is_element_not_present_by_id(id), 'Element is present'


@step('I should see an element with id "{id}" within {timeout:d} seconds')
def should_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_present_by_id(id, wait_time=timeout), 'Element not present'


@step('I should not see an element with id "{id}" within {timeout:d} seconds')
def should_not_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_not_present_by_id(id, wait_time=timeout), 'Element is present'


@step('I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), 'Element not present'


@step('I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert not context.browser.is_element_present_by_css(css), 'Element is present'


@step('I should see an element with the css selector "{css}" within {timeout:d} seconds')
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), 'Element not present'


@step('I should not see an element with the css selector "{css}" within {timeout:d} seconds')
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert not context.browser.is_element_present_by_css(css, wait_time=timeout), 'Element is present'


@step('I should see an element with xpath "{xpath}"')
@persona_vars
def should_see_element_with_xpath(context, xpath):
    print(xpath)
    assert context.browser.is_element_present_by_xpath(xpath), 'Element not present'


@step('I should not see an element with xpath "{xpath}"')
@persona_vars
def should_not_see_element_with_xpath(context, xpath):
    assert not context.browser.is_element_present_by_xpath(xpath), 'Element is present'


@step('I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), 'Element not present'


@step('I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert not context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), 'Element is present'
