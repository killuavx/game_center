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
from warehouse.models import Package
from warehouse.views_rest import PackageViewSet, AuthorViewSet

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

class TopicalItemViewSetProxy(object):

    _viewset_map = {
        'default' : PackageViewSet,

        # - 精选推荐
        'home-recommend-game': PackageViewSet,
        # - 网游专区
        'home-network-game': PackageViewSet,

        # - 最新游戏
        'homebar-newest-game': PackageViewSet,
        # - 大型游戏
        'homebar-big-game': PackageViewSet,
        # - 中文游戏
        'homebar-cn-game': PackageViewSet,

        # -- 精选专辑
        'spec-choice-topic': PackageViewSet,
        # -- 顶级开发商
        'spec-top-author': AuthorViewSet,
    }

    def __init__(self, topic):
        self.topic = topic

    def _get_viewset(self, slug):
        try:
            return self._viewset_map[self.topic.slug]
        except KeyError:
            return self._viewset_map['default']
            #raise generics.Http404()

    def _get_model_from_viewset(self, viewset):
        return viewset.serializer_class.Meta.model

    def list_view(self):
        ViewSet = self._get_viewset(self.topic.slug)
        model = self._get_model_from_viewset(ViewSet)
        self.queryset = TopicalItem.objects.get_items_by_topic(self.topic, model)

        return ViewSet.as_view({'get':'list'},
                                            queryset=self.queryset)

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

    @link()
    def items(self, request, slug, *args, **kwargs):
        topic =  generics.get_object_or_404(self.queryset, slug=slug)

        qvs = TopicalItemViewSetProxy(topic)
        list_view = qvs.list_view()
        return list_view(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        origin_serializer_class, self.serializer_class = \
            self.serializer_class, TopicDetailWithPackageSerializer
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response
