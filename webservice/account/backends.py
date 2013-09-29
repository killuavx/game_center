# -*- coding: utf-8 -*-
from account.models import Player, Profile

class GameCenterAuthenticationBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Player.USERNAME_FIELD)

        user = None
        try:
            user = Player._default_manager.get_by_natural_key(username)
        except Player.DoesNotExist:
            # counting
            pass

        try:
            user = Player.objects.by_profile_with(email=username).get()
        except (Player.DoesNotExist, Profile.DoesNotExist ) as e:
            # counting
            pass

        try:
            user = Player.objects.by_profile_with(phone=username).get()
        except (Player.DoesNotExist, Profile.DoesNotExist) as e:
            # counting
            pass

        if user is not None and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None
