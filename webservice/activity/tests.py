# -*- coding: utf-8 -*-
from django.test import TestCase

class WarehouseDSL(object):
    pass


class ActivityDSL(object):

    def giftbag_already_exists_for(self, package, version=None,
                                   published_datetime=None,
                                   expire_datetime=None,
                                   ):
        pass

    def gitbag_already_has_many_gitcard(self, gitbag, card_code):
        pass


class GitBagTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
