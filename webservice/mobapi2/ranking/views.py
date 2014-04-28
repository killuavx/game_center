# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from rest_framework import viewsets, filters
from rest_framework.decorators import link
from mobapi2.warehouse.views.package import PackageViewSet
from mobapi2.ranking.serializers import PackageRankingSummarySerializer
from ranking.models import PackageRanking


class RankingFilter(filters.BaseFilterBackend):

    CHOICE_CYCLE_TYPE = PackageRankingSummarySerializer.CHOICE_CYCLE_TYPE

    def filter_queryset(self, request, queryset, view):
        if self.has_filter_ranking_pk(request, queryset, view):
            return queryset
        return self.filter_queryset_ranking_params(request, queryset, view)

    def has_filter_ranking_pk(self, request, queryset, view):
        resolve_match = resolve(request.path)
        if 'pk' in resolve_match.kwargs:
            return True
        return False

    def filter_queryset_ranking_params(self, request, queryset, view):
        category_slug = request.GET.get('category')
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)

        ranking_type = request.GET.get('ranking_type')
        if ranking_type is not None:
            queryset = queryset.filter(ranking_type__slug=ranking_type)

        cycle = request.GET.get('cycle')
        if cycle not in self.CHOICE_CYCLE_TYPE:
            cycle = 'all'
        cycle_type = self.CHOICE_CYCLE_TYPE[cycle]
        return queryset.filter(cycle_type=cycle_type)


class PackageRankingViewSet(viewsets.ReadOnlyModelViewSet):
    """ 软件接口

    ## API访问形式

    * 列表: /api/rankings/?
        * 游戏分类总排行: /api/rankings/?category=game
        * 游戏分类的周排行: /api/rankings/?category=game&cycle=weekly
    * 详情: /api/rankings/`{id}`/

    ## PackageRankingSummarySerializer 字段结果

    * `url`: 详情地址, 如"http://0.0.0.0:8080/api/v2/rankings/1/",
    * `ranking_name`: 排行名称
    * `ranking_slug`: 排行slug名,
    * `category_name`: 分类名称,
    * `category_slug`: 分类slug名,
    * `cycle_type`: 周期类型[all: 总榜, daily: 每日榜, weekly: 每周榜, monthly: 每周榜]其一, 如all
    * `packages_url`: 榜单应用列表地址, 如"http://0.0.0.0:8080/api/v2/rankings/1/packages/", 详情见[/api/v2/packages](应用列表接口)
    * `packages`: 榜单topN的应用列表

    ## PackageSummarySerializer 应用结构详情见[/api/v2/packages](应用列表接口)

    """

    view_name = 'ranking'
    model = PackageRanking
    serializer_class = PackageRankingSummarySerializer
    filter_backends = (RankingFilter, )

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        return self.queryset

    @link()
    def packages(self, request, pk, *args, **kwargs):
        ranking = self.get_object()
        list_view = self.get_packages_list_view(request, ranking)
        return list_view(request, *args, **kwargs)

    def get_packages_list_view(self, request, ranking):
        ViewSet = PackageViewSet
        queryset = ranking.packages.all()
        queryset = queryset.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view


class RankingPackageFilter(filters.BaseFilterBackend):

    CHOICE_CYCLE_TYPE = PackageRankingSummarySerializer.CHOICE_CYCLE_TYPE

    def filter_queryset(self, request, queryset, view):
        # 根据榜单id查询
        ranking_pk = request.GET.get('ranking_pk')
        if ranking_pk and str(ranking_pk).isnumeric():
            queryset = queryset.filter(rankings__pk=int(ranking_pk))
            return queryset

        category_slug = request.GET.get('category')
        cycle = request.GET.get('cycle')
        ranking_type = request.GET.get('ranking_type')
        if cycle not in self.CHOICE_CYCLE_TYPE:
            cycle = 'all'
        cycle_type = self.CHOICE_CYCLE_TYPE[cycle]

        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)

        if ranking_type is not None:
            queryset = queryset.filter(ranking_type__slug=ranking_type)

        return queryset.filter(cycle_type=cycle_type)



