# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlencode
from rest_framework import serializers
from django.core.urlresolvers import reverse
from comment.models import Comment
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