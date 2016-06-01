# -*- coding: utf-8 -*-
from django.core.files import File
from django.test import TestCase
from django.utils.timezone import now
import shutil
import io
import os
from os.path import join, abspath, dirname
from django.test.utils import override_settings
from should_dsl import should
from account.models import User as Player

__author__ = 'me'
_fixture_dir = join(dirname(abspath(__file__)), 'fixtures')

class AccountUnitTest(TestCase):

    _fixture_dir = _fixture_dir
    _files_to_remove = []

    def setUp(self):
        _dir = join(self._fixture_dir, 'temp')
        os.makedirs(_dir, exist_ok=True)
        self._files_to_remove.append(_dir)

    def tearDown(self):
        for f in self._files_to_remove:
            shutil.rmtree(f, ignore_errors=True)

    @override_settings(MEDIA_ROOT=join(_fixture_dir, 'temp'))
    def test_upload_file_to_path(self):

        user = Player.objects.create_user(username="robert",
                                          phone="+86-021-123321123",
                                          email="robert@testcase.com",
                                          password="123456")
        icon = io.FileIO(join(self._fixture_dir, 'user-icon.png'))
        user.profile.icon = File(icon)
        cover = io.FileIO(join(self._fixture_dir, 'user-cover.jpg'))
        user.profile.cover = File(cover)
        user.profile.save()

        path_pattern = 'userprofile/%(date)s/%(user_id)d' % {
            'date': now().strftime('%Y%m%d'),
            'user_id': user.pk,
        }
        user.profile.icon.path |should| end_with(join(path_pattern, 'icon.png'))
        user.profile.cover.path |should| end_with(join(path_pattern, 'cover.jpg'))
