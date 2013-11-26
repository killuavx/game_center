# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from fts.features.app_dsls import warehouse
from fts.features.app_dsls import account


class UserBookmarkUnitTest(TestCase):

    world = {}
    tags = []

    def setUp(self):
        warehouse.setup(self)
        account.setup(self)
        self.WarehouseDSL = warehouse.factory_dsl(self)
        self.AccountDSL = account.factory_dsl(self)

    def tearDown(self):
        warehouse.teardown(self)
        account.teardown(self)

    def test_user_bookmarks(self):
        user = self.AccountDSL.already_exists_player_create(self,
                                                            username="kent")
        self.assertEqual(0, user.profile.bookmarks.count())

        pkg = self.WarehouseDSL.create_package_without_ui(
            self,
            title='植物大战僵尸')
        user.profile.bookmarks.add(pkg)

        self.assertEqual(1, user.profile.bookmarks.count())

        except_pkg = user.profile.bookmarks.all()[0]
        self.assertEqual(pkg, except_pkg)

        user.profile.bookmarks.remove(except_pkg)
        self.assertEqual(0, user.profile.bookmarks.count())


