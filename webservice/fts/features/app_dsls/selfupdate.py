# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils.timezone import now
from clientapp.models import ClientPackageVersion
from fts.helpers import fixtures_dir, add_model_objects
from os.path import join, isfile
import os
from should_dsl import should, should_not


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
        add_model_objects(version)
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
    def goto_create_page(cls, context):
        raise NotImplementedError('you must implement %s.%s' %(
            cls,
            'goto_create_page'
        ))

    @classmethod
    def receive_latest_client_version(cls, context):
        return context.world.get('content_json')

    @classmethod
    def create_clientversion(cls, context, **kwargs):
        raise NotImplementedError('you must implement %s.%s' %(
            cls,
            'visit_selfupdate'
        ))


class SelfUpdateUsingWebBrowserDSL(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        context.execute_steps('When I visit "%s"' % cls.api_uri)

    @classmethod
    def goto_create_page(cls, context):
        create_uri='clientapp/clientpackageversion/add'
        if create_uri in context.browser.url:
            return
        else:
            context.execute_steps("""
                When I click the link to a url that contains "%(create_uri)s"
            """ % dict(
                create_uri=create_uri,
            ))

    @classmethod
    def create_clientversion(cls, context, **kwargs):
        package_name='com.ccplay.gc.app'
        icon_path=join(fixtures_dir, kwargs.get('icon', 'icon.png'))
        cover_path=join(fixtures_dir, kwargs.get('cover', 'cover.jpg'))
        download_path=join(fixtures_dir, kwargs.get('download', 'appexample/application.apk'))

        isfile(download_path) |should| be(True)
        isfile(cover_path) |should| be(True)
        isfile(icon_path) |should| be(True)

        d, t = str(now() - timedelta(days=1)).split(' ')
        t = t.split('.')[0]
        datetime_steps = """
        And I fill in "released_datetime_0" with "%(date)s"
        And I fill in "released_datetime_1" with "%(time)s"
        """ % dict(date=d, time=t)

        other_steps = """
        When I fill in "whatsnew" with "%(whatsnew)s"
         And I fill in "summary" with "%(summary)s"
        """ %dict(whatsnew=kwargs.get('whatsnew', 'no content'),
                  summary=kwargs.get('summary', 'no content'))

        context.execute_steps("""
            When I fill in "package_name" with "%(package_name)s"
             And I fill in "version_code" with "%(version_code)s"
             And I fill in "version_name" with "%(version_name)s"
             And I select "%(status)s" from "status"
             And I attach the file "%(download)s" to "download"
             And I attach the file "%(icon)s" to "icon"
             And I attach the file "%(cover)s" to "cover"
             %(other_steps)s
             %(datetime_steps)s
             And I press "%(btn)s"
        """ % dict(
            package_name=package_name,
            version_code=kwargs.get('version_code'),
            version_name=kwargs.get('version_name'),
            status=kwargs.get('status'),
            icon=icon_path,
            cover=cover_path,
            download=download_path,
            datetime_steps=datetime_steps,
            other_steps=other_steps,
            btn='保存并增加另一个',
        ))

        message = 'Client Package Version "%s:%s" 已经成功添加' %\
                  (package_name, kwargs.get('version_code'))
        context.execute_steps('Then I should see "%s"' % message)
        add_model_objects(ClientPackageVersion.objects.get(
            package_name=package_name,
            version_code=kwargs.get('version_code')
        ))


class SelfUpdateDSLWithNoUIClient(SelfUpdateBaseDSL):

    @classmethod
    def visit_selfupdate(cls, context):
        context.client.get(cls.api_uri)

    @classmethod
    def create_clientversion(cls, context, **kwargs):
        package_name='com.ccplay.gc.app'

        icon_path=join(fixtures_dir, kwargs.get('icon', 'icon.png'))
        cover_path=join(fixtures_dir, kwargs.get('cover', 'cover.jpg'))
        download_path=join(fixtures_dir, kwargs.get('download', 'appexample/application.apk'))
        isfile(download_path) |should| be(True)
        isfile(cover_path) |should| be(True)
        isfile(icon_path) |should| be(True)

        yesterday=now() - timedelta(days=1)
        cpv = ClientPackageVersion.objects.create(
            package_name=package_name,
            icon=icon_path,
            cover=cover_path,
            whatsnew=kwargs.get('whatsnew', ''),
            summary=kwargs.get('summary', ''),
            version_code=kwargs.get('version_code'),
            version_name=kwargs.get('version_name'),
            status=kwargs.get('status'),
            released_datetime=yesterday
        )
        cpv.pk |should_not| be(None)
        cpv.download = download_path
        cpv.save()
        add_model_objects(cpv)

    @classmethod
    def goto_create_page(cls, context):
        pass


def factory_dsl(context):
    if 'browser' in context.tags:
        SelfUpdateDSL = SelfUpdateUsingWebBrowserDSL
    else:
        SelfUpdateDSL = SelfUpdateDSLWithNoUIClient

    return SelfUpdateDSL


