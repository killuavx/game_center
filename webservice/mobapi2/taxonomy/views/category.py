# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.decorators import link
from rest_framework.settings import api_settings
from taxonomy.models import Category
from mobapi.taxonomy.serializers.category import CategorySummarySerializer, CategoryDetailSerializer
from mobapi.warehouse.views.package import PackageViewSet


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ 分类接口

    ## 分类树接口

        GET /api/categories/

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功, 返回分类树状结构的列表数据

    ### 单个分类元素数据结构

    * `url`: 详细信息接口
    * `icon`: 图标地址
    * `name`: 分类名字
    * `slug`: 分类唯一标识的名字
    * `packages_url`: 分类软件列表接口
    * `parent`: 父级分类详细信息接口
    * `children`: 子级分裂列表

    ----

    ## 分类应用列表接口

        GET /api/topics/{slug}/packages/?page_size=10

    #### 请求信息

    * `{slug}`: 分类slug
    * `page_size`: 每页个数

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功, 返回应用列表, 数据结构见[应用列表接口](/api/packages/)

    ----

    """
    serializer_class = CategorySummarySerializer
    model = Category
    lookup_field = 'slug'
    paginate_by = None

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Category.objects
        return self.queryset.as_root().showed()

    @link()
    def packages(self, request, slug, *args, **kwargs):
        queryset = Category.objects.published()
        category = generics.get_object_or_404(queryset, slug=slug)

        list_view = self.get_packages_list_view(request, category)
        return list_view(request, *args, **kwargs)

    def get_packages_list_view(self, request, category):
        ViewSet = PackageViewSet
        queryset = category.packages.all()
        queryset = queryset.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view

    def filter_packages_list_view(self, list_view, request, category):
        list_view.paginate_by = request.GET.get(
            api_settings.PAGINATE_BY_PARAM, api_settings.PAGINATE_BY)
        list_view.max_paginate_by = 50
        return list_view

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class, self.serializer_class = self.serializer_class, CategoryDetailSerializer
        origin_queryset, self.queryset = self.queryset, Category.objects.all()

        response = super(CategoryViewSet, self).retrieve(request, *args,
                                                         **kwargs)
        self.serializer_class = list_serializer_class
        self.queryset = origin_queryset
        return response