# -*- coding: utf-8 -*-
from rest_framework import serializers
from promotion.models import Advertisement
from mobapi.rest_fields import factory_imageurl_field


class AdvertisementSerializer(serializers.HyperlinkedModelSerializer):
    content_url = serializers.SerializerMethodField('get_content_url')

    def get_content_url(self, obj):
        hlid = serializers.HyperlinkedIdentityField(source='content',
                                                    view_name='package-detail',
        )
        hlid.context = self.context
        return hlid.field_to_native(obj.content, 'content_url')

    content_type = serializers.SerializerMethodField('get_content_type')

    def get_content_type(self, obj):
        return str(obj.content_type).lower()

    cover = factory_imageurl_field(None)

    class Meta:
        model = Advertisement
        fields = ('title',
                  'cover',
                  'content_url',
                  'content_type',
        )

