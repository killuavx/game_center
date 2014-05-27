# -*- coding: utf-8 -*-
from rest_framework import serializers
from clientapp.models import ClientPackageVersion
from mobapi2.serializers import ModelSerializer


class ClientPackageVersionSerializer(ModelSerializer):

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