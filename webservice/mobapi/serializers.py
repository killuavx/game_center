# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlencode
from rest_framework import serializers
from django.core.urlresolvers import reverse
from comment.models import Comment
from account.models import User as Player


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
            return Comment.objects.with_site().published().filter(
                user=obj).count()
        except:
            return 0

    def get_profile_bookmark_count(self, obj):
        try:
            return obj.profile.bookmarks.published().count()
        except:
            pass
        return 0


class AccountDetailSerializer(AccountRelatedProfileMixin,
                              serializers.ModelSerializer):
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

#---------------------------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    user_icon = serializers.SerializerMethodField('get_user_icon_url')

    def get_user_icon_url(self, obj):
        try:
            return obj.user.profile.icon['small'].url
        except:
            return None

    class Meta:
        model = Comment
        fields = (
            'user_name',
            'user_icon',
            'comment',
            'submit_date',
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


#---------------------------------------------------------------------------
from clientapp.models import ClientPackageVersion


class ClientPackageVersionSerializer(serializers.ModelSerializer):
    download = serializers.SerializerMethodField('get_download_url')

    def get_download_url(self, obj):
        if obj.download:
            return obj.download.url
        return None

    class Meta:
        model = ClientPackageVersion
        fields = (
            'package_name',
            'version_code',
            'version_name',
            'download',
            'download_size',
            'summary',
            'whatsnew',
            'released_datetime',
        )


def get_packageversion_comment_queryset(version):
    version_cmt = Comment.objects.for_model(version)
    return version_cmt.filter(is_public=True, is_removed=False)


def get_packageversion_comments_url(version):
    ct = ContentType.objects.get_for_model(version)
    kwargs = dict(content_type=ct.pk, object_pk=version.pk)
    url = reverse('comment-list')
    return "%s?%s" % (url, urlencode(kwargs))