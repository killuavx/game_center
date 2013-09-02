# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author


class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'name')

class PackageSerializer(serializers.HyperlinkedModelSerializer):

    author = AuthorSummarySerializer()

    class Meta:
        model = Package
        fields = ('url',
                  'package_name',
                  'title',
                  'tags',
                  'summary',
                  'author',
                  'released_datetime')

class PackageDetailSerializer(serializers.HyperlinkedModelSerializer):

    author = AuthorSummarySerializer()

    class Meta:
        model = Package
        fields = ('url',
                  'package_name',
                  'title',
                  'tags',
                  'summary',
                  'description',
                  'author',
                  'released_datetime')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name', 'packages')

    class PackageSummarySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Package
            fields = ( 'url',
                       'package_name',
                       'title',
                       'summary',
                       'released_datetime',
            )

    packages = PackageSummarySerializer(many=True)


