# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils.timezone import now
from clientapp.models import ClientPackageVersion


class SelfUpdateBaseDSL(object):

    api_uri = '/api/selfupdate'

    client_versions_key = 'platform_clientversions'

    package_name = 'com.ccplay.gc.app'

    @classmethod
    def clientversion_already_exists(cls, context, **kwargs):
        released_datetime = None
        if kwargs.get('status') == ClientPackageVersion.STATUS.published:
            released_datetime = now()-timedelta(days=1)
        version = ClientPackageVersion.objects.create(
            package_name=cls.package_name,
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
        raise NotImplementedError('you must implement %s.%s' %(
            cls,
            'visit_selfupdate'
        ))

    @classmethod
    def receive_latest_client_version(cls, context):
        return context.world.get('content_json')


class SelfUpdateUsingWebBrowserDSL(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        context.execute_steps("""
            When I visit "%s"
        """ % cls.api_uri)


class SelfUpdateDSLWithNoUIClient(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        context.client.get(cls.api_uri)


def factory_dsl(context):
    if 'browser' in context.tags:
        SelfUpdateDSL = SelfUpdateUsingWebBrowserDSL
    else:
        SelfUpdateDSL = SelfUpdateDSLWithNoUIClient

    return SelfUpdateDSL


