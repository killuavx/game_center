# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.helpers import ApiDSL
from should_dsl import should
from comment.models import Comment
from warehouse.models import Package, PackageVersion


from django.test.testcases import override_settings

@when('I post comment "{comment:n?s}" to the package')
def step_post_comment_to_the_package(context, comment):
    is_public = context.world.get('settings_comment_is_public', None)
    if is_public is not None:
        _decorator = override_settings(COMMENTS_POST_PUBLISHED=is_public)
    else:
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return _wrapper
    _decorator(ApiDSL.When_i_post_comment_to)(context,
                                            content=comment,
                                            obj=context.world.get("the_package"))

@then('I should receive comment "{content:n?s}" from response')
def step_should_receive_comment_from_response(context, content):
    context.world.get('content').get('comment') |should| equal_to(content)


from fts.features.app_dsls.web import factory_dsl as factory_web_dsl
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


def get_packageversion(title, version_code):
    package = Package.objects.get(title=title)
    package.status |should| equal_to(Package.STATUS.published)
    packageversion = package.versions.get(version_code=version_code)
    packageversion.status |should| equal_to(PackageVersion.STATUS.published)
    return packageversion


@when('I post comment "{comment_content:n?s}" '
      'to the package title "{title}" version_code "{version_code:d}"')
def post_comment_to_package_version(context, comment_content,
                                    title, version_code):

    CommentDSL = factory_dsl(context)
    packageversion = get_packageversion(title, version_code)

    _decorator = _get_comment_settings_decorator(context)
    _decorator(CommentDSL.post)(context, packageversion, comment_content)

    factory_web_dsl(context).response_to_world(context)

@when('I visit comment list of the package version')
def visit_comment_list(context):
    package = context.world.get('the_package')
    version = package.versions.get()
    CommentDSL = factory_dsl(context)
    CommentDSL.visit_comment_list(context, version)

    factory_web_dsl(context).response_to_world(context)


def step_should_see_comment_list_in_comment_page(context):
    results = factory_web_dsl(context).response_structure_content(context)
    comment = results.get('results')[0]

    comment |should| include_keys('user_icon',
                                  'user_name',
                                  'submit_date',
                                  'comment')
    context.world.update(dict(comment=comment))

@given('the comment of package name "{pkg_title}" '
       'version_code "{version_code:d}" change to {is_public:pub?}')
def change_comment_of_the_packageversion_to_published(context,
                                                      pkg_title,
                                                      version_code,
                                                      is_public):
    version = get_packageversion(pkg_title, version_code)
    the_comment = Comment.objects.for_model(version).get()
    CommentDSL = factory_dsl(context)
    CommentDSL.change_comment_publish_status(context, the_comment, is_public)
    context.world.update(dict(the_comment=the_comment))



