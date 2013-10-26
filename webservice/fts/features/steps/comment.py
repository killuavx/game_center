# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.tests.helpers import ApiDSL
from should_dsl import should
from comment.models import Comment
from warehouse.models import Package, PackageVersion

@given('the comment of package name "{pkg_title}" '
       'version_code "{version_code:d}" change to {is_public:pub?}')
def step_change_comment_of_the_packageversion_to_published(context,
                                                           pkg_title,
                                                           version_code,
                                                           is_public):
    version = PackageVersion.objects.get(package__title=pkg_title,
                                         version_code=version_code)
    the_comment = Comment.objects.for_model(version).get()
    the_comment.is_public = is_public
    the_comment.save()
    context.world.update(dict(the_comment=the_comment))

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


@when('I post comment "{comment:n?s}" to the package')
def step_post_comment_to_the_package(context, comment):
    ApiDSL.When_i_post_comment_to(context,
                                  comment,
                                  context.world.get("the_package"))

@then('I should receive comment "{content:n?s}" from response')
def step_should_receive_comment_from_response(context, content):
    context.world.get('content').get('comment') |should| equal_to(content)

@when('I visit my commented package page')
def step_visit_my_commented_packages(context):
    ApiDSL.When_i_access_my_commented_packages_page(context)

