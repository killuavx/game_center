# -*- coding: utf-8 -*-
from behave import *
from behaving.web.steps import *
from fts.helpers import ApiDSL
from fts.helpers import get_current_request
from should_dsl import should, should_not
from warehouse.models import Package, PackageVersion


@given('a set of packages in warehouse')
def step_given_a_set_of_packages_in_warehouse(context):
    for row in context.table:
        pkg = ApiDSL.Given_i_have_published_package(context,
                                                    title=row.get('title'),
                                                    package_name=row.get(
                                                        'package_name'),
                                                    version_code=int(row.get(
                                                        'version_code')),
                                                    version_name=row.get(
                                                        'version_name'),
                                                    all_datetime=row.get(
                                                        'released_datetime')
        )


@given('package "{package_name}" has a set of versions below')
def step_given_package_has_versions_below(context, package_name):
    package = Package.objects.get(package_name=package_name)
    versions = {}
    for row in context.table:
        version = ApiDSL. \
            Given_package_has_version_with(context,
                                           package=package,
                                           version_name=row.get('version_name'),
                                           version_code=row.get('version_code'),
                                           status=PackageVersion.STATUS.published,
                                           all_datetime=row.get(
                                               'released_datetime')
        )
        versions[int(row.get('version_code'))] = version
    context.world.update(dict(
        the_package=package,
        the_package_versions=versions,
        the_latest_version_code=min(list(versions.keys()))
    ))



@given('package name "{title}" has a set of versions below')
def step_package_has_a_set_of_versions(context, title):
    package = ApiDSL.Given_i_have_package_with(context, title=title)
    versions = dict()
    for v in context.table:
        version = ApiDSL \
            .Given_package_has_version_with(context,
                                            package,
                                            version_code=int(
                                                v.get('version_code')),
                                            version_name=v.get('version_name'),
                                            status=PackageVersion.STATUS.published,
                                            all_datetime=package.released_datetime)
        versions[int(v.get('version_code'))] = version
    package.status = Package.STATUS.published
    package.save()

    context.world.get('packages', dict()) \
        .update({package.package_name: package})
    context.world.update(dict(
        the_package=package,
        the_latest_version_code=min(list(versions.keys())),
        the_package_versions=versions,
    ))


from fts.features.app_dsls.warehouse import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl


@given('package exists such below')
def package_already_exists_below(context):
    WarehouseDSL = factory_dsl(context)
    for row in context.table:
        WarehouseDSL.create_package_without_ui(context, **row.as_dict())


@when('I visit the package detail title "{title}"')
def visit_the_package_detail(context, title):
    WarehouseDSL = factory_dsl(context)
    package = Package.objects.get(title=title)
    context.world.update(dict(
        the_package=package
    ))
    WarehouseDSL.visit_package_detail(context, package)

    factory_web_dsl(context).response_to_world(context)


@when('I follow the package {field}')
def follow_the_package(context, field):
    package = context.world.get('the_package')
    WarehouseDSL = factory_dsl(context)
    WarehouseDSL.visit_package_detail(context, package)
    WarehouseDSL.follow_package_detail_above(context, field)

    factory_web_dsl(context).response_to_world(context)

# comment
@then('I should see comment_count {comment_count:d} '
      'in the package version detail')
def should_comment_count_in_the_package_version_detail(context, comment_count):
    WebDSL = factory_web_dsl(context)
    package_detail = WebDSL.response_structure_content(context)

    package_detail.get('comment_count') | should | equal_to(comment_count)

    for v in package_detail.get('versions'):
        v.get('comment_count') | should_not | be(None)

# package update
@then('I should see empty package update list')
def should_package_update_list_be_empty(context):
    results = factory_web_dsl(context).response_structure_content(context)
    results |should| be_empty


from fts.features.app_dsls.clientapp import factory_dsl as factory_clientapp_dsl

@when('I post package version to check update '
      'with package_name: "{package_name}", '
      'version_name: "{version_name}", version_code: "{version_code:d}"')
def post_package_update_version(context,
                                package_name,
                                version_name,
                                version_code):
    ClientAppDSL = factory_clientapp_dsl(context)
    ClientAppDSL.post_package_to_update(context,
                                        package_name=package_name,
                                        version_code=version_code,
                                        version_name=version_name)
    factory_web_dsl(context).response_to_world(context)


@then('I should see package update list '
      'has the version package_name: "{package_name}", '
      'version_name: "{response_version_name}", '
      'version_code: "{response_version_code:d}", it can {is_updatable:be?} update')
def should_see_package_update_list_contains(context,
                                            package_name,
                                            response_version_name,
                                            response_version_code,
                                            is_updatable):
    def find_func(package):
        return package.get('package_name') == package_name and \
            package.get('version_code') == response_version_code and \
            package.get('version_name') == response_version_name and \
            package.get('is_updatable') == is_updatable

    WebDSL = factory_web_dsl(context)
    WebDSL.should_result_contains(context,
                                  within_pagination=False,
                                  find_func=find_func)
