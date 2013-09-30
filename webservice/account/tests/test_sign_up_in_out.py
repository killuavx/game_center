# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.utils import override_settings
from account.models import Player, Profile
from account.backends import GameCenterAuthenticationBackend

class SimpleAccountUnitTest(TestCase):

    def test_basic_signup(self):
        user = Player(username='killuavx')
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.set_password('123456')
        user.save()

        self.assertEqual(user.check_password('123456'), True)

        Profile.objects.create(user=user, email='t1@testcase.com',
                                           phone='+86-021-67890546')
        self.assertEqual('t1@testcase.com', user.profile.email)

    def test_authenticate(self):
        user = Player(username='killuavx')
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.set_password('123456')
        user.save()

        email = 't1@testcase.com'
        phone = '+86-021-67890546'
        Profile.objects.create(user=user, email=email,
                               phone=phone)

        backend = GameCenterAuthenticationBackend()
        except_user = backend.authenticate(username=user.username, password='123456')
        self.assertEqual(except_user, user)

        except_user = backend.authenticate(username=phone, password='123456')
        self.assertEqual(except_user, user)

        except_user = backend.authenticate(username=email, password='123456')
        self.assertEqual(except_user, user)

        except_user = backend.authenticate(username='123', password='123456')
        self.assertIsNone(except_user)
