# -*- coding: utf-8 -*-
from django.test import TestCase
from should_dsl import should
from account.models import User


from mongoengine import register_connection
from django.conf import settings
con_key = 'data_center'
con_opts = settings.MOGOENGINE_CONNECTS[con_key]
register_connection(alias=con_key,
                    name=con_opts.get('name'),
                    host=con_opts.get('host'),
                    port=con_opts.get('port'))

import logging
logger = logging.getLogger('console')

class ExchangeLevelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.get(username='admin')

    def tearDown(self):
        self.user.profile.experience = 0

    def test_change_experience(self):
        self.user.profile.change_experience(10)
        self.user.profile.level |should| equal_to(1)

        self.user.profile.change_experience(50)
        self.user.profile.level |should| equal_to(1)

        self.user.profile.change_experience(80)
        self.user.profile.level |should| equal_to(2)

        self.user.profile.change_experience(200)
        self.user.profile.level |should| equal_to(3)

        self.user.profile.change_experience(210)
        self.user.profile.level |should| equal_to(3)

        self.user.profile.change_experience(440)
        self.user.profile.level |should| equal_to(3)

        self.user.profile.change_experience(450)
        self.user.profile.level |should| equal_to(4)

        self.user.profile.change_experience(800)
        self.user.profile.level |should| equal_to(5)

        self.user.profile.change_experience(1250)
        self.user.profile.level |should| equal_to(6)

        self.user.profile.change_experience(1800)
        self.user.profile.level |should| equal_to(7)

        self.user.profile.change_experience(1900)
        self.user.profile.level |should| equal_to(7)

        self.user.profile.change_experience(2450)
        self.user.profile.level |should| equal_to(8)

        self.user.profile.change_experience(2451)
        self.user.profile.level |should| equal_to(8)
