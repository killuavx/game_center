# -*- coding: utf-8 -*-
import os
from os.path import abspath, dirname, join
import shutil
from django.test.testcases import TestCase, skipIf

from django.conf import settings
from warehouse.utils.parser import *
from mock import MagicMock
from should_dsl import should
__author__ = 'me'

_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')

class PackageFileParserUnitTest(TestCase):

    _fixture_dir = _fixture_dir

    def setUp(self):
        AAPT_CMD=settings.AAPT_CMD
        set_package_parser_exe(AAPT_CMD)
        self._pkgfile = join(self._fixture_dir, 'tinysize.apk')

    def _mock_badging_text(self, parser, return_value):
        parser.badging_text = MagicMock(return_value=return_value)

    def _pkg_profile_text(self):
        return_value ="""package: name='solitairelite.solitaire' versionCode='4' versionName='1.3'
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
        return return_value

    def test_base_parser(self):
        parser = PackageFileParser(self._pkgfile)
        if not settings.AAPT_CMD:
            self._mock_badging_text(parser, self._pkg_profile_text())
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

    def _pkg2_profile_text(self):
        return_value = """package: name='com.eamobile.bejeweled2_na_wf' versionCode='2007700' versionName='2.0.10'
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
        return return_value

    def test_complex_parse(self):
        parser = PackageFileParser(self._pkgfile)
        self._mock_badging_text(parser, self._pkg2_profile_text())

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

