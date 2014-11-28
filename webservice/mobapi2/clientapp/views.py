# -*- coding: utf-8 -*-
from rest_framework import generics, status, filters, views
from rest_framework.decorators import link
from rest_framework.response import Response
from mobapi2.clientapp.serializers import ClientPackageVersionSerializer, LoadingCoverSerializer
from clientapp.models import ClientPackageVersion, LoadingCover
from rest_framework_extensions.cache.decorators import cache_response
from mobapi2 import cache_keyconstructors as ckc
from rest_framework import viewsets


class SelfUpdateView(generics.RetrieveAPIView):
    """ 客户端自更新接口

    #### 访问方式

        GET /api/selfupdate/?package_name=com.lion.market

    #### 请求参数
    * `package_name`: 更新包名，指定需要更新的包名（可选，默认为"com.lion.market"）

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功, 返回客户端最后版本数据
    * 204 HTTP_204_NO_CONTENT
        * 没有可更新的数据

    ### 返回数据结构

    * `package_name`: 客户端的包名
    * `version_code`: 最后版本的版本号
    * `version_name`: 最后版本的版本名
    * `whatsnew`: 更新描述内容
    * `summary`: 一句话摘要
    * `download`: 客户端下载地址
    * `download_size`: 文件字节大小

    ----
    """

    serializer_class = ClientPackageVersionSerializer
    model = ClientPackageVersion
    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filter_fields = ('package_name', )

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = ClientPackageVersion.objects.published()
        return self.queryset

    def get_object(self, queryset=None):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.latest_version()

    @cache_response(key_func=ckc.PackageFilterKeyConstructor())
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except ClientPackageVersion.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoadingCoverViewSet(viewsets.ViewSet):
    """ 客户端Loading封面接口

    #### 访问方式

    GET /api/v2/loadingcovers/active/?`package_name`=`com.lion.market`&`version_name`=`2.6`

    #### 请求参数
    * `package_name`: 客户端包名, "com.lion.market"
    * `version_name`: 客户端版本名, 如 1.2.1

    #### 响应内容

    * 200 HTTP_200_OK
        * 正常返回数据
    * 404 HTTP_404_NOT_FOUND
        * 无图片

    """

    queryset = None
    model = LoadingCover
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoadingCoverSerializer

    def get_queryset(self):
        if not self.queryset:
            self.queryset = self.model.objects.status_published().order_by('-_order')
        return self.queryset

    @link()
    @cache_response(key_func=ckc.PackageFilterKeyConstructor())
    def active(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        package_name = request.GET.get('package_name', 'com.lion.market')
        print(package_name)
        version_name = request.GET.get('version_name')
        try:
            cover = queryset.find_covers(package_name=package_name,
                                         version_name=version_name)[0]
        except IndexError:
            try:
                cover = queryset.find_covers(package_name)[0]
            except IndexError:
                return Response({'detail': 'Not Found'},
                                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cover)
        return Response(serializer.data)


from mobapi2.rest_clients import android_home_api


class HomePageViewSet(viewsets.ViewSet):
    """ 主页符合接口

    ### 虫虫精选页面

    #### 访问方式

        GET /api/v2/home/recommend/

        {
            advertisements: {
                next: null,
                results: [...],
                count: 5,
                previous: null
            },
            packages: {
                next: "http://android.ccplay.com.cn/api/v2/packages/?ordering=topical&topic_slug=home-recommend-game&page=2",
                results: [...],
                count: 20,
                previous: null
            }
        }

    ### 网络专区页面

    #### 访问方式

        GET /api/v2/home/network/

        {
            advertisements: {
                next: null,
                results: [...],
                count: 5,
                previous: null
            },
            packages: {
                next: "http://android.ccplay.com.cn/api/v2/packages/?ordering=topical&topic_slug=home-network-game&page=2",
                results: [...],
                count: 20,
                previous: null
            }
        }


    ### 响应数据

    * `advertisements`: 广告列表结构，见: [/api/v2/advertisements/](/api/v2/advertisements/)
    * `packages`: 软件列表结构，见: [/api/v2/packages/](/api/v2/packages/)


    """

    permission_classes = ()
    authentication_classes = ()

    def recommend(self, request, *args, **kwargs):
        return Response(dict(
            packages=android_home_api.recommend_list.data,
            advertisements=android_home_api.recommend_advs.data
        ))

    def network(self, request, *args, **kwargs):
        return Response(dict(
            packages=android_home_api.netgame_list.data,
            advertisements=android_home_api.netgame_advs.data
        ))
