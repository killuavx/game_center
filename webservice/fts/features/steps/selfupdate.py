# -*- coding: utf-8 -*-
from behave import *
from should_dsl import should
from fts.helpers import ApiDSL
from clientapp.models import ClientPackageVersion

class SelfUpdateDSL(object):
    pass

@given('nothing can selfupdate')
def step_nothing_can_update(context):
    ClientPackageVersion.objects.count() |should| equal_to(0)


@when('I visit selfupdate')
def step_visit_selfupdate(context):
    ApiDSL.When_i_access_selfupdate(context)

