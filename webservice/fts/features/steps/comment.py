# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.features import support
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

