# -*- encoding=utf-8 -*-
import copy
from rest_framework import  mixins
from warehouse.models import Package, Author
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework import (viewsets,
                            generics,
                            status,
                            filters)
from mobapi.serializers import (PackageSummarySerializer,
                                PackageDetailSerializer,
                                AuthorSerializer)

class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
                       filters.SearchFilter,
    )
    filter_fields = ('package_name', 'title',)
    ordering = ('title',
                'package_name',
                'updated_datetime',
                'released_datetime' )

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self) \
            .retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

class PackageSearchViewSet(PackageViewSet):
    """ 软件搜索接口

    ## 接口访问基本形式:

    1. 搜索软件 /api/search/?q=`{q}`
    2. 响应内容跟一般软件接口结构一致

    `
    Note: 现简单实现搜索 package_name like %{q}% or title like %{q}%
        后期使用full-text search engine
    `
    """

    filter_backends = (filters.DjangoFilterBackend,
                       filters.OrderingFilter,
                       SphinxSearchFilter,
    )
    search_fields = ('package_name', 'title')
    ordering = ('-updated_datetime', )

    def list(self, request, *args, **kwargs):
        querydict = copy.deepcopy(dict(request.GET))
        q = querydict.get('q')
        q = q.pop() if isinstance(q, list) else q
        if not q or not (q and q.strip()):
            data = {'detail': 'Not Allow without search parameter'
                              ' /api/search/?q={q}'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return super(PackageSearchViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = super(PackageSearchViewSet, self) \
            .retrieve(request, *args, **kwargs)
        return response

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.activated()
    serializer_class = AuthorSerializer

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.queryset, pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.published()
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)

class PackageRankingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PackageSummarySerializer
    queryset = Package.objects.published().by_rankings_order()

#------------------------------------------------------------------
from taxonomy.models import Category, Topic, TopicalItem
from mobapi.serializers import ( CategoryDetailSerializer,
                                 CategorySummarySerializer,
                                 TopicSummarySerializer,
                                 TopicDetailWithPackageSerializer )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.as_root().all()
    serializer_class = CategorySummarySerializer
    lookup_field = 'slug'
    paginate_by = None

    @link()
    def packages(self, request, slug, *args, **kwargs):
        category =  generics.get_object_or_404(self.queryset, slug=slug)

        ViewSet = PackageViewSet
        queryset = category.packages.all()
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class, self.serializer_class = self.serializer_class, CategoryDetailSerializer
        origin_queryset, self.queryset = self.queryset, Category.objects.all()

        response = super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        self.queryset = origin_queryset
        return response

from mobapi.helpers import (get_item_model_by_topic,
                              get_viewset_by_topic)

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

#------------------------------------------------------------------
from searcher.models import TipsWord
from mobapi.serializers import TipsWordSerializer

class TipsWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TipsWordSerializer
    queryset = TipsWord.objects.published()

