# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from should_dsl import should
from fts.features.app_dsls.warehouse import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl

@given('package title "{title}" has a set of versions below')
@given('package name "{package_name}" has a set of versions below')
def create_package_versions(context, title=None, package_name=None):
    WarehouseDSL = factory_dsl(context)

    package = WarehouseDSL.create_package_without_ui(context,
                                                     with_version=False,
                                                     title=title,
                                                     package_name=package_name)
    for row in context.table:
        WarehouseDSL.create_package_versions_without_ui(context,
                                                        package,
                                                        **row.as_dict())


# pkg_field in ('name' , 'title')
@given('I focus on package {pkg_field} "{pkg_value}"')
@given('I focus on package {pkg_field} "{pkg_value}" '
       'version code "{version_code}"')
def focus_on_package_or_version(context,
                                pkg_field,
                                pkg_value=None,
                                version_code=None):
    WarehouseDSL = factory_dsl(context)

    if pkg_field == 'name':
        pkg_field = 'package_name'

    if version_code is not None:
        packageversion = WarehouseDSL.get_packageversion_by(
            version_code=version_code, **{pkg_field: pkg_value})
        context.world.update(the_package_version=packageversion)
        context.world.update(the_package=packageversion.package)
    else:
        package = WarehouseDSL.get_package_by(**{pkg_field: pkg_value})
        context.world.update(the_package=package)
        context.world.update(the_package_version=package.versions\
            .latest_version())


@given('package exists such below')
def package_already_exists_below(context):
    WarehouseDSL = factory_dsl(context)
    for row in context.table:
        WarehouseDSL.create_package_without_ui(context, **row.as_dict())

@given('change {field} of the package version to {value}')
def change_package_version(context, field, value):
    version = context.world.get('the_package_version')
    WarehouseDSL = factory_dsl(context)
    WarehouseDSL.change_package_version(context,
                                        version=version,
                                        field=field,
                                        value=value)

@when('I visit the package detail')
@when('I visit the package detail {pkg_field} "{pkg_value}"')
def visit_the_package_detail(context, pkg_field=None, pkg_value=None):
    if pkg_field:
        focus_on_package_or_version(context, pkg_field, pkg_value)

    WarehouseDSL = factory_dsl(context)
    package = context.world.get('the_package')
    if package is None:
        package_version = context.world.get('the_package_version')
        package = package_version.package
    WarehouseDSL.visit_package_detail(context, package)
    factory_web_dsl(context).response_to_world(context)


@when('I follow the package {field}')
def follow_the_package(context, field):
    WarehouseDSL = factory_dsl(context)
    WarehouseDSL.follow_package_detail_above(context, field)

    factory_web_dsl(context).response_to_world(context)

@when('I visit ranking list page')
def visit_ranking_page(context):
    WarehouseDSL = factory_dsl(context)
    WarehouseDSL.visit_ranking_page(context)

    factory_web_dsl(context).response_to_world(context)

# comment
@then('I should see comment_count {comment_count:d} '
      'in the package version detail')
def should_comment_count_in_the_package_version_detail(context, comment_count):
    WebDSL = factory_web_dsl(context)
    package_detail = WebDSL.response_structure_content(context)

    package_detail.get('comment_count') | should | equal_to(comment_count)

# package update
@then('I should see empty package update list')
def should_package_update_list_be_empty(context):
    results = factory_web_dsl(context).response_structure_content(context)
    results |should| be_empty
