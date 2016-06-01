# -*- coding: utf-8 -*-
from behave import *
from behaving.personas.steps import *
from warehouse.models import Package
from django.db.models.query import Q
from fts.features.app_dsls.account import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl


@when('I sign up with below information')
def signup_with_below_information(context):
    AccountDSL = factory_dsl(context)
    WebDSL = factory_web_dsl(context)
    for row in context.table:
        AccountDSL.signup(context, **row.as_dict())
        WebDSL.response_to_world(context)

@given('player "{username}" already exists')
def player_already_exists(context, username):
    AccountDSL = factory_dsl(context)
    AccountDSL.already_exists_player_create(context, username)

@when('I sign in as "{username}"')
def signin_as(context, username, password=False):
    WebDSL = factory_web_dsl(context)
    AccountDSL = factory_dsl(context)
    if password is False:
        password = AccountDSL._PASSWORD

    signin_data = dict(username=username, password=password)
    with AccountDSL.signin(context, **signin_data) as user_data:
        WebDSL.response_to_world(context)
        result = WebDSL.response_structure_content(context)
        user_data['token'] = result.get('token')

@given('I sign in as "{username}" already exists')
def player_already_exists_and_signin(context, username):
    player_already_exists(context, username)
    signin_as(context, username)

@when('I visit my profile')
def visit_myprofile(context):
    AccountDSL = factory_dsl(context)
    AccountDSL.visit_myprofile(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

@when('I sign out')
def signout(context):
    AccountDSL = factory_dsl(context)
    AccountDSL.signout(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)


# bookmark
@when('I mark package name "{pkg_title}"')
def mark_package(context, pkg_title):
    package = Package.objects\
        .get(Q(title=pkg_title) | Q(package_name=pkg_title))

    AccountDSL = factory_dsl(context)
    AccountDSL.add_bookmark(context, package)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)


@when('I unmark package name "{pkg_title}"')
def unmark_package(context, pkg_title):
    package = Package.objects \
        .get(Q(title=pkg_title) | Q(package_name=pkg_title))

    AccountDSL = factory_dsl(context)
    AccountDSL.remove_bookmark(context, package)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)


@when('I visit my bookmarks page')
def visit_bookmarks_page(context):
    AccountDSL = factory_dsl(context)
    AccountDSL.visit_bookmarks(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

@when('I check bookmark with package name "{pkg_title}"')
def check_bookmark(context, pkg_title):
    package = Package.objects.get(Q(title=pkg_title)|Q(package_name=pkg_title))
    AccountDSL = factory_dsl(context)
    AccountDSL.check_bookmark(context, package)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

# comment
@when('I visit my commented package page')
def visit_my_commented_packages(context):
    AccountDSL = factory_dsl(context)
    AccountDSL.visit_commented_packages(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

