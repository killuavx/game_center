# -*- coding: utf-8 -*-
import copy
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.utils.timezone import now
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from mobapi.authentications import PlayerTokenAuthentication
from mobapi.comment.serializers import CommentSerializer, CommentCreateSerializer
from comment.models import Comment

class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """ 评论接口


    ----

    ## 评论列表接口

    #### 访问方式

    具体的评论列表接口见 应用详情接口[例子](/api/packages/100)里的comments_url

        GET /api/comments/?content_type=23&object_pk=120

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功
        * 评论列表,没有评论返回空results列表
    * 404 HTTP_404_NOT_FOUND
        * 找不到这款应用

    ### 评论列表结构

    * `user_name`: 发表评论的用户名"admin",
    * `user_icon`: 用户的icon图片地址, 没有则null,
    * `comment`: 评论的内容,
    * `submit_date`: 发表的时间,格式是时间戳,如"1382392569"

    ----

    ## 发表评论接口

    ### 必备请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    #### 访问方式

    具体的评论列表接口见 应用详情接口[例子](/api/packages/100)里的comments_url

        POST /api/comments/?content_type=23&object_pk=120
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type:application/x-www-form-urlencoded

        comment=great%20job

    #### 响应内容

    * 201 HTTP_201_CREATED
        * 发表评论成功
        * 返回刚创建的评论信息
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization
    * 404 HTTP_404_NOT_FOUND
        * 找不到这款应用

    ### 新创建的评论数据结构

    * `user_name`: 发表评论的用户名"admin",
    * `user_icon`: 用户的icon图片地址, 没有则null,
    * `comment`: 评论的内容,
    * `submit_date`: 发表的时间,格式是时间戳,如"1382392569"

    """

    authentication_classes = (PlayerTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.published().by_submit_order()

    def check_paramters(self, querydict):
        ct = 'content_type'
        if ct not in querydict or not querydict.get(ct):
            return False

        opk = 'object_pk'
        if opk not in querydict or not querydict.get(opk):
            return False

        return {'content_type_id': int(querydict.get(ct)),
                opk: int(querydict.get(opk))}

    def get_content_object(self, params):
        content_type = ContentType.objects.get_for_id(
            params.get('content_type_id'))
        content_object = content_type.get_object_for_this_type(
            pk=params.get('object_pk'))
        return content_object

    def get_queryset(self):
        return Comment.objects.for_model(self.content_object) \
            .published().with_site().by_submit_order()

    def list(self, request, *args, **kwargs):
        params = self.check_paramters(copy.deepcopy(request.GET))
        bad = Response({'detail': 'Bad Request'},
                       status=status.HTTP_400_BAD_REQUEST)
        if not params:
            return bad

        try:
            self.content_object = self.get_content_object(params)
        except exceptions.ObjectDoesNotExist:
            return bad

        return super(CommentViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        params = self.check_paramters(copy.deepcopy(request.GET))
        bad = Response({'detail': 'Bad Request'},
                       status=status.HTTP_400_BAD_REQUEST)
        if not params:
            return bad

        try:
            content_object = self.get_content_object(params)
        except exceptions.ObjectDoesNotExist:
            return bad

        serializer_class, self.serializer_class = \
            self.serializer_class, CommentCreateSerializer
        response = super(CommentViewSet, self).create(request, *args, **kwargs)
        self.serializer_class = serializer_class

        if response.status_code == status.HTTP_201_CREATED:
            serializer = self.serializer_class(self.object)
            response.data = serializer.data
        return response

    def pre_save(self, obj):
        if not obj.ip_address:
            obj.ip_adress = self.request.get_client_ip()
        return obj

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        # create data
        if not instance and data:
            queryparams = copy.deepcopy(self.request.QUERY_PARAMS)
            params = self.check_paramters(queryparams)
            data = copy.deepcopy(data)
            data.setdefault('submit_date', now())
            data.setdefault('site', settings.SITE_ID)
            data.setdefault('user', self.request.user.pk)
            data.setdefault('user_name', self.request.user.username)
            data.setdefault('user_email', self.request.user.profile.email)
            data.setdefault('content_type', params.get('content_type_id'))
            data.setdefault('object_pk', params.get('object_pk'))

        return super(CommentViewSet, self).get_serializer(instance, data,
                                                          files, many, partial)

