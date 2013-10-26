# -*- coding: utf-8 -*-
__author__ = 'me'
from behave import *
from behaving.web.steps import *
from fts.tests.helpers import get_current_request
from should_dsl import should, should_not
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
    package = Package.objects.get(package_name=package_name)
    versions = {}
    for row in context.table:
        version = ApiDSL.\
            Given_package_has_version_with(context,
                                           package=package,
                                           version_name=row.get('version_name'),
                                           version_code=row.get('version_code'),
                                           status=PackageVersion.STATUS.published,
                                           all_datetime=row.get('released_datetime')
        )
        versions[int(row.get('version_code'))] = version
    context.world.update(dict(
        the_package=package,
        the_package_versions=versions,
        the_latest_version_code=min(list(versions.keys()))
    ))


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
def step_then_should_see_package_update_list_has_the_version(context,
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

@when('I access the package detail')
def step_when_i_access_the_package_detail(context):
    ApiDSL.When_i_access_package_detail(context, context.world.get('the_package'))


@when('I access comment list of the package')
def step_access_comment_list_of_the_package(context):
    ApiDSL.When_i_access_comment_list(context, context.world.get('the_package'))

@then('I should see comment_count {comment_count:d} in the package version detail')
def step_should_see_comment_count_in_the_package_version_detail(context, comment_count):
    package_detail = context.world.get('content')
    package_detail.get('comment_count') |should| equal_to(comment_count)

    for v in package_detail.get('versions'):
        v.get('comment_count') |should_not| be(None)

@given('package name "{title}" has a set of versions below')
def step_package_has_a_set_of_versions(context, title):
    package = ApiDSL.Given_i_have_package_with(context, title=title)
    versions = dict()
    for v in context.table:
        version = ApiDSL\
            .Given_package_has_version_with(context,
                                            package,
                                            version_code=int(v.get('version_code')),
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

@then('I should see the package commented by me in result list')
def step_should_see_commented_package_in_result_list(context):
    from mobapi.serializers import get_packageversion_comments_url
    results = context.world.get('content').get('results')
    except_package = results[0]
    the_package_versions = context.world.get('the_package_versions')
    latest_version_code = context.world.get('the_latest_version_code')
    the_latest_version = the_package_versions[latest_version_code]

    # comments_url has query string with content_type and object_pk
    # it can be compare different package version
    # FIXME choose other way to compare differenct package version
    comments_url = get_packageversion_comments_url(the_latest_version)
    absolute_comments_url = get_current_request() \
        .build_absolute_uri(comments_url)
    absolute_comments_url |should| equal_to(except_package.get('comments_url'))


@then('I should see the package summary from response in content results')
def step_should_see_the_package_summary_in_response_content_results(context):
    the_package = context.world.get('the_package')
    results = context.world.get('content').get('results', list())
    (the_package.package_name, ) |should| include_any_of([r.get('package_name') for r in results])

@then('I should see the package summary from response in content')
def step_should_see_the_package_summary_in_response_content(context):
    the_package = context.world.get('the_package')
    content = context.world.get('content')
    the_package.package_name |should| equal_to(content.get('package_name'))
