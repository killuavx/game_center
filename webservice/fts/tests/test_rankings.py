# -*- encoding: utf-8-*-
from fts.tests.helpers import ApiDSL, RestApiTest
from datetime import timedelta
from django.utils.timezone import now
from warehouse.models import PackageVersion

class RankingsUnitTast(RestApiTest):

    def test_package_download_count_should_be_equal_sum_of_published_versions_download_count(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self, all_datetime=yestoday)
        v1 = pkg1.versions.all()[0]
        v1.download_count = 10
        v1.save()

        v2 = ApiDSL.Given_package_has_version_with(self,
                                                   package=pkg1,
                                                   version_code=2,
                                                   version_name='2v',
                                                   status=PackageVersion.STATUS.published,
                                                   all_datetime=yestoday,
                                                   )
        v2.download_count = 20
        v2.save()

        pkg1.released_datetime = yestoday
        pkg1.save()

        self.assertEqual(pkg1.download_count, 30)

    def test_package_download_count_should_be_equal_sum_of_published_versions_download_count_2(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self, all_datetime=yestoday)
        v1 = pkg1.versions.all()[0]
        v1.download_count = 10
        v1.save()
        v2 = ApiDSL.Given_package_has_version_with(self,
                                                   package=pkg1,
                                                   version_code=2,
                                                   version_name='2v',
                                                   status=PackageVersion.STATUS.published,
                                                   all_datetime=yestoday,
                                                   )
        v2.download_count = 20
        v2.save()
        v3 = ApiDSL.Given_package_has_version_with(self,
                                                   package=pkg1,
                                                   version_code=3,
                                                   version_name='3v',
                                                   status=PackageVersion.STATUS.draft,
                                                   all_datetime=yestoday,
                                                   )
        v3.download_count = 20
        v3.save()

        pkg1.released_datetime = yestoday
        pkg1.save()

        self.assertEqual(pkg1.download_count, 30)

class RankingsRestApiTest(RestApiTest):

    def test_should_see_package_detail_with_categories(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self, all_datetime=yestoday)
        pkg1.released_datetime = yestoday
        pkg1.download_count = 1213
        pkg1.save()

        pkg2 = ApiDSL.Given_i_have_published_package(self, all_datetime=yestoday)
        pkg2.released_datetime = yestoday
        pkg2.download_count = 123456
        pkg2.save()

        ApiDSL.When_i_access_rankings_list(self, rankings_type='total')
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=2)
        ApiDSL.Then_i_should_see_package_list_order_by_download_count_desc(self)


