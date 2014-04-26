# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import serializers
from mobapi2.rest_fields import factory_imageurl_field
from warehouse.models import Author
from mobapi2.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi2.serializers import HyperlinkedWithRouterModelSerializer as HyperlinkedModelSerializer


class AuthorSerializer(HyperlinkedModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    packages_url = serializers.SerializerMethodField('get_packages_url')

    def get_packages_url(self, obj):
        request = self.context.get('request')
        view_name = self.opts.router.get_base_name('author-packages')
        return request.build_absolute_uri(
            reverse(view_name, kwargs=dict(pk=obj.pk))
        )

    class Meta:
        model = Author
        fields = ('url', 'icon', 'cover', 'name', 'packages_url')


class AuthorSummarySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name')