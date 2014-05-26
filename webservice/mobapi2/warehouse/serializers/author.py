# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from easy_thumbnails.exceptions import InvalidImageFormatError
from rest_framework import serializers
from mobapi2.rest_fields import factory_imageurl_field
from warehouse.models import Author
from mobapi2.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi2.serializers import HyperlinkedModelSerializer


class AuthorSerializer(HyperlinkedModelSerializer):

    limit_packages = 4

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = serializers.SerializerMethodField('get_cover')
    def get_cover(self, obj):
        try:
            return obj.resources.cover.new20.file.url
        except ObjectDoesNotExist:
            try:
                return obj.cover[IMAGE_COVER_SIZE].url
            except (ValueError, KeyError, InvalidImageFormatError):
                return None
        return None

    packages_url = serializers.SerializerMethodField('get_packages_url')

    def get_packages_url(self, obj):
        request = self.context.get('request')
        view_name = self.opts.router.get_base_name('author-packages')
        return request.build_absolute_uri(
            reverse(view_name, kwargs=dict(pk=obj.pk))
        )

    def filter_items(self, obj, queryset):
        return queryset.published()

    packages = serializers.SerializerMethodField('get_packages')

    def get_packages(self, obj):
        from mobapi2.warehouse.serializers.package import PackageSummarySerializer
        packages = self.filter_items(obj, obj.packages)[0:self.limit_packages]
        return PackageSummarySerializer(packages,
                                        context=self.context,
                                        many=True).data

    class Meta:
        model = Author
        fields = ('url', 'icon', 'cover', 'name', 'packages_url', 'packages')


class AuthorSummarySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name')