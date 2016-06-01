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
        """
        等级 经验
        Lv0   0
        Lv1   50
        Lv2   80
        Lv3   200
        Lv4   450
        从3级开始，经验值的计算公式为
        (等级-1)*(等级-1)*50
        """
        # level 0
        self.user.profile.change_experience(0)
        self.user.profile.level |should| equal_to(0)

        self.user.profile.change_experience(10)
        self.user.profile.level |should| equal_to(0)

        self.user.profile.change_experience(50-1)
        self.user.profile.level |should| equal_to(0)

        # level 1
        self.user.profile.change_experience(50)
        self.user.profile.level |should| equal_to(1)

        self.user.profile.change_experience(60)
        self.user.profile.level |should| equal_to(1)

        self.user.profile.change_experience(80-1)
        self.user.profile.level |should| equal_to(1)

        # level 2
        self.user.profile.change_experience(80)
        self.user.profile.level |should| equal_to(2)

        self.user.profile.change_experience(100)
        self.user.profile.level |should| equal_to(2)

        self.user.profile.change_experience(200-1)
        self.user.profile.level |should| equal_to(2)

        # level 3
        self.user.profile.change_experience(200)
        self.user.profile.level |should| equal_to(3)

        self.user.profile.change_experience(280)
        self.user.profile.level |should| equal_to(3)

        self.user.profile.change_experience(450-1)
        self.user.profile.level |should| equal_to(3)

        # level 4
        self.user.profile.change_experience(450)
        self.user.profile.level |should| equal_to(4)


        self.user.profile.change_experience(800-1)
        self.user.profile.level |should| equal_to(4)

        # level 5
        self.user.profile.change_experience(800)
        self.user.profile.level |should| equal_to(5)

        self.user.profile.change_experience(820)
        self.user.profile.level |should| equal_to(5)


