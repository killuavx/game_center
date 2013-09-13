# -*- encoding=utf-8 -*-
from rest_framework import filters
from rest_framework.decorators import link
from taxonomy.models import Category, Topic, TopicalItem
from taxonomy.serializers import CategoryDetailSerializer,\
    CategorySummarySerializer,\
    TopicSummarySerializer, \
    TopicDetailWithPackageSerializer
from rest_framework import viewsets
from rest_framework import generics
from warehouse.models import Package
from warehouse.views_rest import PackageViewSet

from pprint import pprint as print

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySummarySerializer
    lookup_field = 'slug'

    item_viewset_package = PackageViewSet

    @link()
    def items(self, request, slug, *args, **kwargs):
        category =  generics.get_object_or_404(self.queryset, slug=slug)

        Pkg_ViewSet = self.item_viewset_package
        pkg_queryset = Pkg_ViewSet.queryset.by_category(category)
        package_list = Pkg_ViewSet.as_view({'get':'list'},
                                           queryset=pkg_queryset)
        return package_list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class

        self.serializer_class = CategoryDetailSerializer
        response = super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.published()
    serializer_class = TopicSummarySerializer
    lookup_field = 'slug'
    filter_backends = (filters.OrderingFilter,
                      filters.DjangoFilterBackend,
                       )
    filter_fields = ('name', 'slug',)
    ordering = ('released_datetime',)

    def list(self, request, *args, **kwargs):
        origin_queryset, self.queryset = self.queryset, self.queryset.as_root()
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        return res

    @link()
    def children(self, request, slug, *args, **kwargs):
        queryset = self.queryset.filter(slug=slug)
        topic =  generics.get_object_or_404(queryset, slug=slug)

        origin_queryset, self.queryset = self.queryset, self.queryset.by_parent(topic)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        return res

    item_viewset_package = PackageViewSet

    @link()
    def items(self, request, slug, *args, **kwargs):
        topic =  generics.get_object_or_404(self.queryset, slug=slug)

        Pkg_ViewSet = self.item_viewset_package
        pkg_queryset = TopicalItem.objects.get_items_by_topic(topic, Package)
        package_list_view = Pkg_ViewSet.as_view({'get':'list'},
                                           queryset=pkg_queryset)
        return package_list_view(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        origin_serializer_class, self.serializer_class = \
            self.serializer_class, TopicDetailWithPackageSerializer
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response
