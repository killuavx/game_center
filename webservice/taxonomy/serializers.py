# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        if obj.name:
            return obj.url
        return ""

    def from_native(self, data):
        pass

class CategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    class Meta:
        model = Category
        fields = ('url', 'icon', 'name', 'slug', 'children')

CategorySummarySerializer.children = CategorySummarySerializer(many=True)

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    class Meta:
        model = Category
        fields = ('url', 'icon', 'name', 'slug', 'packages')

from warehouse.serializers import PackageSummarySerializer
CategoryDetailSerializer.packages = PackageSummarySerializer
