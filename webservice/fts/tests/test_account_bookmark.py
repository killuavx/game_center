# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from fts.features.app_dsls import account, warehouse


class AccountBaseUnitTest(TestCase):

    tags = []

    world = {}

    def setUp(self):
        super(AccountBaseUnitTest, self).setUp()
        self.WarehouseDSL = warehouse.factory_dsl(self)
        self.WarehouseDSL.setup(self)
        self.AccountDSL = account.factory_dsl(self)
        self.AccountDSL.setup(self)

    def tearDown(self):
        self.WarehouseDSL.teardown(self)
        self.AccountDSL.teardown(self)
        super(AccountBaseUnitTest, self).tearDown()

    def create_package(self, with_version=False, **kwargs):
        return self.WarehouseDSL.create_package_without_ui(
            self,
            with_version=with_version,
            **kwargs)

    def create_account(self, username):
        return self.AccountDSL \
            .already_exists_player_create(context=self,
                                          username=username)

    def account_signin(self, user):
        self.AccountDSL.signin(context=user,
                               username=user.username,
                               password=self.AccountDSL._PASSWORD)

