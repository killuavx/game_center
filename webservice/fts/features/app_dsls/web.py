# -*- coding: utf-8 -*-
import json
from collections import namedtuple
from behaving.web.steps import basic
from should_dsl import should
from fts.features.support import HackBrowserFromClient


def text_to_json_data(text):
    try:
        data = json.loads(text)
    except:
        data = None
    return data

class WebBaseDSL(object):

    StatusCode = namedtuple('StatusCode', ['code', 'reason'])

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


class WebUsingNoUIClientDSL(WebBaseDSL):

    @classmethod
    def browser_or_client(cls, context):
        context.client_initial_params = cls.client_initial_params
        #context.client = Client(cls.client_initial_params)
        context.client = HackBrowserFromClient(cls.client_initial_params)
        context.browser = context.client

    @classmethod
    def should_see(cls, context, text):
        context.client.is_text_present =\
            lambda text: context.world.get('content')
        basic.should_see(context, text)


    @classmethod
    def response_to_world(cls, context):
        response = context.client.response
        content = context.client.response_content
        context.world.update(dict(
            content=content,
            content_json=text_to_json_data(content),
            status=cls.StatusCode(
                code=response.status_code,
                reason=response.status_text
            )
        ))


class WebUsingBrowserDSL(WebBaseDSL):

    driver_name = ''
    #driver_name = 'phantomjs'

    #default_browser = 'phantomjs'
    default_browser = ''

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
        status = browser.status_code
        data = None
        body = browser.find_by_tag('body')
        if body:
            content = body.text
            data = text_to_json_data(content)
        context.world.update(dict(
            content=content,
            content_json=data,
            status=cls.StatusCode(
                code=status.code,
                reason=status.reason
            )
        ))


def factory_dsl(context):
    if 'browser' in context.tags:
        return WebUsingBrowserDSL
    else:
        return WebUsingNoUIClientDSL