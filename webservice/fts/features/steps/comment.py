# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.helpers import ApiDSL
from should_dsl import should

from django.test.testcases import override_settings
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl
from fts.features.app_dsls.warehouse import factory_dsl as factory_warehouse_dsl
from fts.features.app_dsls.comment import factory_dsl

@given('post comment status of platform default is {is_public:pub?}')
def settings_change(context, is_public):
    context.world.update(dict(settings_comment_is_public=is_public))


def _get_comment_settings_decorator(context):
    is_public = context.world.get('settings_comment_is_public', None)
    if is_public is not None:
        _decorator = override_settings(COMMENTS_POST_PUBLISHED=is_public)
    else:
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return _wrapper

    return _decorator

@when('I post comment "{comment_content:n?s}" '
      'to the package version')
@when('I post comment "{comment_content:n?s}" '
      'to the package title "{title}" version_code "{version_code:d}"')
def post_comment_to_package_version(context, comment_content,
                                    title=None, version_code=None):

    if title is not None and version_code is not None:
        WarehouseDSL = factory_warehouse_dsl(context)
        packageversion = WarehouseDSL.get_packageversion_by(
            title=title,
            version_code=version_code)
    else:
        packageversion = context.world.get('the_package_version')


    CommentDSL = factory_dsl(context)
    _decorator = _get_comment_settings_decorator(context)
    _decorator(CommentDSL.post)(context, packageversion, comment_content)

    factory_web_dsl(context).response_to_world(context)

@when('I visit comment list of the package version')
def visit_comment_list(context):
    version = context.world.get('the_package_version')
    CommentDSL = factory_dsl(context)
    CommentDSL.visit_comment_list(context, version)

    factory_web_dsl(context).response_to_world(context)

@given('the comment of the package version change to {is_public:pub?}')
@given('the comment of package name "{title}" '
       'version_code "{version_code:d}" change to {is_public:pub?}')
def change_comment_of_the_packageversion_to_published(context,
                                                      is_public,
                                                      title=None,
                                                      package_name=None,
                                                      version_code=None):
    WarehouseDSL = factory_warehouse_dsl(context)
    if package_name:
        context.execute_steps(
            'Given I focus on package name "%s" version code "%s"' % (
                package_name, version_code))
    elif title:
        context.execute_steps(
            'Given I focus on package title "%s" version code "%s"' % (
                title, version_code))

    packageversion = context.world.get('the_package_version')

    CommentDSL = factory_dsl(context)
    the_comment = CommentDSL.get_comment_by(packageversion)
    CommentDSL.change_comment_publish_status(context, the_comment, is_public)
    context.world.update(dict(the_comment=the_comment))



