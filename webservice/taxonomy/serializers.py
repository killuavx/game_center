# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category, Topic
from django.core.urlresolvers import reverse

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

class CategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        if obj.packages.count() > 0:
            request = self.context.get('request')
            path = reverse('categories-items', kwargs=dict(slug=obj.slug))
            if request:
                return request.build_absolute_uri(path)
            return path
        return None

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'parent',
                  'children',
                  'items_url',
        )

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        if obj.packages.count() > 0:
            request = self.context.get('request')
            path = reverse('categories-items', kwargs=dict(slug=obj.slug))
            if request:
                return request.build_absolute_uri(path)
            return path
        return None

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'items_url',
        )

class TopicRelatedMethodFieldMixin(object):

    def get_items_url(self, obj):
        if obj.items.count() > 0:
            request = self.context.get('request')
            path = reverse('topic-items', kwargs=dict(slug=obj.slug))
            if request:
                return request.build_absolute_uri(path)
            return path
        return None

    def get_items_count(self, obj):
        return obj.children.count()

    def get_children_url(self, obj):
        if obj.children.count() > 0:
            request = self.context.get('request')
            path = reverse('topic-children', kwargs=dict(slug=obj.slug))
            if request:
                return request.build_absolute_uri(path)
            return path
        return None

class TopicDetailWithPackageSerializer(TopicRelatedMethodFieldMixin,
                                       serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    cover = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'name',
                  'slug',
                  'summary',
                  'children_url',
                  'items_url',
                  'items_count',
                  'updated_datetime',
                  'released_datetime')

class TopicSummarySerializer(TopicRelatedMethodFieldMixin,
                             serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    cover = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'children_url',
                  'items_url',
                  'items_count',
                  'name',
                  'slug',
                  'updated_datetime',
                  'released_datetime')

