# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from apksite.apis import ApiFactory, ApiResponseException
from apksite.models import User


class RemoteApiUserBackend(object):

    def authenticate(self, username, password, app=None, **kwargs):
        api = ApiFactory.factory('user.login')
        response = api.request(username=username, password=password, app=app)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            raise PermissionDenied(e.msg)

        return self.wrapup_user(result)

    def get_user(self, id):
        api = ApiFactory.factory('user.getProfile')
        response = api.request(user_id=id)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            return None
        return self.wrapup_user(result)

    def wrapup_user(self, result):
        user = User(**dict(
            id=result.get('id'),
            username=result.get('username')
        ))
        user.profile = result
        return user

