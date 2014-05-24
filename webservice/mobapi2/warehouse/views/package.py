# -*- coding: utf-8 -*-
import copy
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import link
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from warehouse.models import Package
from mobapi2.warehouse.serializers.package import (
    PackageSummarySerializer,
    PackageDetailSerializer,
    PackageUpdateSummarySerializer)
from mobapi2.warehouse.views.filters import (
    PackageIdsFilter,
    SolrSearchFilter,
    RelatedPackageSearchFilter)
from django.http import Http404
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.utils import (
    default_list_cache_key_func,
    default_object_cache_key_func)
from rest_framework_extensions.key_constructor import (
    bits,
    constructors
)
from mobapi2 import cache_keyconstructors as ckc


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
    * `supported_languages`: 支持语言,如:“中文,英文,其他”
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

    model = Package
    serializer_class = PackageSummarySerializer
    serializer_class_detail = PackageDetailSerializer
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       RelatedPackageSearchFilter
    )
    filter_fields = ('package_name', 'title', 'categories')
    ordering = ('-released_datetime',
                '-updated_datetime',
                'title',
                'package_name'
                )

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        return self.queryset.published()

    @cache_response(key_func=default_object_cache_key_func)
    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = self.serializer_class_detail
        response = super(PackageViewSet, self) \
            .retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

    @cache_response(key_func=ckc.LookupOrderingListKeyConstructor())
    @link()
    def relatedpackages(self, request, *args, **kwargs):

        self.object = self.get_object(self.get_queryset())
        self.related_package_list = None
        response = self.list(request, *args, **kwargs)
        self.related_package_list = self.object_list

        return response

    @cache_response(key_func=default_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        return super(PackageViewSet, self).list(request, *args, **kwargs)


class PackageSearchListKeyConstructor(constructors.DefaultKeyConstructor):

    q = bits.QueryParamsKeyBit(params=['q'])

    pagination = bits.PaginationKeyBit()


package_search_cache_list_key_func = PackageSearchListKeyConstructor()


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
                       #SphinxSearchFilter,
                       SolrSearchFilter,
    )
    search_fields = ('title', 'tags_text', 'package_name', 'categories')
    search_ordering = ('-released_datetime', )
    #ordering = ('-updated_datetime', )

    @cache_response(key_func=package_search_cache_list_key_func)
    def list(self, request, *args, **kwargs):
        querydict = copy.deepcopy(dict(request.GET))
        q = querydict.get('q')
        q = q.pop() if isinstance(q, list) else q
        if not q or not (q and q.strip()):
            data = {'detail': 'Not Allow without search parameter'
                              ' /api/search/?q={q}'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        return super(PackageViewSet, self).list(request, *args, **kwargs)


class UpdatePostKeyBit(bits.KeyBitDictBase):

    def get_source_dict(self, *args, **kwargs):
        request = kwargs.get('request')
        return request.DATA

    def get_data(self, **kwargs):
        kwargs['params'] = []
        kwargs['params'].append('versions')
        return super(UpdatePostKeyBit, self).get_data(**kwargs)


class UpdatePostKeyConstructor(constructors.DefaultKeyConstructor):

    versions = UpdatePostKeyBit()


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
    model = Package

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        return self.queryset

    def _make_sorted_idx(self, versions):
        sorted_pkg_idx = dict()
        for i, v in enumerate(versions):
            v.update(dict(order_idx=i))
            sorted_pkg_idx[v.get('package_name')] = v
        return sorted_pkg_idx

    @cache_response(key_func=UpdatePostKeyConstructor())
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
        pkgs = self.get_queryset().filter(package_name__in=pkg_names).all()

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


class IdsKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        kwargs['params'].append('ids')
        return super(IdsKeyBit, self).get_data(**kwargs)


class PushListKeyConstructor(constructors.DefaultListKeyConstructor):

    ids = IdsKeyBit()


class PackagePushView(generics.ListAPIView):
    """  推送软件列表查询

    ### 访问方式

        GET /api/push/packages/?ids={pk1},{pk2}...
        Content-Type: application/json

    #### 请求参数

    * `ids`: 以","分隔的软件包id列表

    ### 响应

    #### HTTP Response Body 响应内容

        [
            {
                "url": "http://gc.ccplay.com.cn/api/packages/451/",
                "icon": "http://gc.ccplay.com.cn/media/package/451/v11/icon.png.72x72_q85_upscale.png",
                "cover": null,
                "package_name": "com.feelingtouch.dragonwarcraft",
                "title": "\u9f99\u7a74\u52c7\u58eb\u91d1\u5e01\u65e0\u9650\u7248",
                "version_code": 11,
                "version_name": "1.1",
                "download": "http://gc.ccplay.com.cn/media/package/451/v11/application.apk",
                "download_count": 632051,
                "download_size": 24050691,
                "comment_count": 0,
                "comments_url": "http://gc.ccplay.com.cn/api/comments/?content_type=17&object_pk=447",
                "tags": [
                    "TD",
                    "\u5854\u9632",
                ],
                "category_name": "\u7834\u89e3\u6e38\u620f",
                "categories_names": [
                    "\u7834\u89e3\u6e38\u620f",
                ],
                "whatsnew": "",
                "summary": "",
                "description": "",
                "author": {
                    "url": "http://gc.ccplay.com.cn/api/authors/298/",
                    "name": "FT Games"
                },
                "released_datetime": "1383162567",
                "screenshots": [
                    {
                        "large": "http://gc.ccplay.com.cn/media/package/451/v11/screenshot/4.jpg.480x800_q85_upscale.jpg",
                        "preview": "http://gc.ccplay.com.cn/media/package/451/v11/screenshot/4.jpg.235x390_q85_upscale.jpg",
                        "rotate": "0"
                    },...
                ],
                "actions": {
                    "mark": "http://gc.ccplay.com.cn/api/bookmarks/451/"
                },
                "versions_url": "http://gc.ccplay.com.cn/api/packageversions/?package=451",
                "related_packages_url": "http://gc.ccplay.com.cn/api/packages/451/relatedpackages/"
            },
        ]

    应用详情结构见[软件详情](/api/packages/#packagedetailserializer)

    #### HTTP Response Status

    * 200 HTTP_200_OK
        * 获取成功
        * 返回各应用的详情信息列表
    * 404 HTTP_404_NOT_FOUND
        * 请求格式有错，或没有任何数据

    ----
    """

    serializer_class = PackageDetailSerializer
    filter_backends = (PackageIdsFilter, )

    model = Package

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        return self.queryset

    def resort_with_request(self, request, object_list):
        _ids = request.GET.get('ids')
        ids = [int(id.strip()) for id in _ids.split(',')]
        resorted = [None] * len(ids)
        for obj in object_list:
            index = ids.index(obj.pk)
            resorted[index] = obj
        return resorted

    @cache_response(key_func=PushListKeyConstructor())
    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        self.object_list = self.resort_with_request(request=request, object_list=self.object_list)

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)
