# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from analysis.serializers import EventSerializer
from analysis.documents.event import Event
from mobapi2.authentications import PlayerTokenAuthentication


class EventViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    ## 记录事件接口

    ### 可选登陆数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 可通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    #### 访问方式

        POST /api/events/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type:application/json

        {
            "imei": "4401023012500234",
            "eventtype": "activate",
            "entrytype": "client"
        }

    #### 提交信息

    * `imei`: 国际移动设备标识码 *
    * `eventtype`: 事件类型，可选值[activate, open, close, click]分别对应[激活, 打开, 关闭, 点击] *
    * `entrytype`: 进入类型，可选值[client, game]分别对应[市场客户端, 嵌入sdk的游戏] *
    * `package_name`: 游戏或客户端应用包名
    * `device`: 厂商设备号信息
    * `manufacturer`: 设备生产厂商
    * `tags`: 自定义标签，数组类型

    #### 响应内容

    * 201 HTTP_201_CREATED
        * 发布成功
        * 返回刚创建的信息
    * 400 HTTP_400_BAD_REQUEST
        * 坏请求
        * 返回错误信息
    """

    model = Event
    queryset = Event.objects
    serializer_class = EventSerializer
    permission_classes = ()
    authentication_classes = (PlayerTokenAuthentication, )

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        if instance is None and data:
            instance = self.model(**data)
        serializer = super(EventViewSet, self).get_serializer(instance=instance,
                                                              data=data,
                                                              files=files,
                                                              many=many,
                                                              partial=partial)
        request = serializer.context.get('request')
        if request and serializer.object:
            serializer.object.user = request.user
            if hasattr(request, 'get_client_ip'):
                serializer.object.client_ip = request.get_client_ip()
                serializer.object.domain = request.get_host()
        return serializer
