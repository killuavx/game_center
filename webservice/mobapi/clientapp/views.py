# -*- coding: utf-8 -*-
from rest_framework import generics, status, filters
from rest_framework.response import Response
from mobapi.clientapp.serializers import ClientPackageVersionSerializer
from clientapp.models import ClientPackageVersion


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
        if not self.queryset:
            self.queryset = ClientPackageVersion.objects
        return self.queryset.published()

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