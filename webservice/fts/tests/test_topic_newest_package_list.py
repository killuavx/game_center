# -*- encoding=utf-8 -*-
from fts import helpers
from fts.helpers import ApiDSL, RestApiTest
from warehouse.models import Package, PackageVersion
from datetime import timedelta
from django.utils.timezone import now
from os.path import join
import os
from django.core.files import File
import io

class NewestTopicPackageTest(RestApiTest):

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
        pkg1 = ApiDSL.Given_i_have_published_package(self, title='pkg1', all_datetime=tomorrow)
        pkg1.released_datetime = tomorrow
        pkg1.save()

        # yestoday published
        yestoday = now()-timedelta(days=1)
        pkg2 = ApiDSL.Given_i_have_published_package(self, title='pkg2', all_datetime=yestoday)
        pkg2.released_datetime = yestoday
        pkg2.save()

        # yestoday unpublished or else status
        pkg3 = ApiDSL.Given_i_have_published_package(self, title='pkg3', all_datetime=yestoday)
        pkg3.released_datetime = yestoday
        pkg3.status = Package.STATUS.unpublished
        pkg3.save()

        pkg4 = ApiDSL.Given_i_have_published_package(self, title='pkg4', all_datetime=yestoday)
        pkg4.released_datetime = yestoday
        pkg4.status = Package.STATUS.draft
        pkg4.save()

        topic = self.Given_i_haven_topic_with_packages(pkg1, pkg2, pkg3, pkg4,
                                               all_datetime=yestoday)
        self.assertTrue(topic.is_published())

        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self,num=1)

    def test_should_see_package_list_orderby_released_datetime_desc(self):
        # tomorrow will be published
        tomorrow = now()-timedelta(days=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self, title='pkg1', all_datetime=tomorrow-timedelta(minutes=3))
        pkg1.released_datetime = pkg1.versions.get().released_datetime
        pkg1.save()
        pkg2 = ApiDSL.Given_i_have_published_package(self, title='pkg2', all_datetime=tomorrow-timedelta(minutes=2))
        pkg2.released_datetime = pkg2.versions.get().released_datetime
        pkg2.save()
        pkg3 = ApiDSL.Given_i_have_published_package(self, title='pkg3', all_datetime=tomorrow-timedelta(minutes=1))
        pkg3.released_datetime = pkg3.versions.get().released_datetime
        pkg3.save()

        topic = self.Given_i_haven_topic_with_packages(*(pkg1, pkg2, pkg3), all_datetime=tomorrow-timedelta(minutes=5))

        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=3)
        ApiDSL.Then_i_should_see_package_list_order_by_released_datetime_desc(self)

    def test_should_see_package_summary_information_for_list(self):
        yestoday = now()-timedelta(days=1)
        pkg = ApiDSL.Given_i_have_published_package(self, all_datetime=yestoday)
        topic = self.Given_i_haven_topic_with_packages(pkg, all_datetime=yestoday)
        self.assertTrue(topic.is_published())

        ApiDSL.When_i_access_topic_newest_package(self)
        ApiDSL.Then_i_should_receive_success_response(self)

        ApiDSL.Then_i_should_see_result_list(self,num=1)
        pkg_data = self.world.get('content').get('results')[0]
        ApiDSL.Then_i_should_see_package_summary_information_for_list(self,pkg_data)
        helpers.clear_data()

class PackageInfoRestApiTest(RestApiTest):

    def setUp(self):
        super(PackageInfoRestApiTest, self).setUp()
        self._fixture_dir = ApiDSL._fixtures_dir
        self._files = []

    def tearDown(self):
        super(PackageInfoRestApiTest, self).tearDown()
        for f in self._files:
            os.remove(f)

    def Given_package_version_has_data_integration_version_app(self, version ):
        cpkfilepath = join(self._fixture_dir, 'appexample/appdata-nodata-gpk.cpk')
        apkfilepath = join(self._fixture_dir, 'appexample/application.apk')
        version.download = File(io.FileIO(apkfilepath))
        version.di_download = File(io.FileIO(cpkfilepath))
        version.save()

        self._files.append(version.download.path)
        self._files.append(version.di_download.path)

    def test_should_see_package_detail_with_categories(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='pkg4',
                                                    all_datetime=yestoday)
        cat1 = helpers.create_category(name='Big Game', slug='big-game')
        cat2 = helpers.create_category(name='CN Game', slug='cn-game')
        cat3 = helpers.create_category(name='Single Game', slug='single-game')
        pkg.categories.add(cat1)
        pkg.categories.add(cat2)
        pkg.categories.add(cat3)
        pkg.released_datetime = yestoday
        pkg.save()

        ApiDSL.When_i_access_package_detail(self, pkg)
        ApiDSL.Then_i_should_receive_success_response(self)

        pkg_data = self.world.get('content')
        ApiDSL.Then_i_should_see_package_detail_information(self,
            pkg_detail_data=pkg_data
        )
        names = (cat1.name, cat2.name, cat3.name)
        ApiDSL.Then_i_should_see_package_detail_contains_categories_names(self,
            pkg_data=pkg_data,
            cat_names=names )

    def test_should_see_package_detail_cpk_download(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='pkg4',
                                                    all_datetime=yestoday)
        pkg.released_datetime = yestoday
        pkg.save()

        version = pkg.versions.all()[0]
        self.Given_package_version_has_data_integration_version_app(version)

        ApiDSL.When_i_access_package_detail(self, pkg)
        ApiDSL.Then_i_should_receive_success_response(self)
        pkg_data = self.world.get('content')
        ApiDSL.Then_i_should_see_package_detail_information(self,
                                                            pkg_detail_data=pkg_data
        )
        self.assertRegex(pkg_data.get('download'), '.*\.cpk$')

        except_version = pkg_data.get('versions')[0]
        self.assertRegex(except_version.get('download'), '.*\.cpk$')

    def test_should_see_package_detail_apk_download(self):
        yestoday = now() - timedelta(days=1)
        today = now() - timedelta(minutes=1)
        pkg = ApiDSL.Given_i_have_published_package(self,
                                                    title='pkg4',
                                                    all_datetime=yestoday)
        pkg.released_datetime = yestoday
        pkg.save()

        version = pkg.versions.all()[0]
        self.Given_package_version_has_data_integration_version_app(version)
        version.di_download = ''
        version.save()

        ApiDSL.When_i_access_package_detail(self, pkg)
        ApiDSL.Then_i_should_receive_success_response(self)
        pkg_data = self.world.get('content')
        ApiDSL.Then_i_should_see_package_detail_information(self,
                                                            pkg_detail_data=pkg_data
        )
        self.assertRegex(pkg_data.get('download'), '.*\.apk$')

        # version download url
        except_version = pkg_data.get('versions')[0]
        self.assertRegex(except_version.get('download'), '.*\.apk$')

