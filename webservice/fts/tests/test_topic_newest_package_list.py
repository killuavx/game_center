# -*- encoding=utf-8 -*-
from fts import helpers
from fts.helpers import ApiDSL, RestApiTest
from datetime import timedelta
from django.utils.timezone import now
from os.path import join
import os
from django.core.files import File
import io

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
        helpers.disconnect_packageversion_pre_save()
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

        helpers.connect_packageversion_pre_save()

    def test_should_see_package_detail_apk_download(self):
        helpers.disconnect_packageversion_pre_save()

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

        helpers.connect_packageversion_pre_save()

