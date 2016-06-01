# -*- coding: utf-8 -*-
import json
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
                               be_or_not=True,
                               find_func=lambda obj: False):
        results = cls.response_structure_content(context)

        _should_or_not = should if be_or_not else should_not
        if within_pagination:
            results= results.get('results')
        any((find_func(row) for row in results)) |_should_or_not| be(True)

    @classmethod
    def should_result_paginate_by(cls, context, within_pagination, page_size):
        result = content = cls.response_structure_content(context)
        if within_pagination:
            result = content.get('results')

        result |should| have(page_size).elements

    @classmethod
    def response_to_world(cls, context):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'response_to_world'))

    @classmethod
    def should_result_list_sequence_like(cls, context, within_pagination):
        result = content = cls.response_structure_content(context)
        if within_pagination:
            result = content.get('results')

        headings = context.table.headings
        expect_sequence = []
        for row in context.table:
            _kws ={field: row.get(field) for field in headings}
            expect_sequence.append(_kws)

        result_sequence = []
        for row in result:
            _kws ={field: str(row.get(field)) for field in headings}
            result_sequence.append(_kws)

        result_sequence |should| equal_to(expect_sequence)

    @classmethod
    def follow_url_in_response_list_result(cls, context,
                                              url_field,
                                              find_field,
                                              find_value,
                                              within_pagination=True):
        results = cls.response_structure_content(context)

        if within_pagination:
            results= results.get('results')
        def find_row(row):
            if str(row.get(find_field)) == find_value:
                return row
            return False

        expect_row = None
        for row in results:
            row = find_row(row)
            if row:
                expect_row = row
                break

        expect_row |should_not| be(None)
        url_to_follow = expect_row.get(url_field)
        url_to_follow |should_not| be(None)

        context.browser.visit(url_to_follow)

    @classmethod
    def follow_url_on_response(cls, context, url_field):
        data = cls.response_structure_content(context)
        url = data.get(url_field)
        url |should_not| be(None)
        context.browser.visit(url)


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


class WebBrowserDSL(WebUsingBrowserDSL):
    pass


def factory_dsl(context):
    if 'browser' in context.tags:
        if 'web' in context.tags:
            return WebBrowserDSL
        return WebUsingBrowserDSL
    else:
        return WebUsingNoUIClientDSL