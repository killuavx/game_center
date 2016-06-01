# -*- coding: utf-8 -*-
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl
from fts.features.app_dsls.clientapp import factory_dsl as factory_dsl

@when('I post package version to check update '
      'with package_name: "{package_name}", '
      'version_name: "{version_name}", version_code: "{version_code:d}"')
def post_package_update_version(context,
                                package_name,
                                version_name,
                                version_code):
    ClientAppDSL = factory_dsl(context)
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
