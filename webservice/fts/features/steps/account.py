# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import when, given, then
from fts.features import support
from behaving.personas.steps import *
from fts.tests.helpers import ApiDSL, RestApiTest
from should_dsl import should

@when('I am player, named "{name:emptys}", email "{email:emptys}", phone "{phone:emptys}", with password "{password:emptys}"')
def step_as_player(context, name=None, email=None, phone=None, password=None):
    data = { k:v for k,v in dict(username=name,
                           email=email,
                           phone=phone,
                           password=password).items() if v is not None }

    context.personas[name].update(data)

@when('I sign up with "{name}"')
def step_sign_up(context, name):
    ApiDSL.When_i_signup_with(context, context.personas[name])

@then('I should receive {status_code:d} {status_desc}')
def step_should_receive_status(context, status_code, status_desc):
    ApiDSL.Then_i_should_receive_response_with(context,
                                               status_code=status_code)

@then('I should see player profile with named "{name}", email "{email}", phone "{phone}"')
def step_should_see_player_profile(context, name=None, email=None, phone=None):
    except_account = context.world.get('content')
    ApiDSL.Then_i_should_see_account_profile(context, except_account)
    name |should| equal_to(except_account.get('username'))
    email |should| equal_to(except_account.get('email'))
    phone |should| equal_to(except_account.get('phone'))


@then('I should see "{message}"')
def step_should_see_message(context, message):
    message |should| equal_to(context.world.get('content').get('detail'))

