# -*- coding: utf-8 -*-
__author__ = 'me'
from fts.helpers import ApiDSL
from fts.tests import helpers
from django.test.testcases import TestCase

class UserBookmarkUnitTest(TestCase):


    def test_user_bookmarks(self):
        user = helpers.create_account()
        self.assertEqual(0, user.profile.bookmarks.count())

        pkg = ApiDSL.Given_i_have_published_package(self, title='植物大战僵尸')
        user.profile.bookmarks.add(pkg)

        self.assertEqual(1, user.profile.bookmarks.count())

        except_pkg = user.profile.bookmarks.all()[0]
        self.assertEqual(pkg, except_pkg)

        user.profile.bookmarks.remove(except_pkg)
        self.assertEqual(0, user.profile.bookmarks.count())


