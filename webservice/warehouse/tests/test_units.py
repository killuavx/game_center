# -*- encoding=utf-8 -*-
import os
import io
import shutil
from os.path import join, abspath, dirname
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.test.testcases import skipIf
from django.utils.timezone import timedelta, now
from django.core.files import File
from warehouse.utils.parser import PackageFileParser, set_package_parser_exe
from should_dsl import should, should_not
from mock import MagicMock
from fts import helpers
from warehouse.models import *
from fts.features.app_dsls import warehouse
from fts.features.app_dsls import taxonomy

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')


class WarehouseBaseUnitTest(TestCase):
    tags = []
    world = {}

    _fixture_dir = _fixture_dir
    _files_to_remove = []
    _count = 0

    def setUp(self):
        _dir = join(self._fixture_dir, 'temp')
        os.makedirs(_dir, exist_ok=True)
        self._files_to_remove.append(_dir)
        super(WarehouseBaseUnitTest, self).setUp()

        self.WarehouseDSL = warehouse.factory_dsl(self)
        self.WarehouseDSL.setup(self)
        self.TaxonomyDSL = taxonomy.factory_dsl(self)
        self.TaxonomyDSL.setup(self)
        self._count = 0

    def _create_author(self, **default):
        return self.create_author(**default)

    def tearDown(self):
        for f in self._files_to_remove:
            shutil.rmtree(f, ignore_errors=True)

        self.WarehouseDSL.teardown(self)
        self.TaxonomyDSL.teardown(self)

    def create_author(self, **kwargs):
        return self.WarehouseDSL.create_author_without_ui(self, **kwargs)

    def create_package(self, with_version=False, **kwargs):
        self._count += 1
        return self.WarehouseDSL.create_package_without_ui(
            self,
            with_version=with_version,
            **kwargs)

    def create_package_version(self, **kwargs):
        return self.WarehouseDSL.create_package_versions_without_ui(self,
                                                                    **kwargs)

    def create_screenshot(self, version):
        return self.WarehouseDSL.create_screenshot_without_ui(self, version)

    def create_category(self, **kwargs):
        return self.TaxonomyDSL.create_category(context=self, **kwargs)


class AuthorUnitTest(WarehouseBaseUnitTest):
    def test_basic_create(self):
        author = Author.objects.create(name="Martin Flower",
                                       email="martin-flower@testcase.com")
        self.assertEqual(author.status, Author.STATUS.draft)

        except_author = Author.objects.get(pk=author.pk)
        self.assertEqual(except_author.name, "Martin Flower")
        self.assertEqual(except_author.email, "martin-flower@testcase.com")
        self.assertEqual(except_author.phone, None)

        self.assertEqual(str(author), "Martin Flower")

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_image_to_path(self):
        author = Author(name="Chillingo International",
                        email="ChillingoInternational@testcase.com")
        icon = io.FileIO(join(self._fixture_dir, 'author-icon.png'))
        author.icon = File(icon)
        cover = io.FileIO(join(self._fixture_dir, 'author-cover.jpg'))
        author.cover = File(cover)
        author.save()

        path_pattern = r".*/author/%s/\d{2}-\d{6}" % now().strftime(
            "%Y%m%d%H%M")
        author.icon.path | should | be_like(join(path_pattern, "icon\.png"))
        author.cover.path | should | be_like(join(path_pattern, "cover\.jpg"))

    def test_change_status_from_draft_to_unactivated(self):
        author = self._create_author()
        self.assertEqual(author.status, Author.STATUS.draft)
        author.review()
        self.assertEqual(author.status, Author.STATUS.unactivated)

        author.save()
        self.assertEqual(author.status, Author.STATUS.unactivated)

    def test_change_status_from_unactivated_to_activated(self):
        author = self._create_author()
        author.status = Author.STATUS.unactivated
        self.assertEqual(author.status, Author.STATUS.unactivated)

        author.activate()
        self.assertEqual(author.status, Author.STATUS.activated)

    def test_change_status_from_activated_to_rejected(self):
        author = self._create_author()
        author.status = Author.STATUS.activated
        self.assertEqual(author.status, Author.STATUS.activated)

        author.reject()
        self.assertEqual(author.status, Author.STATUS.rejected)

    def test_change_status_from_rejected_to_activated(self):
        author = self._create_author()
        author.status = Author.STATUS.rejected
        self.assertEqual(author.status, Author.STATUS.rejected)

        author.appeal()
        self.assertEqual(author.status, Author.STATUS.unactivated)

    def test_change_status_from_rejected_to_draft(self):
        author = self._create_author()
        author.status = Author.STATUS.rejected
        self.assertEqual(author.status, Author.STATUS.rejected)

        author.recall()
        self.assertEqual(author.status, Author.STATUS.draft)


class PackageUnitTest(WarehouseBaseUnitTest):
    def setUp(self):
        super(PackageUnitTest, self).setUp()
        self.author = self.create_author(name="Martin Flower",
                                         email="martin-flower@testcase.com")

    def test_basic_create(self):
        pkg = Package(title="谷歌地图", package_name="com.google.apps.map")
        pkg.author = self.author
        pkg.save()

        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertEqual(except_pkg.title, "谷歌地图")
        self.assertEqual(except_pkg.package_name, "com.google.apps.map")
        self.assertEqual(str(except_pkg), "谷歌地图")

        self.assertEqual(except_pkg.summary, "")
        self.assertEqual(except_pkg.description, "")

        # datetime compare with created_datetime, updated_datetime and released_time
        timenow = now().utcnow()
        self.assertEqual(except_pkg.released_datetime, None)
        created_timedelta = timenow - except_pkg.created_datetime.utcnow()
        self.assertLess(created_timedelta, timedelta(seconds=1))
        updated_timedelta = timenow - except_pkg.updated_datetime.utcnow()
        self.assertLess(updated_timedelta, timedelta(seconds=1))

        except_author = pkg.author
        self.assertEqual(except_author.name, "Martin Flower")

    def _create_with_one_version(self):
        return helpers.create_package(title="梦幻西游",
                                      package_name="com.menghuan.xiyou",
                                      author=self.author)

    def test_change_status_bewteen_draft_to_unpublished(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)

        pkg.review()
        self.assertEqual(pkg.status, Package.STATUS.unpublished)

    def test_status_not_support_changed_between_unpublished_and_published(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)

        pkg.review() # from Draft to Unpublished
        pkg.publish() # from Unpublished to published
        self.assertEqual(pkg.status, Package.STATUS.published)

        # Status Changed Not Support from Published to Unpublished
        with self.assertRaises(StatusNotSupportAction):
            pkg.unpublish()

    def test_change_status_between_unpublished_and_rejected(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)

        pkg.reject() # from Unpublished to Rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)
        pkg.appeal() # from Rejected to Unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)

    def test_change_status_between_rejected_and_draft(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)

        pkg.recall() # from Rejected to Draft
        self.assertEqual(pkg.status, Package.STATUS.draft)

    def test_change_status_between_published_and_reject(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.published
        self.assertEqual(pkg.status, Package.STATUS.published)

        pkg.reject()
        self.assertEqual(pkg.status, Package.STATUS.rejected)

    def test_status_draft_transactions_migration(self):
        pkg = self._create_with_one_version()
        self.assertEqual(pkg.status, Package.STATUS.draft)
        self.assertEqual(pkg.next_statuses, (Package.STATUS.unpublished,))
        self.assertEqual(pkg.next_actions, ('review',))
        self.assertEqual(pkg.next_transactions(),
                         ( ('review', Package.STATUS.unpublished), ))

    def test_status_unpublished_transactions_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.unpublished
        self.assertEqual(pkg.status, Package.STATUS.unpublished)
        self.assertEqual(pkg.next_statuses,
                         (Package.STATUS.published, Package.STATUS.rejected))
        self.assertEqual(pkg.next_actions, ( 'publish', 'reject'))
        self.assertEqual(pkg.next_transactions(), (
            ('publish', Package.STATUS.published),
            ('reject', Package.STATUS.rejected), )
        )

    def test_status_rejected_transactions_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.rejected
        self.assertEqual(pkg.status, Package.STATUS.rejected)

        self.assertEqual(pkg.next_statuses,
                         (Package.STATUS.draft, Package.STATUS.unpublished))
        self.assertEqual(pkg.next_actions, ('recall', 'appeal'))
        self.assertEqual(pkg.next_transactions(), (
            ('recall', Package.STATUS.draft),
            ('appeal', Package.STATUS.unpublished), )
        )

    def test_status_published_transaction_migration(self):
        pkg = self._create_with_one_version()
        pkg.status = Package.STATUS.published
        self.assertEqual(pkg.status, Package.STATUS.published)
        self.assertEqual(pkg.next_statuses, (Package.STATUS.rejected,))
        self.assertEqual(pkg.next_actions, ('reject',))
        self.assertEqual(pkg.next_transactions(), (
            ('reject', Package.STATUS.rejected), )
        )


class PackageManagerUnitTest(WarehouseBaseUnitTest):
    _count = 0

    def test_package_version_has_many_screenshots(self):
        yestoday = now() - timedelta(days=1)
        pkg = self.create_package(
            status=Package.STATUS.published,
            released_datetime=yestoday,
            with_version=False,
        )
        version = self.create_package_version(
            package=pkg,
            version_code=1,
            version_name='1.0beta',
            all_datetime=yestoday,
            status=PackageVersion.STATUS.published
        )
        self.create_screenshot(version=version)

        except_pkg = Package.objects.get(pk=pkg.pk)
        except_version = except_pkg.versions.get()
        self.assertEqual(except_version.screenshots.count(), 1)
        except_ss = except_version.screenshots.get()
        self.assertIsNotNone(except_ss.image.url)
        except_ss.delete()

    def create_package(self, status=None, released_datetime=None, **kwargs):
        self._count += 1
        pkg = super(PackageManagerUnitTest, self).create_package(
            package_name='com.gamecenter.%d' % self._count,
            title='游戏%d' % self._count,
            status=status,
            released_datetime=released_datetime,
            **kwargs
        )
        return pkg

    def test_package_main_category(self):
        tomorrow = now() + timedelta(days=1)
        pkg = self.create_package(
            status=Package.STATUS.published,
            released_datetime=tomorrow
        )
        self.assertIsNone(pkg.main_category)
        cat1 = self.create_category(name='Big Game', slug='big-game')
        cat2 = self.create_category(name='CN Game', slug='cn-game')
        cat3 = self.create_category(name='Single Game', slug='single-game')

        pkg.categories.add(cat1)
        pkg.categories.add(cat2)
        pkg.categories.add(cat3)

        except_cat = pkg.main_category
        self.assertEqual(except_cat, cat1)

    def test_published_list_should_all_status_ok(self):
        # tomorrow will be published
        tomorrow = now() + timedelta(days=1)
        self.create_package(
            status=Package.STATUS.published,
            released_datetime=tomorrow
        )
        # yestoday published
        yestoday = now() - timedelta(days=1)
        self.create_package(
            status=Package.STATUS.published,
            released_datetime=yestoday
        )
        # yestoday unpublished or else status
        self.create_package(
            status=Package.STATUS.unpublished,
            released_datetime=yestoday
        )
        self.create_package(
            released_datetime=yestoday,
            status=Package.STATUS.draft
        )
        published_pkgs_set = Package.objects.published()
        self.assertEqual(1, published_pkgs_set.count())

        pub_pkgs = published_pkgs_set.all()
        pkg = pub_pkgs[0]
        self.assertEqual(pkg.status, Package.STATUS.published)


class PackageVersionUnitTest(WarehouseBaseUnitTest):
    def test_basic_create(self):
        pkg = self.create_package(
            package_name='com.warehouse.tests.packageversion.%s' % helpers.guid()
        )
        pkgversion = PackageVersion(
            version_name='1.0beta',
            version_code=1004,
            whatsnew='all new!'
        )
        pkg.versions.add(pkgversion)
        self.assertEqual(pkgversion.version_code, 1004)
        self.assertEqual(pkgversion.version_name, '1.0beta')
        self.assertEqual(pkgversion.whatsnew, 'all new!')

        except_pkgversion = Package.objects.get(pk=pkg.pk).versions.get()
        self.assertEqual(except_pkgversion, pkgversion)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_file_to_path(self):
        helpers.disconnect_packageversion_pre_save()
        pkg = self.create_package(
            package_name='com.warehouse.tests.packageversion.%s' % helpers.guid()
        )
        icon = io.FileIO(join(self._fixture_dir, 'tinysize-icon.png'))
        cover = io.FileIO(join(self._fixture_dir, 'tinysize-cover.jpg'))
        download = io.FileIO(join(self._fixture_dir, 'tinysize.apk'))
        di_download = io.FileIO(join(self._fixture_dir, 'tinysize.cpk'))
        pkgversion = PackageVersion(
            version_name='1.0beta',
            version_code=1004,
            whatsnew='all new!',
            icon=File(icon),
            cover=File(cover),
            download=File(download),
            di_download=File(di_download)
        )
        pkg.versions.add(pkgversion)

        except_version = Package.objects.get(pk=pkg.pk).versions.get()
        version_path = 'package/%d/v%d' % (pkg.pk, except_version.version_code)
        except_version.icon.path | should | end_with(
            join(version_path, 'icon.png'))
        except_version.cover.path | should | end_with(
            join(version_path, 'cover.jpg'))
        except_version.download.path | should | end_with(
            join(version_path, 'application.apk'))
        except_version.di_download.path | should | end_with(
            join(version_path, 'application-di.cpk'))

        helpers.connect_packageversion_pre_save()


    def test_should_package_with_version(self):
        pkg = self.create_package(
            package_name='com.warehouse.tests.packageversion.%s' % helpers.guid()
        )
        version1 = PackageVersion(
            version_name='1.0beta2',
            version_code=1014,
            whatsnew='all new!'
        )
        version2 = PackageVersion(
            version_name='1.0beta3',
            version_code=1024,
            whatsnew='all new!'
        )
        pkg.versions.add(version1)
        pkg.versions.add(version2)

        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertEqual(except_pkg.versions.latest('version_code'), version2)

    def test_package_should_change_updated_datetime_sync_with_latest_published_version(
            self):
        yestoday = now() - timedelta(days=1)
        pkg = self.create_package(with_version=False,
                                  package_name='com.tests.%s' % helpers.guid(),
                                  released_datetime=yestoday,
                                  updated_datetime=yestoday,
                                  created_datetime=yestoday)

        # published version at yestoday
        today = now() - timedelta(minutes=1)
        version1 = self.create_package_version(
            package=pkg,
            version_name='1.0beta',
            version_code=11010,
            status=PackageVersion.STATUS.published,
            released_datetime=yestoday,
            updated_datetime=yestoday,
            created_datetime=yestoday)

        # new published version at today
        recently = today - timedelta(hours=2)
        version2 = self.create_package_version(
            package=pkg,
            version_name='1.0beta2',
            version_code=11020,
            status=PackageVersion.STATUS.draft,
            released_datetime=recently,
            updated_datetime=recently,
            created_datetime=recently)

        # package updated_datetime should be same with latest published version 1.0beta
        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertGreater(timedelta(seconds=1),
                           version1.updated_datetime - except_pkg.updated_datetime)

    def test_package_should_change_updated_datetime_sync_with_latest_published_version_v2(
            self):
        yestoday = now() - timedelta(days=1)
        pkg = self.create_package(with_version=False,
                                  package_name='com.tests.%s' % helpers.guid(),
                                  released_datetime=yestoday,
                                  updated_datetime=yestoday,
                                  created_datetime=yestoday)
        # published version at yestoday
        today = now() - timedelta(minutes=1)
        version1 = self.create_package_version(
            package=pkg,
            version_name='1.0beta',
            version_code=21010,
            status=PackageVersion.STATUS.published,
            released_datetime=yestoday,
            updated_datetime=yestoday,
            created_datetime=yestoday)

        # new published version at today
        recently = today - timedelta(hours=2)
        version2 = self.create_package_version(
            package=pkg,
            version_name='1.0beta2',
            version_code=21020,
            status=PackageVersion.STATUS.published,
            released_datetime=yestoday,
            updated_datetime=yestoday,
            created_datetime=yestoday)

        # package updated_datetime should be same with latest published version 1.0beta2
        except_pkg = Package.objects.get(pk=pkg.pk)
        self.assertGreater(timedelta(seconds=1),
                           version2.updated_datetime - except_pkg.updated_datetime)


class PackageScreenshotUnitTest(WarehouseBaseUnitTest):
    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_package_version_screenshot_upload_to_path(self):
        yestoday = now() - timedelta(days=1)
        pkg = self.create_package(package_name='com.tests.packageversion.upload')
        version = self.create_package_version(package=pkg,
                                              version_code=1,
                                              version_name='1.0beta',
                                              released_datetime=yestoday)
        screenshot = self.create_screenshot(version=version)

        except_version = Package.objects.get(pk=pkg.pk).versions.get()
        version_path = 'package/%d/v%d' % (pkg.pk, except_version.version_code)
        except_screenshot = except_version.screenshots.get()
        image_basename = basename(except_screenshot.image.name)
        except_screenshot.image.path | should | end_with(
            join(version_path, 'screenshot', image_basename))


def pkg_profile_text():
    return """package: name='solitairelite.solitaire' versionCode='4' versionName='1.3'
sdkVersion:'3'
application-label:'Solitaire'
application-icon-160:'res/drawable/solitaire_icon.png'
application: label='Solitaire' icon='res/drawable/solitaire_icon.png'
launchable-activity: name='solitairelite.solitaire.Solitaire'  label='Solitaire' icon=''
uses-permission:'android.permission.INTERNET'
uses-permission:'android.permission.ACCESS_NETWORK_STATE'
uses-permission:'android.permission.WRITE_EXTERNAL_STORAGE'
uses-implied-permission:'android.permission.WRITE_EXTERNAL_STORAGE','targetSdkVersion < 4'
uses-permission:'android.permission.READ_PHONE_STATE'
uses-implied-permission:'android.permission.READ_PHONE_STATE','targetSdkVersion < 4'
uses-permission:'android.permission.READ_EXTERNAL_STORAGE'
uses-implied-permission:'android.permission.READ_EXTERNAL_STORAGE','requested WRITE_EXTERNAL_STORAGE'
uses-feature:'android.hardware.touchscreen'
uses-implied-feature:'android.hardware.touchscreen','assumed you require a touch screen unless explicitly made optional'
main
other-activities
supports-screens: 'normal'
supports-any-density: 'false'
locales: '--_--'
densities: '160'
"""


def pkg_complex_profile_text():
    return """package: name='com.eamobile.bejeweled2_na_wf' versionCode='2007700' versionName='2.0.10'
sdkVersion:'4'
maxSdkVersion:'13'
targetSdkVersion:'7'
application-label:'Bejeweled 2'
application-icon-120:'res/drawable-ldpi/icon.png'
application-icon-160:'res/drawable-mdpi/icon.png'
application-icon-240:'res/drawable-hdpi/icon.png'
application: label='Bejeweled 2' icon='res/drawable-mdpi/icon.png'
launchable-activity: name='com.inject.InjectActivity'  label='' icon=''
uses-permission:'android.permission.WAKE_LOCK'
uses-permission:'android.permission.VIBRATE'
uses-permission:'android.permission.WRITE_EXTERNAL_STORAGE'
uses-permission:'android.permission.READ_PHONE_STATE'
uses-permission:'android.permission.INTERNET'
uses-permission:'android.permission.READ_PHONE_STATE'
uses-permission:'android.permission.ACCESS_WIFI_STATE'
uses-permission:'android.permission.ACCESS_NETWORK_STATE'
uses-permission:'com.android.vending.CHECK_LICENSE'
uses-feature:'android.hardware.telephony'
uses-feature:'android.hardware.touchscreen'
compatible-screens:'200/120','200/240','200/160','200/320','300/120','300/240','300/160','300/320','400/120','400/160','400/240','400/320'
uses-permission:'android.permission.READ_EXTERNAL_STORAGE'
uses-implied-permission:'android.permission.READ_EXTERNAL_STORAGE','requested WRITE_EXTERNAL_STORAGE'
uses-feature:'android.hardware.wifi'
uses-implied-feature:'android.hardware.wifi','requested android.permission.ACCESS_WIFI_STATE, android.permission.CHANGE_WIFI_STATE, or android.permission.CHANGE_WIFI_MULTICAST_STATE permission'
uses-feature:'android.hardware.screen.portrait'
uses-implied-feature:'android.hardware.screen.portrait','one or more activities have specified a portrait orientation'
main
other-activities
supports-screens: 'small' 'normal' 'large'
supports-any-density: 'true'
locales: '--_--'
densities: '120' '160' '240'
native-code: 'armeabi'"""


def pkg_mutil_languages_profile_text():
    return """package: name='com.limbic.ac130' versionCode='1379701800' versionName='1.9.1'
sdkVersion:'10'
targetSdkVersion:'17'
supports-gl-texture:'GL_OES_compressed_ETC1_RGB8_texture'
uses-permission:'android.permission.ACCESS_NETWORK_STATE'
uses-permission:'android.permission.GET_ACCOUNTS'
uses-permission:'android.permission.READ_PHONE_STATE'
uses-permission:'android.permission.INTERNET'
uses-permission:'com.android.vending.BILLING'
application-label:'Zombie GS'
application-label-ca:'Zombie GS'
application-label-da:'Zombie GS'
application-label-fa:'Zombie GS'
application-label-ja:'Zombie GS'
application-label-nb:'Zombie GS'
application-label-be:'Zombie GS'
application-label-de:'Zombie GS'
application-label-he:'Zombie GS'
application-label-af:'Zombie GS'
application-label-bg:'Zombie GS'
application-label-th:'Zombie GS'
application-label-fi:'Zombie GS'
application-label-hi:'Zombie GS'
application-label-vi:'Zombie GS'
application-label-sk:'Zombie GS'
application-label-uk:'Zombie GS'
application-label-el:'Zombie GS'
application-label-nl:'Zombie GS'
application-label-pl:'Zombie GS'
application-label-sl:'Zombie GS'
application-label-tl:'Zombie GS'
application-label-am:'Zombie GS'
application-label-in:'Zombie GS'
application-label-ko:'Zombie GS'
application-label-ro:'Zombie GS'
application-label-ar:'Zombie GS'
application-label-fr:'Zombie GS'
application-label-hr:'Zombie GS'
application-label-sr:'Zombie GS'
application-label-tr:'Zombie GS'
application-label-cs:'Zombie GS'
application-label-es:'Zombie GS'
application-label-ms:'Zombie GS'
application-label-et:'Zombie GS'
application-label-it:'Zombie GS'
application-label-lt:'Zombie GS'
application-label-pt:'Zombie GS'
application-label-hu:'Zombie GS'
application-label-ru:'Zombie GS'
application-label-zu:'Zombie GS'
application-label-lv:'Zombie GS'
application-label-sv:'Zombie GS'
application-label-iw:'Zombie GS'
application-label-sw:'Zombie GS'
application-label-en_GB:'Zombie GS'
application-label-zh_CN:'Zombie GS'
application-label-pt_BR:'Zombie GS'
application-label-es_US:'Zombie GS'
application-label-pt_PT:'Zombie GS'
application-label-zh_TW:'Zombie GS'
application-icon-120:'res/drawable/icon.png'
application-icon-160:'res/drawable-mdpi/icon.png'
application-icon-240:'res/drawable-hdpi/icon.png'
application-icon-320:'res/drawable-xhdpi/icon.png'
application-icon-480:'res/drawable-xxhdpi/icon.png'
application: label='Zombie GS' icon='res/drawable-mdpi/icon.png'
launchable-activity: name='com.lion.WelcomeActivity'  label='Zombie GS' icon=''
uses-feature:'android.hardware.touchscreen'
uses-implied-feature:'android.hardware.touchscreen','assumed you require a touch screen unless explicitly made optional'
uses-feature:'android.hardware.screen.landscape'
uses-implied-feature:'android.hardware.screen.landscape','one or more activities have specified a landscape orientation'
main
other-activities
other-receivers
other-services
supports-screens: 'normal' 'large' 'xlarge'
supports-any-density: 'true'
locales: '--_--' 'ca' 'da' 'fa' 'ja' 'nb' 'be' 'de' 'he' 'af' 'bg' 'th' 'fi' 'hi' 'vi' 'sk' 'uk' 'el' 'nl' 'pl' 'sl' 'tl' 'am' 'in' 'ko' 'ro' 'ar' 'fr' 'hr' 'sr' 'tr' 'cs' 'es' 'ms' 'et' 'it' 'lt' 'pt' 'hu' 'ru' 'zu' 'lv' 'sv' 'iw' 'sw' 'en_GB' 'zh_CN' 'pt_BR' 'es_US' 'pt_PT' 'zh_TW'
densities: '120' '160' '240' '320' '480'
native-code: 'armeabi'"""


from warehouse.utils.parse_handle import *


class PkgCreateWithPackageFileParserUnitTest(WarehouseBaseUnitTest):
    class MockPackageFileParser(PackageFileParser):
        def badging_text(self):
            return pkg_profile_text()

    class MockParsePackageVersion(ParsePackageVersion):
        def fetch_icon_to_version(self):
            icon_filename = join(WarehouseBaseUnitTest._fixture_dir, 'icon.png')
            self._version.icon = File(io.File(icon_filename))

    def setUp(self):
        super(PkgCreateWithPackageFileParserUnitTest, self).setUp()
        AAPT_CMD = settings.AAPT_CMD
        set_package_parser_exe(AAPT_CMD)
        self._pkgfile = join(self._fixture_dir, 'tinysize.apk')

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'),
                       PACKAGE_FILE_PARSE_OPTS=dict(
                           package_version_parser_class=MockPackageFileParser,
                           package_version_parse_handle=MockParsePackageVersion
                       ))
    def test_autofill_package_detail(self):
        parser = self.MockPackageFileParser(self._pkgfile)
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        version.save()

        version.package.package_name | should | equal_to(
            parser.package.get('package_name'))
        parser.package.get('package_name') | should | equal_to(
            'solitairelite.solitaire')
        version.version_code | should | equal_to(4)
        version.version_code | should | equal_to(
            parser.package.get('version_code'))
        version.version_name | should | equal_to('1.3')
        version.version_name | should | equal_to(
            parser.package.get('version_name'))

        version.package.title | should | equal_to(parser.application_labels[''])
        version.package.author_id | should | equal_to(-1)

        version.icon | should_not | be_empty


class ParsePackageVersionUnitTest(WarehouseBaseUnitTest):
    _fixture_dir = _fixture_dir

    def setUp(self):
        AAPT_CMD = settings.AAPT_CMD
        set_package_parser_exe(AAPT_CMD)
        self._pkgfile = join(self._fixture_dir, 'tinysize.apk')
        super(ParsePackageVersionUnitTest, self).setUp()

    def _mock_badging_text(self, parser, return_value):
        parser.badging_text = MagicMock(return_value=return_value)

    def test_parse_to_package(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)

        expect_version = parse_handle.parse_to_version()
        version | should | be(expect_version)
        package = parse_handle.parse_to_package()
        package | should | equal_to(version.package)
        package.package_name | should | equal_to(
            parser.package.get('package_name'))

    def test_choose_icon_density(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)

        # choose_icon_density
        # case 1
        [int(k) for k in
         parser.application_icons.keys()] | should | include_all_of([
            120, #    4
            160, #    3
            240, #    2
            320, # <--1
            480  #    5
        ])
        parse_handle.choose_icon_density() | should | equal_to(320)

        # case 2
        import copy

        application_icons = copy.deepcopy(parser.application_icons)
        icons = copy.deepcopy(application_icons)
        icons.pop('320')
        icons.pop('240')
        [int(k) for k in icons.keys()] | should | include_all_of([
            120,
            160,
            480
        ])
        parser.application_icons = icons # mock data
        parse_handle.choose_icon_density() | should | equal_to(160)

        # case 3
        icons = copy.deepcopy(application_icons)
        icons.pop('120')
        icons.pop('160')
        icons.pop('240')
        val = icons.pop('320')
        icons['520'] = val
        [int(k) for k in icons.keys()] | should | include_all_of([
            480,
            520
        ])
        parser.application_icons = icons
        parse_handle.choose_icon_density() | should | equal_to(480)

    def test_parse_to_version(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)
        expect_version = parse_handle.parse_to_version()

        expect_version | should | be(version)
        expect_version.version_code | should | equal_to(
            parser.package.get('version_code'))
        expect_version.version_name | should | equal_to(
            parser.package.get('version_name'))

    @skipIf(settings.AAPT_CMD is None, 'ignore parse with no aapt support')
    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'),
                       UNZIP_FILE_TEMP_DIR=join(_fixture_dir, 'temp/unzipdir'))
    def test_fetch_icon_to_version(self):
        parser = PackageFileParser(self._pkgfile)
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)
        parse_handle._unzip_file_temp_dir = settings.UNZIP_FILE_TEMP_DIR
        expect_version = parse_handle.fetch_icon_to_version()
        expect_version.icon.size | should | equal_to(4982)

    def test_choose_locale(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)

        parser.locales = ['zh_CN', 'zh_TW', 'en_GB', 'fr']
        parse_handle.choose_locale() | should | equal_to('zh_CN')

        parser.locales = ['en_GB', 'zh_TW', 'fr']
        parse_handle.choose_locale() | should | equal_to('zh_TW')

        parser.locales = ['fr', 'en_GB']
        parse_handle.choose_locale() | should | equal_to('en_GB')

        parser.locales = ['en_GB', 'zh', 'zh_TW', 'en']
        parse_handle.choose_locale() | should | equal_to('zh')

        parser.locales = ['en_GB', 'fr', 'en']
        parse_handle.choose_locale() | should | equal_to('en')

        parser.locales = ['fr']
        parse_handle.choose_locale() | should | be(None)

    def test_choose_locale(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())
        version = PackageVersion()
        version.download = File(io.FileIO(self._pkgfile))
        parse_handle = ParsePackageVersion(version, parser)

        parse_handle.choose_locale() | should | equal_to('zh_CN')

        package = parse_handle.parse_to_package()
        package.title | should | equal_to(parser.application_labels['zh_CN'])
