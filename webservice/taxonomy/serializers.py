# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.helpers import get_item_model_by_topic
from taxonomy.models import Category, Topic, TopicalItem
from django.core.urlresolvers import reverse

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

def get_url_for_taxonomy(request, obj, related_items, reverse_viewname):
    if related_items.count() > 0:
        path = reverse(reverse_viewname, kwargs=dict(slug=obj.slug))
        if request:
            return request.build_absolute_uri(path)
        return path
    return None

class CategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    PREFIX = 'category'

    icon = ImageUrlField()

    packages_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'parent',
                  'children',
                  'packages_url',
        )

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):

    PREFIX = 'category'

    icon = ImageUrlField()

    packages_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'packages_url',
        )


class TopicRelatedItemCountUrlAndChildrenUrlMixin(object):

    PREFIX = 'topic'

    item_model_class = None

    def get_items_queryset(self, obj):
        return TopicalItem.objects\
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_items_count(self, obj):
        return self.get_items_queryset(obj).count()

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    self.get_items_queryset(obj),
                                    '%s-items' %self.PREFIX)

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' %self.PREFIX)

class TopicDetailWithPackageSerializer(
                                TopicRelatedItemCountUrlAndChildrenUrlMixin,
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

class TopicSummarySerializer(
                            TopicRelatedItemCountUrlAndChildrenUrlMixin,
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

