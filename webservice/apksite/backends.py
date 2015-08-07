# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from apksite.apis import ApiFactory, ApiResponseException
from apksite.models import User
from toolkit.helpers import current_request

SESSION_KEY_USER_PROFILE = '_auth_user_profile'


class RemoteApiUserBackend(object):

    def authenticate(self, username, password, app=None, **kwargs):

        api = ApiFactory.factory('user.login')
        response = api.request(username=username, password=password, app=app)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            raise PermissionDenied(e.msg)

        currequest = current_request()
        currequest.session[SESSION_KEY_USER_PROFILE] = result
        user = self.wrapup_user(result)
        return user

    def get_user(self, id, update_session=False):
        currequest = current_request()
        if update_session:
            profile_data = self._request_profile_data(id)
            currequest.session[SESSION_KEY_USER_PROFILE] = profile_data
        else:
            profile_data = currequest.session.get(SESSION_KEY_USER_PROFILE)

        if profile_data:
            return self.wrapup_user(profile_data)
        else:
            return None

    def _request_profile_data(self, id):
        api = ApiFactory.factory('user.getProfile')
        response = api.request(user_id=id)
        try:
            result = api.get_response_data(response=response, name=api.name)
        except ApiResponseException as e:
            result = None
        return result

    def wrapup_user(self, result):
        user = User(**dict(
            id=result.get('id'),
            username=result.get('username')
        ))
        user.profile = result
        return user

