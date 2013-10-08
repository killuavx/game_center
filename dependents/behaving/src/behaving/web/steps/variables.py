from splinter.exceptions import ElementDoesNotExist
from behave import step


@step('I set "{key}" to the text of "{name}"')
def set_key_to_el_text(context, key, name):
    assert context.persona is not None, 'no persona is setup'
    el = context.browser.find_by_id(name) or context.browser.find_by_name(name)
    assert el, 'Element not found'
    context.persona[key] = el.first.text


@step('I set "{key}" to the attribute "{attr}" of the element with xpath "{xpath}"')
def set_key_to_xpath_attr(context, key, attr, xpath):
    assert context.persona is not None, 'no persona is setup'
    try:
        el = context.browser.find_by_xpath(xpath)
    except ElementDoesNotExist:
        assert False, 'Element not found'

    context.persona[key] = el.first[attr] or ''
