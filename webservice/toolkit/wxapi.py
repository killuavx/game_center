# -*- coding: utf-8 -*-
from kombu import uuid
import requests
from urllib.parse import *
from toolkit.cache_tagging_mixin import cache


class WXApiException(Exception):

    def __init__(self, code=None, message='', *args, **kwargs):
        self.code = code
        self.message = message
        super(WXApiException, self).__init__(*args, **kwargs)


class WXApi(object):

    _cache = cache

    APP_ID = 'wx2ef930101f70a52e'

    APP_SECRET = '2c3a8ae702896bf4065ad672e5dfbe00'

    ACCOUNT = "377278127@qq.com"

    PASSWORD = "sf12345678"

    def __init__(self, redirect_uri=None):
        #self.redirect_uri = redirect_uri
        self.redirect_uri = None
        if not redirect_uri:
            self.redirect_uri = redirect_uri

    API_QRCONNECT = 'https://open.weixin.qq.com/connect/qrconnect'

    def qrconnect_redirect_url(self, state_key, redirect_uri=None):
        if not redirect_uri:
            redirect_uri = self.redirect_uri

        data = dict(
            appid=self.APP_ID,
            response_type="code",
            state=uuid(),
            scope='snsapi_login',
            redirect_uri=redirect_uri,
        )
        self.set_qrconnect_state(state_key, data['state'])
        query = urlencode(data)
        login_url = "%s?%s" %(self.API_QRCONNECT, query)
        return login_url

    def set_qrconnect_state(self, key, state):
        self._cache.set("wx_snsapi_login_%s" % key, state)

    def get_qrconnect_state(self, key):
        return self._cache.get("wx_snsapi_login_%s" % key)

    def check_qrconnect_state(self, key, state):
        if self.get_qrconnect_state(key) == state:
            return True
        return False

    API_ACCESS_TOKEN = 'https://api.weixin.qq.com/sns/oauth2/access_token'

    def request_access_token(self, code=None):
        data = dict(
            appid=self.APP_ID,
            secret=self.APP_SECRET,
            grant_type='authorization_code',
            code=code,
        )
        api_url = self.API_ACCESS_TOKEN
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise WXApiException(code=response.status_code, message=response.text)

    API_REFRESH_TOKEN = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'

    def refresh_token(self, refresh_token):
        api_url = self.API_REFRESH_TOKEN
        data = dict(
            appid=self.APP_ID,
            grant_type='refresh_token',
            refresh_token=refresh_token,
            )
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise WXApiException(code=response.status_code, message=response.text)

    API_AUTH = 'https://api.weixin.qq.com/sns/auth'

    def auth(self, access_token, openid):
        data = dict(
            access_token=access_token,
            openid=openid,
        )
        api_url = self.API_AUTH
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise WXApiException(code=response.status_code, message=response.text)

    API_USERINFO = 'https://api.weixin.qq.com/sns/userinfo'

    def userinfo(self, access_token, openid):
        data = dict(
            access_token=access_token,
            openid=openid,
        )
        api_url = self.API_USERINFO
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise WXApiException(code=response.status_code, message=response.text)


import io
from account.models import Profile
from django.core.files.images import ImageFile

WX_HEADIMG_SIZE = 132


def userinfo_transaction_profile(user, userinfo):
    headimgurl = userinfo['headimgurl']
    if headimgurl:
        res = requests.get("%s%s" %(headimgurl.rstrip('0'), WX_HEADIMG_SIZE))
        if res.status_code == 200:
            try:
                user.profile.icon = ImageFile(io.BytesIO(res.content),
                                              name='wxface.jpg')
                user.profile.save(update_fields=['mugshot'])
            except:
                user.profile.icon = None

    sex = userinfo['sex']
    if sex:
        user.profile.sex = [None, Profile.SEX.male, Profile.SEX.female][sex]

    changed_fields = []
    for field, val in user.profile.tracker.changed().items():
        changed_fields.append(field)

    if changed_fields:
        user.profile.save(update_fields=changed_fields)

    return user.profile
