# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class GameCenterModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, check_password=True, **kwargs):
        User = get_user_model()
        try:
            filters = {"%s__iexact" % User.USERNAME_FIELD: username}
            user = User.objects.get(**filters)
        except User.DoesNotExist:
            return None

        if not check_password:
            return user

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        from account.models import User as Player
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None



