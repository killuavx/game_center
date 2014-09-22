# -*- coding: utf-8 -*-
from rest_framework import serializers
from promotion.models import Advertisement, Recommend
from mobapi2.settings import IMAGE_ADV_COVER_SIZE, IMAGE_ICON_SIZE
from mobapi2.serializers import HyperlinkedModelSerializer, ModelGetResourceMixin
from urllib.parse import urlparse


class AdvertisementGetResourceMixin(ModelGetResourceMixin):

    DEFAULT_COVER_SIZE = IMAGE_ADV_COVER_SIZE


class AdvertisementSerializer(AdvertisementGetResourceMixin,
                              HyperlinkedModelSerializer):

    content_url = serializers.SerializerMethodField('get_content_url')

    def get_content_url(self, obj):
        hlid = serializers.HyperlinkedIdentityField(
                        source='content',
                        view_name=self.opts.router.get_base_name('package-detail'),
        )
        hlid.context = self.context
        return hlid.field_to_native(obj.content, 'content_url')

    content_type = serializers.SerializerMethodField('get_content_type')

    def get_content_type(self, obj):
        return str(obj.content_type).lower()

    cover = serializers.SerializerMethodField('get_cover')

    class Meta:
        model = Advertisement
        fields = ('title',
                  'cover',
                  'content_url',
                  'content_type',
        )


class RecommendSerializer(HyperlinkedModelSerializer):

    content_url = serializers.SerializerMethodField('get_content_url')

    def get_content_url(self, obj):
        hlid = serializers.HyperlinkedIdentityField(
            source='content',
            view_name=self.opts.router.get_base_name('package-detail'),
            )
        hlid.context = self.context
        return hlid.field_to_native(obj.content, 'content_url')

    def get_content_type(self, obj):
        return str(obj.content_type).lower()

    content_type = serializers.SerializerMethodField('get_content_type')

    icon = serializers.SerializerMethodField('get_icon_url')

    def get_icon_url(self, obj):
        try:
            return obj.icon[IMAGE_ICON_SIZE].url
        except:
            try:
                request = self.context.get('request')
                return request.build_absolute_uri(urlparse(obj.icon.url).path)
            except:
                return None

    cover = serializers.SerializerMethodField('get_cover_url')

    def get_cover_url(self, obj):
        try:
            return obj.cover[IMAGE_ADV_COVER_SIZE].url
        except:
            try:
                request = self.context.get('request')
                return request.build_absolute_uri(urlparse(obj.cover.url).path)
            except:
                return None

    class Meta:
        model = Recommend
        fields = ('title',
                  'icon',
                  'cover',
                  'title',
                  'summary',
                  'content_url',
                  'content_type',
        )
