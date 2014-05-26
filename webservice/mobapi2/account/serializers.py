# -*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.auth import (
    user_login_failed,
    get_backends,
    _clean_credentials)
from toolkit.helpers import import_from
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from comment.models import Comment
from account.models import User as Player
from mobapi2.serializers import ModelSerializer


def filter_keys(data):
    try:
        data.pop('app')
    except KeyError:
        pass


def authenticate(**credentials):
    """
        overwrite authenticate to fix mezzanine.core.auth_backends.MezzanineBackend kwargs error
    If the given credentials are valid, return a User object.
    """
    for backend in get_backends():
        try:
            _credentials = credentials
            if isinstance(backend, import_from('mezzanine.core.auth_backends.MezzanineBackend')):
                _credentials = deepcopy(credentials)
                filter_keys(_credentials)
            user = backend.authenticate(**_credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue

        if user is None:
            continue
            # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__,
                           credentials=_clean_credentials(credentials))


class AccountRelatedProfileMixin(object):
    def get_profile_icon_url(self, obj):
        try:
            return obj.profile.icon.url
        except:
            pass
        return None

    def get_profile_email(self, obj):
        try:
            return obj.profile.email
        except:
            pass
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
