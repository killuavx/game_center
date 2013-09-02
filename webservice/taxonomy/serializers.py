# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'slug', 'packages')
