# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import PackageVersion, PackageVersionScreenshot
from toolkit.helpers import thumbnail_scale_percents
from mobapi.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi.rest_fields import factory_imageurl_field
from mobapi.serializers import (get_packageversion_comment_queryset,
                                get_packageversion_comments_url)


class PackageVersionScreenshotSerializer(serializers.ModelSerializer):
    large = serializers.SerializerMethodField('get_large_url')
    preview = serializers.SerializerMethodField('get_preview_url')

    # TODO 截图的预览地址，以及后台上传时的尺寸处理，
    def get_preview_url(self, obj):
        try:
            if 'one-third' in obj.image:
                return obj.image['one-third'].url
            else:
                return thumbnail_scale_percents(obj.image, 33).url
        except:
            return ''

    # TODO 截图的大图地址，以及后台上传时的尺寸处理，
    def get_large_url(self, obj):
        try:
            return obj.image['large'].url
        except:
            return ''

    class Meta:
        model = PackageVersionScreenshot
        fields = ('large', 'preview', 'rotate')


class PackageVersionSerializer(serializers.ModelSerializer):
    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    def get_version_download_url(self, obj):
        return get_packageversion_download_url(obj)

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    def get_version_download_size(self, obj):
        return get_packageversion_download_size(obj)

    screenshots = PackageVersionScreenshotSerializer(many=True)

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    def get_version_comment_count(self, obj):
        version_cmt = get_packageversion_comment_queryset(obj)
        return version_cmt.count()

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    def get_version_comments_url(self, obj):
        url = get_packageversion_comments_url(obj)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    class Meta:
        model = PackageVersion
        fields = ('icon',
                  'cover',
                  'version_code',
                  'version_name',
                  'screenshots',
                  'whatsnew',
                  'download',
                  'download_count',
                  'download_size',
                  'comments_url',
                  'comment_count',
        )


def get_packageversion_download_url(version):
    try:
        return version.di_download.url
    except ValueError:
        pass
    try:
        return version.download.url
    except ValueError:
        pass

    return None


def get_packageversion_download_size(version):
    try:
        return version.di_download.size
    except ValueError:
        pass
    try:
        return version.download.size
    except ValueError:
        pass

    return None