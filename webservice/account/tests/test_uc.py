# -*- coding: utf-8 -*-
from django.test import TestCase
from account.uc_client.client import ClientApi
from should_dsl import should

class TestUC(TestCase):

    def setUp(self):
        self.api = ClientApi()

    def test_uc_get_user(self):
        result = self.api.uc_get_user(user_name='admin')
        result[0] |should| equal_to("1")
        result[1] |should| equal_to("admin")
        result[2] |should| equal_to("admin@admin.com")
