# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from account.models import Profile
from account.models import UserAppBind
import hashlib
from account.utils import get_datetime_now, PROFILE_EMAIL_DEFAULT_HOST
from django.db import transaction
from toolkit.wxapi import WXApi, WXApiException, userinfo_transaction_profile

sha_constructor = hashlib.sha1

import logging
logger = logging.getLogger('scripts')


class GetUserMixin(object):

    def get_user(self, user_id):
        from account.models import User as Player
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None


def unique_value(queryset, field, value, segment='-'):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
        try:
            queryset.get(**{field: value})
        except ObjectDoesNotExist:
            break
        i += 1
    return value


def unique_email_value(queryset, field, email, segment='_'):
    i = 0
    value, host = email.split('@')
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
            email = "%s@%s" %(value, host)
        try:
            queryset.get(**{field: email})
        except ObjectDoesNotExist:
            break
        i += 1
    return email


def uc_unique_username(api, value, segment='-'):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
        code = int(api.uc_user_checkname(username=value))
        if code == 1:
            break
        i += 1
    return value


def uc_unique_email(api, email, segment='-'):
    i = 0
    value, host = email.split('@')
    while True:
        if i > 0:
            if i > 1:
                value = value.rsplit(segment, 1)[0]
            value = "%s%s%s" % (value, segment, i)
        email = "%s@%s" %(value, host)
        code = int(api.uc_user_checkemail(email=email))
        if code == 1:
            break
        i += 1
    return email


class UserSyncAPI(object):

    @classmethod
    def get_uc_api(cls):
        if not hasattr(cls, '_uc_client_api'):
            from account.uc_client.client import ClientApi
            cls._uc_client_api = ClientApi()
        return cls._uc_client_api

    def sync_user_to_ucenter(self, user, **kwargs):
        try:
            appbind = user.appbinds.filter(app=UserAppBind.APPS.bbs).get()
            return user
        except UserAppBind.DoesNotExist:
            api = self.get_uc_api()
            uid = api.uc_user_register(username=self.clean_ucenter_username(user.username),
                                       email=self.clean_ucenter_email(user.profile.email),
                                       password=kwargs.get('password'),
                                       )
            uid = int(uid)
            bind = UserAppBind.objects.create(user=user,
                                              app=UserAppBind.APPS.bbs,
                                              uid=uid)
            return user

    def clean_ucenter_username(self, username):
        return uc_unique_username(self.get_uc_api(), username)

    def clean_ucenter_email(self, email):
        return uc_unique_email(self.get_uc_api(), email)

    def sync_user_from_ucenter(self, uc_userdata):
        uc_uid = int(uc_userdata[0])
        username = uc_userdata[1]
        password = uc_userdata[2]
        email = uc_userdata[3]

        User = get_user_model()
        try:
            user = User.objects.get_by_appbind(UserAppBind.APPS.bbs, uc_uid)
            return user
        except User.DoesNotExist:
            email = self.clean_email(email)
            username = self.clean_username(username)
            phone = self.clean_phone()

            sid = transaction.savepoint()
            try:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                phone=phone,
                                                password=password)
                UserAppBind.objects.create(user=user,
                                           app=UserAppBind.APPS.bbs,
                                           uid=uc_uid)
                transaction.savepoint_commit(sid)
                return user
            except:
                transaction.savepoint_rollback(sid)
                return None

    def clean_username(self, username):
        User = get_user_model()
        qs = User.objects.all()
        return unique_value(qs, 'username', username)

    def clean_email(self, email):
        qs = Profile.objects.all()
        return unique_email_value(qs, 'email', email)

    def _phone(self):
        now = get_datetime_now()
        return now.strftime('%Y%m%d%H%M%S%f')

    def clean_phone(self):
        phone = self._phone()
        qs = Profile.objects.all()
        return unique_value(qs, 'phone', phone)

    def checkupdate_wx_user_bind(self, openid, extra_data=None):
        appbind = UserAppBind.objects.get(app=UserAppBind.APPS.wx, openid=openid)
        print(extra_data)
        if extra_data:
            appbind.extra_data = extra_data
            if appbind.tracker.has_changed('extra_text'):
                appbind.save()
        return appbind.user

    def create_wx_user_bind(self, openid, userinfo, extra_data):
        username = userinfo['openid'].lower()[0:5] + userinfo['unionid'][0:5].lower()
        username = self.clean_username(username)
        email = "%s@%s" %(username, PROFILE_EMAIL_DEFAULT_HOST)
        email = self.clean_email(email)
        phone = self.clean_phone()
        User = get_user_model()
        user = User.objects.create_user(username=username,
                                        email=email,
                                        phone=phone)
        group_player, _is_new = Group.objects.get_or_create(name='weixin')
        user.groups.add(group_player)
        bind = UserAppBind.objects.create(user=user,
                                          app=UserAppBind.APPS.wx,
                                          openid=openid,
                                          extra_data=extra_data,
                                          )
        userinfo_transaction_profile(user, userinfo)
        return user


class GameCenterModelBackend(UserSyncAPI,
                             GetUserMixin,
                             ModelBackend):
    """
        game center 用户登录验证
    """

    def authenticate(self, username=None, password=None,
                     check_password=True, app=None, **kwargs):
        """
            username: game center账号
            password: game center密码
            app如设置了，表示使用别的登陆方式，略过当前登陆方式
        """
        if app:
            return None
        User = get_user_model()
        try:
            filters = {"%s__iexact" % User.USERNAME_FIELD: username}
            user = User.objects.get(**filters)
        except (User.DoesNotExist, ValueError):
            return None

        if not user.is_active:
            return None

        if not check_password:
            self.sync_user(user, password=password)
            return user

        if user.check_password(password):
            self.sync_user(user, password=password)
            return user
        return None

    def sync_user(self, user, **kwargs):
        try:
            return self.sync_user_to_ucenter(user, **kwargs)
        except:
            return user


class UCenterModelBackend(UserSyncAPI,
                          GetUserMixin,
                          ModelBackend):
    """
        ucenter 用户登录验证
    """

    def authenticate(self, username=None, password=None, app=None, **kwargs):
        """
            username: game center账号
            password: game center密码
            app如设置了，表示使用UCenter登陆方式，否则路过本次验证
        """
        if not app:
            return None

        from account.uc_client.client import UcenterApiNotFound
        try:
            result = self.get_uc_api()\
                .uc_user_login(username=username, password=password)
        except UcenterApiNotFound:
            return None

        code = int(result[0])
        if code < 0:
            return None
        user = self.sync_user(result)
        return user

    def sync_user(self, uc_userdata):
        try:
            user = self.sync_user_from_ucenter(uc_userdata)
            if user and user.is_active:
                return user
        except:
            pass
        return None


class GameCenterProfileBackend(GetUserMixin):

    def authenticate(self, username=None, password=None, app=None, **kwargs):
        """
            username: game center profile 电话号码/电子邮箱
            password: game center密码
            app如设置了，表示使用别的登陆方式，略过当前登陆方式
        """
        if app is not None:
            return None
        try:
            user = Profile.objects.get(phone__iexact=username).user
        except (ObjectDoesNotExist, ValueError):
            try:
                user = Profile.objects.get(email__iexact=username).user
            except (ObjectDoesNotExist, ValueError):
                return None

        if not user.is_active:
            return None

        if user.check_password(password):
            return user
        return None


class WXBackend(UserSyncAPI, GetUserMixin):

    SUCCESS = 0

    wxapi = WXApi()

    ACTIONS = ('wx_access', 'wx_refresh')

    def oauth_by_refresh_token(self, refresh_token):
        result = self.wxapi.refresh_token(refresh_token=refresh_token)
        if result.get('errcode', self.SUCCESS) == self.SUCCESS:
            access_token, openid = result['access_token'], result['openid']
            return access_token, openid, result
        else:
            return None

    def oauth_by_access_token(self, access_token):
        result = self.wxapi.request_access_token(code=access_token)
        openid = result['openid'] if result.get('errcode', self.SUCCESS) == self.SUCCESS else None
        if openid:
            return access_token, openid, result
        else:
            return None

    def authenticate_by(self, access_token, openid, refresh_token):
        try:
            if openid:
                try:
                    return self.checkupdate_wx_user_bind(openid=openid)
                except UserAppBind.DoesNotExist:
                    return None

            result = None
            if access_token:
                result = self.oauth_by_access_token(access_token)
            elif refresh_token:
                result = self.oauth_by_refresh_token(refresh_token)

            if not result:
                return None

            access_token, openid, extra_data = result
            return self.sync_user(openid=openid, access_token=access_token, extra_data=extra_data)

        except WXApiException as e:
            print(e)
            return None

    def authenticate(self, username=None, password=None, app=None, **kwargs):
        access_token = refresh_token = openid = None
        if app == 'wx_access':
            access_token, openid = password, username
        elif app == 'wx_refresh':
            refresh_token, openid = password, username
        else:
            return None

        return self.authenticate_by(access_token=access_token,
                                 refresh_token=refresh_token,
                                 openid=openid)

    def sync_user(self, openid, access_token, extra_data):
        try:
            return self.checkupdate_wx_user_bind(openid=openid, extra_data=extra_data)
        except UserAppBind.DoesNotExist:
            userinfo = self.wxapi.userinfo(access_token=access_token, openid=openid)
            if userinfo.get('errcode', self.SUCCESS) == self.SUCCESS:
                return self.create_wx_user_bind(openid=openid, userinfo=userinfo, extra_data=extra_data)
        return None

