# -*- encoding=utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from fts.tests import helpers
from fts.tests.helpers import ApiDSL
from warehouse.models import Package, PackageVersion
from datetime import timedelta
from django.utils.timezone import now
import json
from django import forms

class RestApiTest(TestCase):

    def setUp(self):
        self.world = dict()
        self.client = Client(HTTP_ACCEPT='application/json')

    def convert_content(self, content):
        return json.loads(content.decode('utf-8'))

    def assertResultList(self, content, previous, next, count, result_len):
        self.assertEqual(content['previous'], next)
        self.assertEqual(content['next'], next)
        self.assertEqual(content['count'], count)
        self.assertEqual(len(content['results']), result_len)

    def assertIsUrl(self, url):
        try:
            forms.URLField(required=True).run_validators(url)
        except forms.ValidationError as err:
            self.fail(err.messages)

class NewestPackageTest(RestApiTest):

    def tearDown(self):
        helpers.clear_data()
        super(NewestPackageTest, self).tearDown()

    def test_should_see_package_list_all_be_published(self):
        # tomorrow will be published
        tomorrow = now()+timedelta(days=1)
        ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.published,
                                   released_datetime=tomorrow
                                   )
        # yestoday published
        yestoday = now()-timedelta(days=1)
        ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.published,
                                   released_datetime=yestoday
                                   )
        # yestoday unpublished or else status
        ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.unpublished,
                                   released_datetime=yestoday
                                   )
        ApiDSL.Given_i_have_package_with(self,
                                   released_datetime=yestoday,
                                   status=Package.STATUS.draft
                                   )
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_packages_list(self,num=1)
        helpers.clear_data()

    def test_should_see_package_list_orderby_released_datetime_desc(self):

        packages = ApiDSL.Given_i_have_some_packages(self, num=3)
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_packages_list(self, num=3)
        ApiDSL.Then_i_should_see_package_list_order_by_released_datetime_desc(self)

    def test_should_see_package_summary_information_for_list(self):

        helpers.create_package(package_name='com.gamecenter.rpg1',
                                     title='rpg 游戏 A',
                                     status=Package.STATUS.published,
                                     released_datetime=now()-timedelta(days=1)
        )
        ApiDSL.When_i_access_packages_newest(self)
        ApiDSL.Then_i_should_receive_success_response(self)

        ApiDSL.Then_i_should_see_packages_list(self,num=1)
        pkg_data = self.world.get('content').get('results')[0]
        ApiDSL.Then_i_should_see_package_summary_information_for_list(self,pkg_data)
        helpers.clear_data()

    def test_should_see_package_detail_information_in_detail(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg = helpers.create_package(package_name='com.gamecenter.rpg1',
                               title='rpg 游戏 A',
                               status=Package.STATUS.published,
                               released_datetime=yestoday,
                               created_datetime=yestoday,
                               updated_datetime=yestoday,
        )
        version1 = ApiDSL.Given_package_has_version_with(self, pkg,
                                                         all_datetime=yestoday ,
                                                         version_name='1.0beta', version_code=21010,
                                                         status=PackageVersion.STATUS.published)
        ApiDSL.Given_package_version_add_screenshot(self, version1)

        # new published version at today
        recently = today - timedelta(hours=2)
        version2 = ApiDSL.Given_package_has_version_with(self, pkg,
                                                         all_datetime=recently,
                                                         version_name='1.0beta2', version_code=21020,
                                                         status=PackageVersion.STATUS.published)
        ApiDSL.Given_package_version_add_screenshot(self, version2)

        ApiDSL.When_i_access_package_detail(self, pkg)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_package_detail_information(self,
            pkg_detail_data=self.world.get('content')
        )
        helpers.clear_data()
