# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.settings import IMAGE_ICON_SIZE
from mobapi2.taxonomy.serializers import get_url_for_taxonomy


class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

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


class CategoryRelatedChildrenMixin(object):
    def get_children(self, obj):
        qs = obj.children.showed()
        try:
            return CategorySummarySerializer(
                instance=qs,
                many=True,
                context=self.context).data
        except:
            return list()


class CategorySummarySerializer(CategoryRelatedChildrenMixin,
                                serializers.HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    children = serializers.SerializerMethodField('get_children')

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
                  'parent',
                  'children',
        )