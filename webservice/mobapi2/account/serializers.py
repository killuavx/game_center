# -*- coding: utf-8 -*-
from copy import deepcopy
from django.core.exceptions import ValidationError
from django.db  import models
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.core import validators

from account import authenticate
from account.utils import *
from comment.models import Comment
from account.models import User as Player, Profile
from account.utils import PROFILE_EMAIL_DEFAULT_HOST, generate_random_email
from mobapi2.serializers import ModelSerializer


class AccountRelatedProfileMixin(object):
    def get_profile_icon_url(self, obj):
        try:
            return obj.profile.icon.url
        except:
            pass
        return None

    def get_profile_email(self, obj):
        email = ''
        try:
            email = obj.profile.email
        except:
            pass
        if email.endswith('uc.ccplay.com.cn'):
            return None
        return None

    def get_profile_phone(self, obj):
        try:
            return obj.profile.phone
        except:
            pass
        return None

    def get_comment_count(self, obj):
        try:
            return Comment.objects.visible().filter(user=obj).count()
        except:
            return 0

    def get_profile_bookmark_count(self, obj):
        try:
            return obj.profile.bookmarks.published().count()
        except:
            pass
        return 0


class AccountDetailSerializer(AccountRelatedProfileMixin, ModelSerializer):

    email = serializers.SerializerMethodField('get_profile_email')
    phone = serializers.SerializerMethodField('get_profile_phone')
    icon = serializers.SerializerMethodField('get_profile_icon_url')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    bookmark_count = serializers \
        .SerializerMethodField('get_profile_bookmark_count')

    class Meta:
        model = Player
        fields = (
            'username',
            'icon',
            'comment_count',
            'bookmark_count',
        )


class MultiAppAuthTokenSerializer(AuthTokenSerializer):

    username = serializers.CharField()
    password = serializers.CharField()

    app = serializers.CharField(default=None, required=False)

    def validate(self, attrs):
        app = attrs.get('app')
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password, app=app)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('用户账号被禁用')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('账号或密码错误')
        else:
            raise serializers.ValidationError('请提供登陆名和密码')


# new profile

class EmailNotSetField(serializers.EmailField):

    default_email_host = PROFILE_EMAIL_DEFAULT_HOST

    default_error_messages = {
        'required': '请填写电子邮件',
        'blank': '请填写电子邮件',
        'invalid': '电子邮箱不正确',
    }

    default = generate_random_email

    def __init__(self, *args, **kwargs):
        if 'required' not in kwargs:
            kwargs['required'] = False

        if 'blank' not in kwargs:
            kwargs['blank'] = True
        super(EmailNotSetField, self).__init__(*args, **kwargs)

    def from_native(self, value):
        val = super(EmailNotSetField, self).from_native(value)
        if val and val.endswith(self.default_email_host):
            return None
        return val

    def to_native(self, value):
        if value and value.endswith(self.default_email_host):
            return None
        return value


class ProfileStatsSerializerMixin(object):

    def get_token_key(self, obj):
        if obj:
            token, created = Token.objects.get_or_create(user=obj.user)
            return token.key
        return None

    def get_comment_count(self, obj):
        try:
            return Comment.objects.visible().filter(user=obj.user).count()
        except:
            return 0

    def get_bookmark_count(self, obj):
        try:
            return obj.bookmarks.published().count()
        except:
            pass
        return 0

    def get_giftbag_count(self, obj):
        user = obj.user
        return user.giftcard_set.count()


from account.validators import validate_phone


class PhoneField(serializers.CharField):

    default_validators = [
        validate_phone,
    ]
    description = "Phone"
    default_error_messages = {
        'invalid': '请填写有效手机号码'
    }

    default = lambda x: get_datetime_now().strftime('%Y%m%d%H%M%S%f')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 16)
        kwargs['min_length'] = kwargs.get('min_length', 11)
        super(PhoneField, self).__init__(*args, **kwargs)


import re


class PhoneNotSetField(PhoneField):

    datetime_re = re.compile(r"^(201[3-9])((0[1-9])|1[0-2])([0-3][0-9])")

    def __init__(self, *args, **kwargs):
        if 'required' not in kwargs:
            kwargs['required'] = False
        super(PhoneNotSetField, self).__init__(*args, **kwargs)

    #def from_native(self, value):
    #    val = super(PhoneNotSetField, self).from_native(value)
    #    if val and self.datetime_re.search(val):
    #        return None
    #    return val

    def to_native(self, val):
        if val and self.datetime_re.search(val):
            return None
        return val


PROFILE_BASIC_FIELDS = ('username', 'icon', 'phone', 'email', 'sex', 'birthday')


_account_serializer_field_mapping = deepcopy(ModelSerializer.field_mapping)
_account_serializer_field_mapping.update({
    models.EmailField: EmailNotSetField,
})

profile_username = serializers.SlugRelatedField(source='user',
                                                slug_field='username',
                                                error_messages={'invalid': '用户名格式不正确'},
                                                read_only=True,
                                                )


class ProfileIconField(serializers.ImageField):

    def to_native(self, value):
        if value:
            url = value.url
            # FIXME 暂时不做cdn同步，使用其他主站服务器的域名访问用户头像
            return url.replace('media.', 'gc.', 1)
        return None


profile_icon = ProfileIconField(source='icon', error_messages={
    'invalid': '图片无效',
    'invalid_image': '图片无效',
    'required': '请提供图片',
})


class AccountProfileSerializer(ModelSerializer):

    field_mapping = _account_serializer_field_mapping

    username = profile_username

    icon = profile_icon

    phone = PhoneNotSetField(required=False, read_only=True)

    class Meta:
        model = Profile
        fields = PROFILE_BASIC_FIELDS

    def save_object(self, obj, **kwargs):
        if not obj.tracker.changed():
            return
        super(AccountProfileSerializer, self).save_object(obj, **kwargs)


class AccountProfileStatsSerializer(ProfileStatsSerializerMixin,
                                    AccountProfileSerializer):

    icon = profile_icon

    username = profile_username

    comment_count = serializers.SerializerMethodField('get_comment_count')

    bookmark_count = serializers \
        .SerializerMethodField('get_bookmark_count')

    giftbag_count = serializers \
        .SerializerMethodField('get_giftbag_count')

    class Meta:
        model = Profile
        fields = PROFILE_BASIC_FIELDS + (
            'comment_count',
            'bookmark_count',
            'giftbag_count',
            'level',
            'coin',
            'experience'
        )


class AccountProfileSigninSerializer(AccountProfileStatsSerializer):

    icon = profile_icon

    username = profile_username

    token = serializers.SerializerMethodField('get_token_key')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    bookmark_count = serializers \
        .SerializerMethodField('get_bookmark_count')

    giftbag_count = serializers \
        .SerializerMethodField('get_giftbag_count')

    class Meta:
        model = Profile
        fields = PROFILE_BASIC_FIELDS + (
            'comment_count',
            'bookmark_count',
            'giftbag_count',
            'level',
            'coin',
            'experience',
            'token'
        )


class AccountProfileSignupSerizlizer(AccountProfileStatsSerializer):

    icon = profile_icon

    username = profile_username

    token = serializers.SerializerMethodField('get_token_key')

    comment_count = serializers.SerializerMethodField('get_comment_count')

    def get_comment_count(self, obj):
        return 0

    bookmark_count = serializers.SerializerMethodField('get_bookmark_count')

    def get_bookmark_count(self, obj):
        return 0

    giftbag_count = serializers.SerializerMethodField('get_giftbag_count')
    def get_giftbag_count(self, obj):
        return 0


    class Meta:
        model = Profile
        fields = PROFILE_BASIC_FIELDS + (
            'comment_count',
            'bookmark_count',
            'giftbag_count',
            'level',
            'coin',
            'experience',
            'token'
        )


from account.models import UserAppBind
from account.backends import WXBackend


class WeixinAuthTokenSerializer(serializers.Serializer):

    access_token = serializers.CharField(required=False)

    refresh_token = serializers.CharField(required=False)

    openid = serializers.CharField(required=False)

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        openid = attrs.get('openid')
        refresh_token = attrs.get('refresh_token')
        backend = WXBackend()
        if access_token or openid or refresh_token:
            attrs['users'] = user = backend.authenticate_by(access_token=access_token,
                                                            refresh_token=refresh_token,
                                                            openid=openid)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('用户账号被禁用')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('授权登陆失败')
        else:
            raise serializers.ValidationError('请提供有效的授信数据(access_token/openid/refresh_token)')


class WeixinAccountProfileSerializer(AccountProfileStatsSerializer):

    icon = profile_icon

    username = profile_username

    token = serializers.SerializerMethodField('get_token_key')

    extra = serializers.SerializerMethodField('get_extra')

    def get_extra(self, obj):
        user = obj.user
        try:
            bind = user.appbinds.filter(app=UserAppBind.APPS.wx).get()
        except UserAppBind.DoesNotExist:
            return None
        return bind.extra_data

    class Meta:
        model = Profile
        fields = PROFILE_BASIC_FIELDS + (
            'comment_count',
            'bookmark_count',
            'giftbag_count',
            'level',
            'coin',
            'experience',
            'token',
            'extra',
        )


from toolkit.CCPSDK.helpers import PhoneAuth, ChangePhoneAuth
from toolkit.CCPSDK.helpers import send_sms, SMS_TEMPID_SIGNUP
from account.forms.mob import validate_phone_unique

PHONE_AUTH_DURATION = 60 * 5


class PhoneAuthSerializer(serializers.Serializer):

    phone = PhoneField(required=True)

    code = serializers.SerializerMethodField('get_random_code')

    DURATION = PHONE_AUTH_DURATION

    duration = serializers.IntegerField(default=DURATION)

    def get_random_code(self, obj):
        phone = self.init_data.get('phone')
        duration = self.init_data.get('duration', self.DURATION)
        return PhoneAuth(phone=phone, duration=duration).make_code(duration)

    def send_sms(self):
        data = self.data
        if not data:
            return False

        sended, res = send_sms(to=data['phone'],
                               datas=[data['code'], int(data['duration']/60)],
                               tempId=SMS_TEMPID_SIGNUP)
        print(data, res)
        return sended, data


class OldPhoneAuthSerializer(serializers.Serializer):

    phone = PhoneField(required=True, label='手机电话',
                       error_messages={
                           'required': '请填写手机号码'
                       })

    code = serializers.CharField(required=True, label='验证码',
                                 error_messages={
                                     'required': '请填写手机验证码'
                                 })

    def validate(self, attrs):
        phone, code = attrs.get('phone'), attrs.get('code')
        if ChangePhoneAuth().auth_oldphone_code(phone, code):
            return attrs
        raise validators.ValidationError('验证码无效', code='invalid')


class ChangePhoneAuthSerializer(serializers.Serializer):
    """
        object is instance of account.Profile
    """

    phone = PhoneField(required=True, validators=[validate_phone_unique])

    code = serializers.CharField(required=True, label='验证码',
                                 error_messages={
                                     'required': '请填写手机验证码'
                                 })
    DURATION = PHONE_AUTH_DURATION

    def validate(self, attrs):
        request = self.context.get('request')
        old_phone = request.user.profile.phone
        phone, code = attrs.get('phone'), attrs.get('code')

        has_phone = True
        if old_phone:
            try:
                validate_phone(old_phone)
            except ValidationError:
                has_phone = False
        else:
            has_phone = False

        if has_phone:
            if ChangePhoneAuth(duration=self.DURATION)\
                .auth_newphone_code(old_phone, phone, code):
                return attrs
        elif PhoneAuth(phone, duration=self.DURATION).check_code(code):
            return attrs

        raise validators.ValidationError('验证码无效', code='invalid')

    def restore_object(self, attrs, instance=None):
        instance.phone = attrs.get('phone')
        return instance

    def save_object(self, obj, **kwargs):
        obj.save(update_fields=['phone'])
