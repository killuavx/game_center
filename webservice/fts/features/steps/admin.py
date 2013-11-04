# -*- coding: utf-8 -*-
from behave import *
from fts.features.app_dsls.admin import factory_dsl
from should_dsl import should


@when('I login admin panel with username "{login_name}" password "{login_pass}"')
def login_on_admin(context, login_name, login_pass):
    AdminDSL = factory_dsl(context)
    AdminDSL.login(context, login_name, login_pass)

@given('staff user exists below')
def create_staff_user(context):
    AdminDSL = factory_dsl(context)
    for row in context.table:
        AdminDSL.create_staff_user(context, row['username'], row['password'])

@then('I should {is_logined:be?} logined to admin')
def should_logined_to_admin(context, is_logined):
    AdminDSL = factory_dsl(context)
    AdminDSL.login_successful_above(context) |should| be(is_logined)


@given('login admin as supperuser "{username}" already exists')
def login_as_supperuser_already_exists(context, username):
    AdminDSL = factory_dsl(context)
    AdminDSL.login_as_supperuser_already_exists(context, username)
