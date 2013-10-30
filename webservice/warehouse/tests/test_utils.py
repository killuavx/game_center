# -*- coding: utf-8 -*-
import os
from os.path import abspath, dirname, join
import shutil
from django.test.testcases import TestCase, skipIf
from django.conf import settings
from warehouse.utils.parser import *
from warehouse.utils.parse_handle import *
from mock import MagicMock
from should_dsl import should

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')


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


class PackageFileParserUnitTest(TestCase):

    _fixture_dir = _fixture_dir

    def setUp(self):
        AAPT_CMD=settings.AAPT_CMD
        set_package_parser_exe(AAPT_CMD)
        self._pkgfile = join(self._fixture_dir, 'tinysize.apk')

    def _mock_badging_text(self, parser, return_value):
        parser.badging_text = MagicMock(return_value=return_value)

    def test_base_parser(self):
        parser = PackageFileParser(self._pkgfile)
        if not settings.AAPT_CMD:
            self._mock_badging_text(parser, pkg_profile_text())
        parser.package['package_name'] |should| equal_to('solitairelite.solitaire')
        parser.package['version_code'] |should| equal_to(4)
        parser.package['version_name'] |should| equal_to('1.3')
        parser.sdk_version |should| equal_to(3)

        parser.application_labels |should| equal_to({
            '': 'Solitaire',
        })
        parser.application_icons |should| equal_to({
            '160': 'res/drawable/solitaire_icon.png',
        })

        parser.uses_permissions |should| equal_to([
            'android.permission.INTERNET',
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.READ_PHONE_STATE',
            'android.permission.READ_EXTERNAL_STORAGE'
        ])
        parser.uses_implied_permissions |should| equal_to({
            'android.permission.WRITE_EXTERNAL_STORAGE': 'targetSdkVersion < 4',
            'android.permission.READ_PHONE_STATE': 'targetSdkVersion < 4',
            'android.permission.READ_EXTERNAL_STORAGE': 'requested WRITE_EXTERNAL_STORAGE',
        })

        parser.uses_features |should| equal_to([
            'android.hardware.touchscreen',
        ])
        parser.uses_implied_features |should| equal_to({
            'android.hardware.touchscreen': 'assumed you require a touch screen unless explicitly made optional'
        })
        parser.densities |should| equal_to([160])
        parser.locales |should| equal_to(['--_--'])
        parser.supports_screens |should| equal_to(['normal'])

    def test_complex_parse(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_complex_profile_text())

        parser.package.get('package_name') |should| equal_to('com.eamobile.bejeweled2_na_wf')
        parser.package.get('version_code') |should| equal_to(2007700)
        parser.package.get('version_name') |should| equal_to('2.0.10')

        parser.target_sdk_version |should| equal_to(7)
        parser.sdk_version |should| equal_to(4)
        parser.max_sdk_version |should| equal_to(13)

        parser.application_icons |should| equal_to({
            '120': 'res/drawable-ldpi/icon.png',
            '160': 'res/drawable-mdpi/icon.png',
            '240': 'res/drawable-hdpi/icon.png',
        })
        parser.application_labels |should| equal_to({
            '': 'Bejeweled 2',
        })

        parser.uses_permissions |should| equal_to([
            'android.permission.WAKE_LOCK',
            'android.permission.VIBRATE',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.READ_PHONE_STATE',
            'android.permission.INTERNET',
            'android.permission.READ_PHONE_STATE',
            'android.permission.ACCESS_WIFI_STATE',
            'android.permission.ACCESS_NETWORK_STATE',
            'com.android.vending.CHECK_LICENSE',
            'android.permission.READ_EXTERNAL_STORAGE',
        ])
        parser.uses_implied_permissions |should| equal_to({
            'android.permission.READ_EXTERNAL_STORAGE': 'requested WRITE_EXTERNAL_STORAGE',
        })

        parser.uses_features |should| equal_to([
            'android.hardware.telephony',
            'android.hardware.touchscreen',
            'android.hardware.wifi',
            'android.hardware.screen.portrait'
        ])
        parser.uses_implied_features |should| equal_to({
            'android.hardware.wifi': 'requested android.permission.ACCESS_WIFI_STATE, android.permission.CHANGE_WIFI_STATE, or android.permission.CHANGE_WIFI_MULTICAST_STATE permission',
            'android.hardware.screen.portrait': 'one or more activities have specified a portrait orientation',
        })

        parser.supports_screens |should| equal_to([
            'small',
            'normal',
            'large',
        ])

        parser.densities |should| equal_to([
            120,
            160,
            240
        ])

        parser.native_code |should| equal_to('armeabi')

    def test_mutil_languages_parse(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())

        parser.package.get('package_name') |should| equal_to('com.limbic.ac130')
        parser.package.get('version_code') |should| equal_to(1379701800)
        parser.package.get('version_name') |should| equal_to('1.9.1')

        parser.sdk_version |should| equal_to(10)
        parser.target_sdk_version |should| equal_to(17)

        parser.application_icons |should| equal_to({
            '120': 'res/drawable/icon.png',
            '160': 'res/drawable-mdpi/icon.png',
            '240': 'res/drawable-hdpi/icon.png',
            '320': 'res/drawable-xhdpi/icon.png',
            '480': 'res/drawable-xxhdpi/icon.png',
        })

        parser.application_labels |should| equal_to({
            '': 'Zombie GS',
            'ca': 'Zombie GS',
            'da': 'Zombie GS',
            'fa': 'Zombie GS',
            'ja': 'Zombie GS',
            'nb': 'Zombie GS',
            'be': 'Zombie GS',
            'de': 'Zombie GS',
            'he': 'Zombie GS',
            'af': 'Zombie GS',
            'bg': 'Zombie GS',
            'th': 'Zombie GS',
            'fi': 'Zombie GS',
            'hi': 'Zombie GS',
            'vi': 'Zombie GS',
            'sk': 'Zombie GS',
            'uk': 'Zombie GS',
            'el': 'Zombie GS',
            'nl': 'Zombie GS',
            'pl': 'Zombie GS',
            'sl': 'Zombie GS',
            'tl': 'Zombie GS',
            'am': 'Zombie GS',
            'in': 'Zombie GS',
            'ko': 'Zombie GS',
            'ro': 'Zombie GS',
            'ar': 'Zombie GS',
            'fr': 'Zombie GS',
            'hr': 'Zombie GS',
            'sr': 'Zombie GS',
            'tr': 'Zombie GS',
            'cs': 'Zombie GS',
            'es': 'Zombie GS',
            'ms': 'Zombie GS',
            'et': 'Zombie GS',
            'it': 'Zombie GS',
            'lt': 'Zombie GS',
            'pt': 'Zombie GS',
            'hu': 'Zombie GS',
            'ru': 'Zombie GS',
            'zu': 'Zombie GS',
            'lv': 'Zombie GS',
            'sv': 'Zombie GS',
            'iw': 'Zombie GS',
            'sw': 'Zombie GS',
            'en_GB': 'Zombie GS',
            'zh_CN': 'Zombie GS',
            'pt_BR': 'Zombie GS',
            'es_US': 'Zombie GS',
            'pt_PT': 'Zombie GS',
            'zh_TW': 'Zombie GS',
        })

        parser.uses_permissions |should| equal_to([
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.GET_ACCOUNTS',
            'android.permission.READ_PHONE_STATE',
            'android.permission.INTERNET',
            'com.android.vending.BILLING',
        ])

        parser.uses_features |should| equal_to([
            'android.hardware.touchscreen',
            'android.hardware.screen.landscape',
        ])
        parser.uses_implied_features |should| equal_to({
            'android.hardware.touchscreen': 'assumed you require a touch screen unless explicitly made optional',
            'android.hardware.screen.landscape': 'one or more activities have specified a landscape orientation',
            })

        parser.supports_screens |should| equal_to([
            'normal',
            'large',
            'xlarge',
            ])

        parser.densities |should| equal_to([
            120,
            160,
            240,
            320,
            480,
        ])
        parser.locales |should| equal_to([
            '--_--',
            'ca',
            'da',
            'fa',
            'ja',
            'nb',
            'be',
            'de',
            'he',
            'af',
            'bg',
            'th',
            'fi',
            'hi',
            'vi',
            'sk',
            'uk',
            'el',
            'nl',
            'pl',
            'sl',
            'tl',
            'am',
            'in',
            'ko',
            'ro',
            'ar',
            'fr',
            'hr',
            'sr',
            'tr',
            'cs',
            'es',
            'ms',
            'et',
            'it',
            'lt',
            'pt',
            'hu',
            'ru',
            'zu',
            'lv',
            'sv',
            'iw',
            'sw',
            'en_GB',
            'zh_CN',
            'pt_BR',
            'es_US',
            'pt_PT',
            'zh_TW'
        ])

        parser.native_code |should| equal_to('armeabi')

    def test_choose_icon_density(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, pkg_mutil_languages_profile_text())

        parser.package.get('package_name') |should| equal_to('com.limbic.ac130')
        parser.package.get('version_code') |should| equal_to(1379701800)
        parser.package.get('version_name') |should| equal_to('1.9.1')

        parser.sdk_version |should| equal_to(10)
        parser.target_sdk_version |should| equal_to(17)

    @skipIf(settings.AAPT_CMD is None, 'ignore fetch file without aapt')
    def test_fetch_file(self):
        self._tmpdir = join(self._fixture_dir, 'temp')
        os.makedirs(self._tmpdir, exist_ok=True)

        parser = PackageFileParser(self._pkgfile)
        if not settings.AAPT_CMD:
            self._mock_badging_text(parser, self._pkg2_profile_text())
        resource_filename = parser.application_icons['160']
        filename = parser.fetch_file(resource_filename=resource_filename,
                                      to_path=self._tmpdir)

        os.path.isfile(filename) |should| be(True)

        shutil.rmtree(self._tmpdir, ignore_errors=True)

    @skipIf(settings.AAPT_CMD is None, 'ignore fetch file without aapt')
    def test_fetch_file_reduplicative(self):
        self._tmpdir = join(self._fixture_dir, 'temp')
        os.makedirs(self._tmpdir, exist_ok=True)

        parser = PackageFileParser(self._pkgfile)
        if not settings.AAPT_CMD:
            self._mock_badging_text(parser, self._pkg2_profile_text())
        resource_filename = parser.application_icons['160']

        # first
        filename = parser.fetch_file(resource_filename=resource_filename,
                                     to_path=self._tmpdir)

        # second
        filename = parser.fetch_file(resource_filename=resource_filename,
                                     to_path=self._tmpdir)

        # unzip popup to confirm next action when file duplication
        # it wait to user interactive
        os.path.isfile(filename) |should| be(True)

        shutil.rmtree(self._tmpdir, ignore_errors=True)


