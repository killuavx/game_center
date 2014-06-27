# -*- coding: utf-8 -*-
from rest_framework import serializers, status
from taxonomy.models import Category
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.settings import IMAGE_ICON_SIZE
from mobapi2.taxonomy.serializers import get_url_for_taxonomy
from mobapi2.serializers import (
    HyperlinkedWithRouterModelSerializer as HyperlinkedModelSerializer)
from mobapi2.warehouse.serializers.package import PackageSummarySerializer
from mobapi2.helpers import get_category_packages_url
from mobapi2.rest_clients import android_api
from toolkit.helpers import SITE_ANDROID, get_global_site


class CategoryDetailSerializer(HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    packages_url = serializers.SerializerMethodField('get_items_url')

    def get_items_url(self, obj):
        return get_category_packages_url(obj,
                                         router=self.opts.router,
                                         request=self.context.get('request'))

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
        if get_global_site() and get_global_site().pk == SITE_ANDROID:
            api = android_api
        else:
            api = None
        if not api:
            return list()

        res = api.packages.get(params=dict(
            category=obj.pk,
            ordering='-released_datetime',
        ))
        if res.status != status.HTTP_200_OK:
            return list()
        if res.data and res.data.get('count') and res.data.get('results'):
            results = res.data.get('results', list())
            return results[0:self.limit_packages]
        return list()


class CategorySummarySerializer(CategoryRelatedChildrenMixin,
                                CategoryRelatedPackagesMixin,
                                HyperlinkedModelSerializer):
    PREFIX = 'category'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    children = serializers.SerializerMethodField('get_children')

    packages_url = serializers.SerializerMethodField('get_items_url')

    packages = serializers.SerializerMethodField('get_packages')

    def get_items_url(self, obj):
        return get_category_packages_url(obj,
                                         router=self.opts.router,
                                         request=self.context.get('request'))

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
