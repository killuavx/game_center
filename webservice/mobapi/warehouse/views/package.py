# -*- coding: utf-8 -*-
import copy
from django.core import exceptions
from rest_framework import viewsets, filters, mixins, status, generics
from rest_framework.decorators import link
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from warehouse.models import Package
from taxonomy.models import Category
from mobapi.warehouse.serializers.package import (
    PackageSummarySerializer,
    PackageDetailSerializer,
    PackageUpdateSummarySerializer)


class RelatedPackageSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if not hasattr(view, 'object') or not view.object:
            return queryset

        if not hasattr(view, 'related_package_list') \
            or view.related_package_list is not None:
            return queryset

        qs = queryset._clone()
        qs = qs.exclude(pk=view.object.pk).filter(
            categories__in=list(view.object.categories.published())).distinct()
        tags = list(view.object.tags)
        if len(tags) and qs.count():
            return type(view.object).tagged.with_any(tags, qs)
        return queryset.filter(pk=None)


class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'


class PackageExcludeCategoryOfApplicationFilter(filters.BaseFilterBackend):
    _exclude_category_slug = 'application'

    def filter_queryset(self, request, queryset, view):
        try:
            exclude_pkg_pks = Category.objects \
                .get(slug=self._exclude_category_slug).packages \
                .values_list('pk', flat=True)
            return queryset.exclude(pk__in=exclude_pkg_pks)
        except exceptions.ObjectDoesNotExist:
            return queryset


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """ 软件接口

    ## API访问形式

    * 列表: /api/packages/
        * 最新发布排序: /api/packages/?ordering=`-released_datetime`
        * 最热下载排序: /api/packages/?ordering=`-download_count`
    * 详情: /api/packages/`{id}`/

    ## PackageSummarySerializer 列表软件结构

    * `url`: 详情接口url
    * `icon`: 图标url
    * `title`: 名称
    * `package_name`: 包名
    * `author`:
        * 'url': 作者详情url
        * 'name': 作者名
    * `cover`: 封面图片url
    * `category_name`: 分类名
    * `categories_names`: 多分类列表名称
    * `tags`: 标签名称列表（如`新作`、`首发`、`礼包`）
    * `version_count`: 版本个数
    * `download_count`:下载量
    * `comments_url`: 评论列表接口(可用于发表评论)
    * `summary`: 一句话摘要
    * `released_datetime`: 发布时间(时间戳)

    ## PackageDetailSerializer 详情软件结构

    * `url`: 详情接口url
    * `icon`: 图标url
    * `cover`: 封面图片url
    * `title`: 名称
    * `package_name`: 包名
    * `version_code`: 版本号
    * `version_name`: 版本名
    * `author`: 作者信息
        * 'url': 作者详情url
        * 'name': 作者名
    * `category_name`: 分类名
    * `categories_names`: 多分类列表名称
    * `tags`: 标签名称列表（如`新作`、`首发`、`礼包`）
    * `download_count`: 下载量
    * 'download_size': 下载文件的字节大小
    * `download`: 下载地址
    * `comment_count`: 评论数量
    * `comments_url`: 评论列表接口(同时用于发表评论)
    * `related_packages_url`: 相关应用列表url接口
    * `summary`: 一句话摘要
    * `released_datetime`: 发布时间(时间戳)
    * `whatsnew`: 版本跟新内容说明
    * `description`: 详细介绍
    * `screenshots`: 截图列表
        * 'large': 大截图
        * 'preview': 预览截图
        * 'rotate':旋转角度(-180, -90, 0, 90, 180)负值为逆时针
    * `versions`: 所有版本列表
        * 'icon': 版本图标url
        * 'cover': 版本封面url
        * 'version_code': 版本号
        * 'version_name': 版本名
        * `screenshots`: 版本截图列表
            * 'large': 大截图
            * 'preview': 预览截图
            * 'rotate':旋转角度(-180, -90, 0, 90, 180)负值为逆时针
        * 'whatsnew': 版本跟新内容介绍
        * 'download': 版本下载地址
        * 'download_count': 版本下载量
        * 'download_size': 版本文件字节大小
        * 'comment_count': 版本评论数量
        * 'comments_url': 版本评论列表地址(同时作为发表评论使用)

    """

    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       RelatedPackageSearchFilter
    )
    filter_fields = ('package_name', 'title',)
    ordering = ('title',
                'package_name',
                'updated_datetime',
                'released_datetime')

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self) \
            .retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

    @link()
    def relatedpackages(self, request, *args, **kwargs):

        self.object = self.get_object(self.get_queryset())
        self.related_package_list = None
        response = self.list(request, *args, **kwargs)
        self.related_package_list = self.object_list

        return response


class PackageRankingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PackageSummarySerializer
    queryset = Package.objects.published().by_rankings_order()
    filter_backends = (PackageExcludeCategoryOfApplicationFilter, )


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


class PackageUpdateView(generics.CreateAPIView):
    """ 应用升级检查接口

    ### 访问方式

        POST /api/updates/
        Content-Type: application/json
        ...

        {"versions":[{"package_name":"com.carrot.carrotfantasy","version_name":"1.1.1","version_code":258}]}

    #### HTTP Body Data

        {"versions":[{"package_name":"com.carrot.carrotfantasy","version_name":"1.1.1","version_code":258}]}

    * versions: 客户端已安装的应用版本列表
        * `package_name`: 包名
        * `version_name`: 版本名
        * `version_code`: 版本号

    ### 响应

    #### HTTP Response Body 响应内容

        [{
            "url": "http://localhost:8000/api/packages/1/",
            "icon": "",
            "package_name": "com.eamobile.sims3_row_qwf",
            "title": "\u6a21\u62df\u4eba\u751f",
            "download": "http://localhost:8000/media/packages/com.guruas.mazegamej-27.1_6.apk",
            "download_size": 3256602,
            "version_code": 2,
            "version_name": "2.0",
            "released_datetime": "1378109580",
            "actions": {
                "mark": "http://localhost:8000/api/bookmarks/1/"
            },
            "is_updatable": True
        }
        ]

    * `url` : 详情地址
    * `icon` : 图标地址
    * `package_name` : 包名
    * `title` : 应用名字
    * `download` : 下载地址
    * `download_size` : 下载文件大小
    * `version_code` : 最新版本号
    * `version_name` : 最新版本号
    * `released_datetime` : 发布时间

    #### HTTP Response Status

    * 200 HTTP_200_OK
        * 获取成功
        * 返回应用升级列表信息
    * 400 HTTP_400_BAD_REQUEST
        * 请求格式有错

    #### 注意

        如果平台上没有应用数据，或应用不可更新，返回结果中不会包含对应的应用数据

    ----

    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PackageUpdateSummarySerializer
    parser_classes = (JSONParser, FormParser)
    queryset = Package.objects.published()

    def _make_sorted_idx(self, versions):
        sorted_pkg_idx = dict()
        for i, v in enumerate(versions):
            v.update(dict(order_idx=i))
            sorted_pkg_idx[v.get('package_name')] = v
        return sorted_pkg_idx

    def post(self, request, *args, **kwargs):
        try:
            versions = request.DATA.pop('versions')
        except KeyError:
            return Response(dict(detail='versions list should not be empty'),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            sorted_pkg_idx = self._make_sorted_idx(versions)
        except TypeError as e:
            return Response(dict(detail='versions should be list type'),
                            status=status.HTTP_400_BAD_REQUEST)

        pkg_names = sorted_pkg_idx.keys()
        pkgs = self.queryset.filter(package_name__in=pkg_names).all()

        def _sorted_key(p):
            idx = sorted_pkg_idx[p.package_name]['order_idx']
            return idx

        sorted_pkgs = sorted(pkgs, key=_sorted_key)

        def _fill_update_info(p):
            p.update_info = sorted_pkg_idx[p.package_name]
            return p

        fill_update_pkgs = map(_fill_update_info, sorted_pkgs)
        serializer = PackageUpdateSummarySerializer(fill_update_pkgs,
                                                    many=True,
                                                    context=dict(
                                                        request=request))
        data = self._filter_ignore_disupdatable(serializer.data)
        return Response(data, status.HTTP_200_OK)

    def _filter_ignore_disupdatable(self, datalist):
        return list(filter(lambda e: e['is_updatable'], datalist))



