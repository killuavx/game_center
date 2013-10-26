# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import when, given, then
from fts.features import support
from behaving.personas.steps import *
from fts.tests.helpers import ApiDSL, RestApiTest
from should_dsl import should
from warehouse.models import Package

@given('I am player in game center, named "{name}", email "{email}", phone "{phone}", with password "{password}"')
def step_given_as_player(context, name, email, phone, password):
    context.execute_steps('''
    Given "{name}" as the persona
    '''.format(name=name))
    ApiDSL.Given_i_have_account(context, dict(
        username=name,
        email=email,
        phone=phone,
        password=password
    ))
    step_as_player(context, name=name, email=email, phone=phone, password=password)

@when('I am player, named "{name:emptys}", email "{email:emptys}", phone "{phone:emptys}", with password "{password:emptys}"')
def step_as_player(context, name=None, email=None, phone=None, password=None):
    data = { k:v for k,v in dict(username=name,
                           email=email,
                           phone=phone,
                           password=password).items() if v is not None }

    context.personas[name].update(data)
    context.persona = context.personas[name]

@when('I sign up with "{name}"')
def step_sign_up(context, name):
    ApiDSL.When_i_signup_with(context, context.personas[name])

@then('I should see player profile with named "{name}", email "{email}", phone "{phone}"')
def step_should_see_player_profile(context, name=None, email=None, phone=None):
    except_account = context.world.get('content')
    ApiDSL.Then_i_should_see_account_profile(context, except_account)
    name |should| equal_to(except_account.get('username'))
    email |should| equal_to(except_account.get('email'))
    phone |should| equal_to(except_account.get('phone'))

@when('I sign in as "{username}" with {sigin_type}')
def step_sign_in_as(context, username, sigin_type):
    user_data = context.personas[username]
    ApiDSL.When_i_signin_with(context, dict(
        username=user_data.get(sigin_type),
        password=user_data.get('password')
    ))
    ApiDSL.When_i_prepare_auth_token(context, context.persona.get('token_key'))

@when('I sign out as "{username}"')
def step_sign_out_as(context, username):
    user_data = context.personas[username]
    ApiDSL.When_i_prepare_auth_token(context, user_data.get('token_key'))
    ApiDSL.When_i_signout(context)

from rest_framework.authtoken.models import Token
@then('I should see my authorization token')
def step_should_see_authorization_token(context):
    user_data = context.persona
    token_key = context.world.get('content').get('token')
    token = Token.objects.get(user__username=user_data.get('username'))
    token_key |should| equal_to(token.key)
    context.persona['token_key'] = token_key
    context.personas[user_data.get('username')]['token_key'] = token_key

@when('I visit my profile using my authorization token')
def step_visit_account_profile(context):
    ApiDSL.When_i_prepare_auth_token(context, token=context.persona.get('token_key'))
    ApiDSL.When_i_access_myprofile(context)

@when('I visit my profile')
def step_visit_account_profile(context):
    ApiDSL.When_i_prepare_auth_token(context, token=context.persona.get('token_key'))
    ApiDSL.When_i_access_myprofile(context)

@given('I sign in as player name "{username}" exists in game center')
def step_signin_existing_player(context, username):
    user = ApiDSL.Given_i_have_account(context, dict(
        username=username
    ))
    if username not in context.personas:
        context.personas[username]=dict()

    token = Token.objects.create(user=user)
    context.personas[username].update(dict(
        username=username,
        email=user.profile.email,
        phone=user.profile.phone,
        token_key=token.key,
        password=None
    ))
    context.persona = context.personas[username]
    ApiDSL.When_i_prepare_auth_token(context, context.persona.get('token_key'))

@then('I should see the player profile with {field} value {value:d}')
def step_should_see_profile_field(context, field, value):
    profile = context.world.get("content")
    profile.get(field) |should| equal_to(value)
    context.persona.update(dict(profile=profile))
    context.personas[context.persona.get('username')] = profile

@when('I mark package name "{pkg_title}"')
def step_mark_package(context, pkg_title):
    package = Package.objects.get(title=pkg_title)
    ApiDSL.When_i_add_bookmark(context, package)

@when('I unmark package name "{pkg_title}"')
def step_unmark_package(context, pkg_title):
    package = Package.objects.get(title=pkg_title)
    ApiDSL.When_i_remove_bookmark(context, package)

@when('I visit my bookmarks page')
def step_visit_mybookmarks(context):
    ApiDSL.When_i_access_bookmarks_page(context)
