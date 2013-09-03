# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category
from warehouse.serializers import PackageSummarySerializer

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return ''

    def from_native(self, data):
        pass

class CategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    class Meta:
        model = Category
        fields = ('url', 'icon', 'name', 'slug', 'parent', 'children')

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    packages = PackageSummarySerializer(many=True)

    class Meta:
        model = Category
        fields = ('url', 'icon', 'name', 'slug', 'packages')
