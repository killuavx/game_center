# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.features import support
from fts.tests.helpers import get_current_request
from fts.tests.helpers import ApiDSL
from should_dsl import should

@then('I should see comment list of the package version in comment page')
def step_should_see_comment_list_in_comment_page(context):
    content = context.world.get('content')
    results = content.get('results')
    comment = results[0]
    comment |should| include_keys('user_icon',
                                  'user_name',
                                  'submit_date',
                                  'comment')
    context.world.update(dict(comment=comment))


@when('I post comment "{comment:emptys}" to the package')
def step_post_comment_to_the_package(context, comment):
    ApiDSL.When_i_post_comment_to(context,
                                  comment,
                                  context.world.get("the_package"))

@then('I should receive comment "{content:emptys}" from response')
def step_should_receive_comment_from_response(context, content):
    context.world.get('content').get('comment') |should| equal_to(content)

@when('I visit my commented package page')
def step_visit_my_commented_packages(context):
    ApiDSL.When_i_access_my_commented_packages_page(context)

@then('I should see the package commented by me in result list')
def step_should_see_commented_package_in_result_list(context):
    from mobapi.serializers import get_packageversion_comments_url
    results = context.world.get('content').get('results')
    except_package = results[0]
    the_package_versions = context.world.get('the_package_versions')
    latest_version_code = context.world.get('the_latest_version_code')
    the_latest_version = the_package_versions[latest_version_code]

    # 评论列表里含有object_pk, content_type,
    # 通过获取评论地址, 能够确定某一个版本
    # FIXME 使用另外一种比对应用版本的方式
    comments_url = get_packageversion_comments_url(the_latest_version)
    absolute_comments_url = get_current_request()\
        .build_absolute_uri(comments_url)
    absolute_comments_url |should| equal_to(except_package.get('comments_url'))

