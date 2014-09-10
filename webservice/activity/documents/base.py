# -*- coding: utf-8 -*-
from account.models import User
from mongoengine import fields


class Ownerable(object):

    user_id = fields.IntField()

    @property
    def user(self):
        if not hasattr(self, '_user'):
            try:
                self._user = User.objects.get(pk=self.user_id)
            except:
                self._user = None
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        self.user_id = user.pk
