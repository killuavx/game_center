# -*- coding: utf-8 -*-
from django.test.testcases import TransactionTestCase


class WebMobHomepageTestCase(TransactionTestCase):


    def test_package_list(self):
        response = self.client.get('/mob/home/')



