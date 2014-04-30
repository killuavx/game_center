# -*- coding: utf-8 -*-
from rest_framework import generics, status, filters, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mobapi2.clientapp.serializers import ClientPackageVersionSerializer
from clientapp.models import ClientPackageVersion, LoadingCover


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

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except ClientPackageVersion.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoadingCoverView(views.APIView):
    """ 客户端自更新接口

    #### 访问方式

    GET /api/v2/loadingcovers/`package_name`/`version_name`

    #### 请求参数
    * `package_name`: 客户端包名, "com.lion.market"
    * `version_name`: 客户端版本名, 如 1.2.1

    #### 响应内容

    * 302 HTTP_302_FOUND
    * 重定向图片
    * 404 HTTP_404_NOT_FOUND
    * 无图片

    """

    permission_classes = ()

    def get(self, request, package_name, version_name=None, *args, **kwargs):
        qs = LoadingCover.objects.published().order_by('-_order')
        q = qs.find_covers(package_name, version_name)
        try:
            cover = qs.find_covers(package_name, version_name)[0]
        except IndexError:
            try:
                cover = qs.find_covers(package_name)[0]
            except IndexError:
                return Response({'detail': 'Not Found'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'title': cover.title},
                        headers=dict(Location=cover.image.url),
                        status=status.HTTP_302_FOUND)

