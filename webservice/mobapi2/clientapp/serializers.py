# -*- coding: utf-8 -*-
from rest_framework import serializers
from clientapp.models import ClientPackageVersion, client_download_url, LoadingCover
from mobapi2.serializers import ModelSerializer


class ClientPackageVersionSerializer(ModelSerializer):

    entrytype = 'client'

    download = serializers.SerializerMethodField('get_download_url')

    def get_download_url(self, obj):
        dwurl = client_download_url(obj.package_name, entrytype=self.entrytype)
        request = self.context.get('request')
        if request:
            dwurl = request.build_absolute_uri(dwurl)
        return dwurl

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


class LoadingCoverSerializer(ModelSerializer):

    url = serializers.SerializerMethodField('get_link_url')

    def get_link_url(self, obj):
        content = obj.content
        if not content:
            return None

        if hasattr(content, 'get_absolute_url_as'):
            return content.get_absolute_url_as(product='client')

        return content

    content_type = serializers.SerializerMethodField('get_content_type')

    def get_content_type(self, obj):
        if obj.link:
            return 'link'
        elif obj.content_type:
            return obj.content_type.model
        else:
            return None

    def get_cover_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    cover = serializers.SerializerMethodField('get_cover_url')

    class Meta:
        model = LoadingCover
        fields = (
            'url',
            'title',
            'content_type',
            'cover',
            'publish_date',
            'expiry_date',
        )

