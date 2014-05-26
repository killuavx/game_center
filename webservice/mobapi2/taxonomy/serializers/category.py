# -*- coding: utf-8 -*-
from rest_framework import serializers
from taxonomy.models import Category
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.settings import IMAGE_ICON_SIZE
from mobapi2.taxonomy.serializers import get_url_for_taxonomy
from mobapi2.serializers import (
    HyperlinkedWithRouterModelSerializer as HyperlinkedModelSerializer)
from mobapi2.warehouse.serializers.package import PackageSummarySerializer


class CategoryDetailSerializer(HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    packages_url = serializers.SerializerMethodField('get_items_url')

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX,
                                    self.opts.router)

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


class CategoryRelatedPackagesMixin(object):

    serializer_class_package = PackageSummarySerializer

    limit_packages = 4

    def get_packages(self, obj):
        if obj.children.count():
            return list()
        packages = obj.packages.published().by_published_order(True)[0:self.limit_packages]
        return self.serializer_class_package(packages,
                                             context=self.context,
                                             many=True).data


class CategorySummarySerializer(CategoryRelatedChildrenMixin,
                                CategoryRelatedPackagesMixin,
                                HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    children = serializers.SerializerMethodField('get_children')

    packages_url = serializers.SerializerMethodField('get_items_url')

    packages = serializers.SerializerMethodField('get_packages')

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX,
                                    self.opts.router)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'packages_url',
                  'parent',
                  'children',
                  'packages',
        )