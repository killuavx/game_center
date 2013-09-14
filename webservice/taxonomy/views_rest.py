# -*- encoding=utf-8 -*-
from rest_framework import filters
from rest_framework.decorators import link
from taxonomy.models import Category, Topic, TopicalItem
from taxonomy.serializers import ( CategoryDetailSerializer,
                                   CategorySummarySerializer,
                                   TopicSummarySerializer,
                                   TopicDetailWithPackageSerializer )
from rest_framework import viewsets
from rest_framework import generics
from warehouse.views_rest import PackageViewSet

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySummarySerializer
    lookup_field = 'slug'

    @link()
    def items(self, request, slug, *args, **kwargs):
        category =  generics.get_object_or_404(self.queryset, slug=slug)

        ViewSet = PackageViewSet
        queryset = category.packages.all()
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class

        self.serializer_class = CategoryDetailSerializer
        response = super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

from taxonomy.helpers import (get_item_model_by_topic,
                              get_viewset_by_topic,
                              get_basic_topic_info)

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """ TODO 补全专区接口说明

    计划接口列表:
    """

    queryset = Topic.objects.published()
    serializer_class = TopicSummarySerializer
    lookup_field = 'slug'
    filter_backends = (filters.OrderingFilter,
                      filters.DjangoFilterBackend,
                       )
    filter_fields = ('name', 'slug',)
    ordering = ('released_datetime',)

    def list(self, request, *args, **kwargs):
        #origin_queryset, self.queryset = self.queryset, self.queryset.as_root()
        origin_queryset, self.queryset = self.queryset, self.queryset.filter(parent=None)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        return res

    @link()
    def children(self, request, slug, *args, **kwargs):
        """子专区列表"""
        queryset = self.queryset.filter(slug=slug)
        topic =  generics.get_object_or_404(queryset, slug=slug)

        origin_queryset, self.queryset = self.queryset, self.queryset.filter(parent=topic)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        return res

    @link()
    def items(self, request, slug, *args, **kwargs):
        topic =  generics.get_object_or_404(self.queryset, slug=slug)

        list_view = self._get_item_list_view(topic)
        return list_view(request, *args, **kwargs)

    def _get_item_list_view(self, topic):
        ViewSet = get_viewset_by_topic(topic)
        model = get_item_model_by_topic(topic)
        queryset = TopicalItem.objects.get_items_by_topic(topic, model)
        # FIXME 重构此处queryset，使之与ViewSet.queryset可以合并查询
        queryset = queryset.published()
        return ViewSet.as_view({'get':'list'}, queryset=queryset)

    def retrieve(self, request, *args, **kwargs):
        origin_serializer_class, self.serializer_class = \
            self.serializer_class, TopicDetailWithPackageSerializer
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = origin_serializer_class
        return response

    def metadata(self, request):
        data = super(TopicViewSet, self).metadata(request)
        data.pop('description')
        return data
