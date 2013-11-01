# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from should_dsl import should
from django.utils.timezone import now, timedelta
from fts.helpers import ApiDSL, convert_content
from splinter.exceptions import ElementDoesNotExist
from clientapp.models import ClientPackageVersion
from fts.features.support import StatusCode

class SelfUpdateBaseDSL(object):

    api_uri = '/api/selfupdate'

    client_versions_key = 'platform_clientversions'

    @classmethod
    def clientversion_already_exists(cls, context, **kwargs):
        released_datetime = None
        if kwargs.get('status') == ClientPackageVersion.STATUS.published:
            released_datetime = now()-timedelta(days=1)
        version = ClientPackageVersion.objects.create(
            version_code=kwargs['version_code'],
            version_name=kwargs['version_name'],
            status=kwargs['status'],
            released_datetime=released_datetime,
        )
        key = cls.client_versions_key
        if not context.world.get(key):
            context.world.setdefault(key, dict())

        context.world.get(key).update({
            version.version_code: version
        })
        return version

    @classmethod
    def clientversion_count(self, context, **kwlookups):
        qs = ClientPackageVersion.objects.all()
        if len(kwlookups):
            return qs.filter(**kwlookups).count()
        return qs.count()

    @classmethod
    def visit_selfupdate(cls, context):
        pass

    @classmethod
    def receive_latest_client_version(cls, context):
        return context.world.get('content')

class SelfUpdateDSLWithNoUIClient(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        res = context.client.get(SelfUpdateBaseDSL.api_uri)
        context.world.update(dict(
            content=convert_content(res.content),
            status=StatusCode(
                code=res.status_code,
                reason=res.status_text,
                )
        ))

class SelfUpdateUsingWebBrowserDSL(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        context.execute_steps("""
            When I visit "%s"
        """ % cls.api_uri)

        try:
            content = context.browser.find_by_tag('body').text
        except ElementDoesNotExist:
            content = context.browser.html
        context.world.update(dict(
            content=convert_content(content),
            status=StatusCode(
                code=context.browser.status_code.code,
                reason=context.browser.status_code.reason
            )
        ))

def factory_selfupdate_dsl(context):
    if 'browser' in context.tags:
        SelfUpdateDSL = SelfUpdateUsingWebBrowserDSL
    else:
        SelfUpdateDSL = SelfUpdateDSLWithNoUIClient

    return SelfUpdateDSL

@given('clientapp has version below')
def step_create_client_versions(context):
    SelfUpdateDSL = factory_selfupdate_dsl(context)
    for row in context.table:
        SelfUpdateDSL.clientversion_already_exists(
            context,
            version_code=row['version_code'],
            version_name=row['version_name'],
            status=row['status']
        )

@given('nothing can selfupdate')
def step_nothing_can_update(context):
    SelfUpdateDSL = factory_selfupdate_dsl(context)
    SelfUpdateDSL.clientversion_count(context) |should| equal_to(0)

@when('I visit selfupdate')
def step_visit_selfupdate(context):
    SelfUpdateDSL = factory_selfupdate_dsl(context)
    SelfUpdateDSL.visit_selfupdate(context)

@then('I should receive client version code "{version_code:d}"')
def step_client_version_code(context, version_code):
    SelfUpdateDSL = factory_selfupdate_dsl(context)
    version = SelfUpdateDSL.receive_latest_client_version(context)
    version.get('version_code') |should| equal_to(version_code)
