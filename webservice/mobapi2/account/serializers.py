# -*- coding: utf-8 -*-
from copy import deepcopy
from django.core.exceptions import ValidationError
from django.db  import models
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.core import validators

from account import authenticate
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
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')


# new profile

class EmailNotSetField(serializers.EmailField):

    default_email_host = PROFILE_EMAIL_DEFAULT_HOST

    default_error_messages = {
        'required': '请填写电子邮件',
        'blank': '请填写电子邮件',
        'invalid': '电子邮箱不正确'
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


PROFILE_BASIC_FIELDS = ('username', 'icon', 'email', 'sex', 'birthday')


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
        .SerializerMethodField('get_bookmark_count')

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
