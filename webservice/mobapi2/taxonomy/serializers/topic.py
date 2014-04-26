# -*- coding: utf-8 -*-
from rest_framework import serializers
from mobapi2.helpers import get_item_model_by_topic
from taxonomy.models import Topic, TopicalItem
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi2.taxonomy.serializers import get_url_for_taxonomy
from mobapi2.serializers import (
    HyperlinkedWithRouterModelSerializer as HyperlinkedModelSerializer)


class TopicRelatedItemCountUrlAndChildrenUrlMixin(object):
    PREFIX = 'topic'

    item_model_class = None

    def get_items_queryset(self, obj):
        return TopicalItem.objects \
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_items_count(self, obj):
        return self.get_items_queryset(obj).published().count()

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    self.get_items_queryset(obj),
                                    '%s-items' % self.PREFIX,
                                    self.opts.router)

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' % self.PREFIX,
                                    self.opts.router)


class TopicSummarySerializer(TopicRelatedItemCountUrlAndChildrenUrlMixin,
                             HyperlinkedModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

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


class TopicDetailWithPackageSerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    HyperlinkedModelSerializer):
    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

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