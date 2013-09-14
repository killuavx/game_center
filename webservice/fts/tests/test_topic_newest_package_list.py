# -*- encoding=utf-8 -*-
from fts.tests import helpers
from fts.tests.helpers import ApiDSL, RestApiTest
from warehouse.models import Package, PackageVersion
from datetime import timedelta
from django.utils.timezone import now

class NewestTopicPackageTest(RestApiTest):

    def setUp(self):
        super(NewestTopicPackageTest, self).setUp()

    def tearDown(self):
        helpers.clear_data()
        super(NewestTopicPackageTest, self).tearDown()

    def Given_i_haven_topic_with_packages(self, *args, **kwargs):
        topic = ApiDSL.Given_i_have_topic_with(self,
                                               name='最新专区',
                                               slug='newest',
                                               status='published',
                                               **kwargs)
        for p in args:
            ApiDSL.Given_topic_add_item(self, topic=topic, item=p)

        return topic

    def test_should_see_package_list_all_be_published(self):
        # tomorrow will be published
        tomorrow = now()+timedelta(days=1)
        ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.published,
                                   released_datetime=tomorrow
                                   )
        # yestoday published
        yestoday = now()-timedelta(days=1)
        pkg1 = ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.published,
                                   released_datetime=yestoday
                                   )
        # yestoday unpublished or else status
        pkg2 = ApiDSL.Given_i_have_package_with(self,
                                   status=Package.STATUS.unpublished,
                                   released_datetime=yestoday
                                   )
        pkg3 = ApiDSL.Given_i_have_package_with(self,
                                   released_datetime=yestoday,
                                   status=Package.STATUS.draft
                                   )
        topic = self.Given_i_haven_topic_with_packages(pkg1, pkg2, pkg3,
                                               all_datetime=yestoday)
        self.assertTrue(topic.is_published())

        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self,num=1)
        helpers.clear_data()

    def test_should_see_package_list_orderby_released_datetime_desc(self):

        packages = ApiDSL.Given_i_have_some_packages(self, num=3)
        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=3)
        ApiDSL.Then_i_should_see_package_list_order_by_released_datetime_desc(self)

    def test_should_see_package_summary_information_for_list(self):

        helpers.create_package(package_name='com.gamecenter.rpg1',
                                     title='rpg 游戏 A',
                                     status=Package.STATUS.published,
                                     released_datetime=now()-timedelta(days=1)
        )
        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)

        ApiDSL.Then_i_should_see_result_list(self,num=1)
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

        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_package_detail_information(self,
            pkg_detail_data=self.world.get('content')
        )
        helpers.clear_data()
