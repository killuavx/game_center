# -*- coding: utf-8 -*-
from rest_framework import serializers
from clientapp.models import ClientPackageVersion, client_download_url
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