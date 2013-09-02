# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author


class PackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Package
        fields = ('url', 'package_name',
                  'title',
                  'tags',
                  'summary',
                  'description',
                  'author',
                  'released_datetime')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    #packages = serializers.HyperlinkedRelatedField(many=True, view_name='package-detail')
    class Meta:
        model = Author
        fields = ('url', 'name', 'packages')
