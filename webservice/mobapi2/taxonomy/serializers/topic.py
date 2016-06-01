# -*- coding: utf-8 -*-
from rest_framework import serializers
from mobapi2.helpers import (
    get_item_model_by_topic,
    get_viewset_by_topic,
    get_topic_packages_url,
    get_topic_authors_url,
    )

from taxonomy.models import Topic, TopicalItem
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.settings import IMAGE_ICON_SIZE
from mobapi2.serializers import HyperlinkedModelSerializer, ModelGetResourceMixin
from mobapi2.taxonomy.serializers import get_url_for_taxonomy
from warehouse.models import Package, Author


class TopicRelatedItemsMixin(object):

    limit_items = 4

    def filter_items(self, obj, queryset):
        model = get_item_model_by_topic(obj)
        if model is Package:
            return queryset.published().by_released_order(True)
        else:
            return queryset

    def get_items_queryset(self, obj):
        return TopicalItem.objects \
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_item_serializer_class(self, obj):
        return get_viewset_by_topic(obj).serializer_class

    def get_items(self, obj):
        if obj.children.count():
            return list()
        queryset = self.get_items_queryset(obj)
        serializer_class_item = self.get_item_serializer_class(obj)
        items = self.filter_items(obj, queryset)[0:self.limit_items]
        return serializer_class_item(items,
                                     context=self.context,
                                     many=True).data


class TopicRelatedItemCountUrlAndChildrenUrlMixin(object):

    PREFIX = 'topic'

    item_model_class = None

    def get_items_queryset(self, obj):
        return TopicalItem.objects \
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_items_count(self, obj):
        return self.get_items_queryset(obj).published().count()

    def get_items_url(self, obj):
        model = get_item_model_by_topic(obj)
        if model is Package or issubclass(model, Package):
            return get_topic_packages_url(obj,
                                          router=self.opts.router,
                                          request=self.context.get('request')
                                          )
        elif model is Author or issubclass(model, Author):
            return get_topic_authors_url(obj,
                                         router=self.opts.router,
                                         request=self.context.get('request')
            )
        else:
            return None

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' % self.PREFIX,
                                    self.opts.router)


class TopicGetResourceMixin(ModelGetResourceMixin):
    pass



class TopicSummarySerializer(TopicRelatedItemCountUrlAndChildrenUrlMixin,
                             TopicRelatedItemsMixin,
                             TopicGetResourceMixin,
                             HyperlinkedModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = serializers.SerializerMethodField('get_default_cover')

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'summary',
                  'children_url',
                  'items_url',
                  'items_count',
                  'items',
                  'name',
                  'slug',
                  'updated_datetime',
                  'released_datetime')


class TopicDetailWithPackageSerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    TopicGetResourceMixin,
    HyperlinkedModelSerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = serializers.SerializerMethodField('get_default_cover')

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
