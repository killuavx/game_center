# -*- coding: utf-8 -*-
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import link
from mobapi2.helpers import get_viewset_by_topic, get_item_model_by_topic
from taxonomy.models import Topic, TopicalItem
from mobapi2.taxonomy.serializers.topic import (
    TopicSummarySerializer,
    TopicDetailWithPackageSerializer)
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.utils import (
    default_list_cache_key_func,
    default_object_cache_key_func)
from mobapi2 import cache_keyconstructors as ckc


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """ 专区接口

    ## 接口访问基本形式:

    1. 专区详细信息:
        /api/topics/{slug}
    2. 子专区列表:
        /api/topics/{slug}/children
    3. 关联对象列表:
        /api/topics/{slug}/items

    ## 专区类型

    * 一级专区软件列表, `只有`items_url能有效访问关联软件列表

        * 精选推荐  slug:`home-recommend-game`

        * 网游专区  slug:`home-network-game`

        * 最新游戏  slug:`homebar-newest-game`

        * 大型游戏  slug:`homebar-big-game`

        * 中文游戏  slug:`homebar-cn-game`


    * 二级专区列表
        * 精选专辑, 通过访问对应的`*_url`，获得下一级的关联数据列表，
        从`*_url`获得关联对象列表的数据，
        再从author.packages_url/topic.items_url获得该级对象的软件列表

            slug:`spec-choice-topic`
            children_url: 子专区url, 类型Topic

        * 顶级开发商

            slug:`spec-top-author`
            item_url: 开发商列表url, 类型Author

    TODO 添加以上7个专区以及开发者和游戏数据
    """

    model = Topic
    serializer_class = TopicSummarySerializer
    lookup_field = 'slug'
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
    )
    filter_fields = ('name', 'slug',)
    ordering = ('released_datetime', )

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Topic.objects.all()
        return self.queryset.published()

    @cache_response(key_func=default_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        origin_queryset, self.queryset = self.queryset, self.get_queryset().as_root()
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        return res

    @cache_response(key_func=ckc.LookupListKeyConstructor())
    @link()
    def children(self, request, slug, *args, **kwargs):
        """子专区列表"""
        queryset = self.get_queryset().filter(slug=slug)
        topic = generics.get_object_or_404(queryset, slug=slug)

        origin_queryset, self.queryset = \
            self.queryset, self.get_queryset().filter(parent=topic)
        self.ordering = ('-updated_datetime', )
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        self.ordering = ('released_datetime', )
        return res

    @cache_response(key_func=ckc.LookupOrderingListKeyConstructor())
    @link()
    def items(self, request, slug, *args, **kwargs):
        topic = generics.get_object_or_404(self.get_queryset(), slug=slug)

        list_view = self._get_item_list_view(topic)
        return list_view(request, *args, **kwargs)

    def _get_item_list_view(self, topic):
        queryset = self.item_list_view_queryset(topic)
        # FIXME 重构此处queryset，使之与ViewSet.queryset可以合并查询
        # FIXME 重构此处，预先检查有无filter backend, OrderingFilter, 如果有OrderingFilter并有filter查询请求，则使用指定排序
        # ignore filter backend ordering
        # using queryset pass by TopicalItem.ordering,
        ViewSet = self.item_list_view(topic)
        return ViewSet.as_view({'get': 'list'},
                               queryset=queryset)

    @classmethod
    def item_list_view(cls, topic):
        ViewSet = get_viewset_by_topic(topic)
        ViewSet.ordering = ()
        return ViewSet

    @classmethod
    def item_list_view_queryset(cls, topic):
        model = get_item_model_by_topic(topic)
        queryset = TopicalItem.objects.get_items_by_topic(topic, model)
        return queryset

    @cache_response(key_func=default_object_cache_key_func)
    def retrieve(self, request, *args, **kwargs):
        origin_serializer_class, self.serializer_class = \
            self.serializer_class, TopicDetailWithPackageSerializer
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = origin_serializer_class
        return response

