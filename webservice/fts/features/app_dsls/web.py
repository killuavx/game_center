# -*- coding: utf-8 -*-
import json
from collections import namedtuple
from behaving.web.steps import basic
from should_dsl import should, should_not
from fts.features.support import HackBrowserFromClient, StatusCode


def text_to_json_data(text):
    try:
        data = json.loads(text)
    except:
        data = None
    return data

class WebBaseDSL(object):

    client_initial_params = dict(HTTP_ACCEPT='application/json',
                                 HTTP_CACHE_CONTROL='no-cache')

    @classmethod
    def response_to_world(cls, context):
        raise NotImplementedError("you must implement %s.%s" %(cls,
                                                               'response_to_world'))

    @classmethod
    def should_receive_status(cls, context, code, reason):
        status = context.world.get('status')
        (status.code, status.reason) |should| equal_to((code, reason))

    @classmethod
    def should_see_in_json_response_detail(cls, context, message):
        message |should| equal_to(
            context.world.get('content_json').get('detail')
        )

    @classmethod
    def should_see(cls, context, text):
        text in context.world.get('content') |should| be(True)

    @classmethod
    def should_see_nothing(cls, context):
        context.world.get('content') |should| be('')

    @classmethod
    def browser_or_client(cls, context):
        raise NotImplementedError("you must implement %s.%s" %(cls,
                                               'browser_or_client'))

    @classmethod
    def response_structure_content(cls, context):
        return context.world.get('content_json')

    @classmethod
    def should_see_empty_result(cls, context, within_pagination):
        results = cls.response_structure_content(context)
        if within_pagination:
            results= results.get('results')

        results |should| be_empty

    @classmethod
    def should_see_field_in_result_within_pagination(cls, context, field, value):
        results = cls.response_structure_content(context)
        expect_val = results.get(field)
        expect_val |should_not| be(None)
        str(expect_val) |should| equal_to(value)

    @classmethod
    def should_result_contains(cls,
                               context,
                               within_pagination,
                               find_func=lambda obj: False):
        results = cls.response_structure_content(context)
        if within_pagination:
            results= results.get('results')
        any((find_func(row) for row in results)) |should| be(True)

    @classmethod
    def response_to_world(cls, context):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'response_to_world'))


class WebUsingNoUIClientDSL(WebBaseDSL):

    @classmethod
    def browser_or_client(cls, context):
        context.client_initial_params = cls.client_initial_params
        #context.client = Client(cls.client_initial_params)
        context.client = HackBrowserFromClient(cls.client_initial_params)
        context.browser = context.client

    @classmethod
    def should_see(cls, context, text):
        basic.should_see(context, text)

    @classmethod
    def response_to_world(cls, context):
        content = context.browser.html
        status = context.browser.status_code
        context.world.update(dict(
            content=content,
            content_json=text_to_json_data(content),
            status=StatusCode(
                code=status.code,
                reason=status.reason
            )
        ))


class WebUsingBrowserDSL(WebBaseDSL):

    driver_name = ''
    #driver_name = 'phantomjs'

    default_browser = ''
    #default_browser = 'phantomjs'

    @classmethod
    def browser_or_client(cls, context):
        context.driver_name = cls.driver_name
        context.default_browser = cls.default_browser
        context.execute_steps("Given a browser")

    @classmethod
    def should_see(cls, context, text):
        basic.should_see(context, text)

    @classmethod
    def response_to_world(cls, context):
        browser = context.browser
        data = None
        try:
            body = browser.find_by_tag('body')
            if body:
                content = body.text
                data = text_to_json_data(content)
        except:
            pass

        status = browser.status_code
        context.world.update(dict(
            content=content,
            content_json=data,
            status=StatusCode(
                code=status.code,
                reason=status.reason
            )
        ))


def factory_dsl(context):
    if 'browser' in context.tags:
        return WebUsingBrowserDSL
    else:
        return WebUsingNoUIClientDSL