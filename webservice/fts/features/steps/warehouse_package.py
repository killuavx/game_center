# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import *
from behaving.web.steps import *
from fts.features import support
from fts.tests.helpers import ApiDSL
from warehouse.models import Package, PackageVersion

@given('a set of packages in warehouse')
def step_given_a_set_of_packages_in_warehouse(context):
    for row in context.table:
        pkg = ApiDSL.Given_i_have_published_package(context,
                                              title=row.get('title'),
                                              package_name=row.get('package_name'),
                                              version_code=int(row.get('version_code')),
                                              version_name=row.get('version_name'),
                                              all_datetime=row.get('released_datetime')
        )

@given('package "{package_name}" has a set of versions below')
def step_given_package_has_versions_below(context, package_name):
    context.package = Package.objects.get(package_name=package_name)
    for row in context.table:
        ApiDSL.Given_package_has_version_with(context,
                                              package=context.package,
                                              version_name=row.get('version_name'),
                                              version_code=row.get('version_code'),
                                              status=PackageVersion.STATUS.published,
                                              all_datetime=row.get('released_datetime')
        )

@when('I post package version to check update with package_name: "{package_name}", version_name: "{version_name}", version_code: "{version_code:d}"')
def step_when_post_package_update_version(context,
                                          package_name,
                                          version_name,
                                          version_code):
    ApiDSL.When_i_post_package_update_versions(context, [
        dict(
            package_name=package_name,
            version_code=version_code,
            version_name=version_name,
        )
    ])

@then('I should see package update list has the version package_name: "{package_name}", version_name: "{response_version_name}", version_code: "{response_version_code:d}", it can {can_be} update')
def  step_then_should_see_package_update_list_has_the_version(context,
                                                              package_name,
                                                              response_version_name,
                                                              response_version_code,
                                                              can_be):
    is_updatable = False if can_be == 'not be' else True
    ApiDSL.Then_i_should_see_package_update_list_has_the_version(context,
                                                                 package_name=package_name,
                                                                 version_name=response_version_name,
                                                                 version_code=response_version_code,
                                                                 is_updatable=is_updatable)
