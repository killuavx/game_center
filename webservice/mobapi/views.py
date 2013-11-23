# -*- encoding=utf-8 -*-
import copy

from rest_framework.settings import api_settings
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import (viewsets,
                            generics,
                            status,
                            filters)

from warehouse.models import Package, PackageVersion
from mobapi.warehouse.serializers.package import PackageSummarySerializer


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object_through_multiple_field(self, queryset):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

from mobapi.serializers import AccountDetailSerializer
from mobapi.authentications import PlayerTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from account.forms import mob as account_forms


def errors_flat_to_str(errors):
    messages = []
    for field, _messages in errors.items():
        messages.append(", ".join(_messages))
    return ", ".join(messages)


class AccountCreateView(generics.CreateAPIView):
    """ 账户注册

    ## 接口访问形式

        POST /api/accounts/signup/
        Content-Type:application/x-www-form-urlencoded
        ....

        username=yourname&phone=+86-021-12345678&email=your@email.com&password=asdf1235s

    ## 请求数据:

    1. `username`: 登陆用户名
    1. `phone`: 注册手机电话号码
    1. `email`: 注册邮箱
    1. `password`: 登陆密码

    ## 响应状态

    * 201 HTTP_201_CREATED
        * 创建成功, 返回用户profile信息,
        * {"username": "admin1", "email": "test@admin.com", "phone": "+86-021-123321123", "icon": null}
    * 400 HTTP_400_BAD_REQUEST
        * 错误请求，请求数据错误
        * {"detail": ["\u5177\u6709 \u7528\u6237\u540d \u7684 User \u5df2\u5b58\u5728\u3002"]}

    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = AccountDetailSerializer

    form_class = account_forms.SignupForm

    def create(self, request, *args, **kwargs):
        form = self.form_class(request.DATA, files=request.FILES)
        if form.is_valid():
            self.object = form.save()
            self.post_save(self.object, created=True)
            serializer = self.serializer_class(self.object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': errors_flat_to_str(form.errors)},
                            status=status.HTTP_400_BAD_REQUEST)



class AccountMyProfileView(generics.RetrieveAPIView):
    """ 账户信息

    ## 访问方式

        GET /api/accounts/myprofile/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 请求数据:

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应状态

    * 201 HTTP_200_OK
        * 创建成功, 返回用户profile信息,
        * {"username": "admin1", "email": "test@admin.com", "phone": "+86-021-123321123", "icon": null}
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization
    """
    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = AccountDetailSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountSignoutView(APIView):
    """ 注销接口

    ## 访问方式

        GET /api/accounts/signout/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应内容

    * 200 HTTP_200_OK
        * 登出成功
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    """

    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        request.auth.delete()
        request.auth = None
        return Response({'detail': 'sign out successful'},
                        status=status.HTTP_200_OK)


from django.utils.timezone import utc, datetime, now
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AccountAuthTokenView(ObtainAuthToken):
    """ 账户登陆

    ## 请求方式

        POST /api/accounts/signin/
        Content-Type:application/x-www-form-urlencoded
        ...

        username=your_name&password=asdf1235s

    ## 请求参数

       1. `username`: 登陆用户名、电话号码或电子邮箱
       1. `password`: 登陆密码

    ## 响应内容

    1. 200 HTTP_200_OK
        * 登陆成功
        * HTTP Response Content: {"token": "ee98b0f181d5ba43ec450008eca3f2a59e6dd9ff"}
        * `token`用于用户登陆后的相关接口操作，需要在请求的Http Header上添加 `Authorization: Token ee98b0f181d5ba43ec450008eca3f2a59e6dd9ff`
    2. 400 HTTP_400_BAD_REQUEST
        * 错误请求，请求数据错误

    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES




class AccountCommentPackageView(generics.ListAPIView):
    """ 已评论软件接口

    ## 访问方式

        GET /api/accounts/commented_packages/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应内容

    * 200 HTTP_200_OK
        * 获取成功
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    """

    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = PackageSummarySerializer
    queryset = Package.objects.published()

    def get(self, request, *args, **kwargs):
        user = request.user
        qs = Comment.objects.with_site().published().by_submit_order()
        version_ids = list(
            qs.filter(user=user).values_list('object_pk', flat=True))
        pkg_ids = PackageVersion.objects.published() \
            .filter(pk__in=version_ids).values_list('package__pk', flat=True)
        pkg_ids = list(pkg_ids)
        self.queryset = self.queryset.filter(pk__in=pkg_ids)

        return super(AccountCommentPackageView, self) \
            .get(request=request, *args, **kwargs)


def documentation_account_view(view):
    _link_mask = '* %s: [%s](%s)'
    _maps = (
        ('注册', '/api/accounts/signup/'),
        ('登陆', '/api/accounts/signin/'),
        ('注销', '/api/accounts/signout/'),
        ('账户信息', '/api/accounts/myprofile/'),
        ('评论软件列表', '/api/accounts/commented_packages/'),
    )
    apis = [
        _link_mask % (r[0], r[1], r[1] ) for r in _maps
    ]
    view.__doc__ += "\n"
    view.__doc__ += "## 相关接口"
    view.__doc__ += "\n"
    view.__doc__ += "\n".join(apis)
    view.__doc__ += '\n----'


documentation_account_view(AccountAuthTokenView)
documentation_account_view(AccountCreateView)
documentation_account_view(AccountSignoutView)
documentation_account_view(AccountMyProfileView)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.object['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import get_object_or_404


class DjangoDataFilterBackend(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.DATA, queryset=queryset).qs

        return queryset


class PackageBookmarkViewSet(viewsets.ModelViewSet):
    """ 账户收藏接口

    ### 必备请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/accounts/signin/](/api/accounts/signin/)，获得登陆`Token <Key>`

    ### 无效访问

    当请求收藏相关的接口时，未包含Authorization头，或无效的Token将得到如下的响应状态

    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    ----

    ## 收藏列表

    #### 访问方式

        GET /api/bookmarks/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功
        * 返回软件列表信息,没有则返回空results列表

    ----

    ## 添加收藏

    #### 访问方式

        POST /api/bookmarks/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        ...

        package_name=com.yourmark.packagename

    #### 响应内容

    * 201 HTTP_201_CREATED
        * 收藏成功
    * 400 HTTP_400_BAD_REQUEST
        * 请求错误
        * 请求数据无效

    ----

    ## 移除收藏

    收藏的url从软件信息中的`actions`.`mark`中获取

    #### 访问方式

        DETELE /api/bookmarks/3/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    #### 响应内容

    * 204 HTTP_204_NO_CONTENT
        * 无返回内容
    * 400 HTTP_400_BAD_REQUEST
        * 请求错误
        * 请求数据无效
    * 404 HTTP_404_NOT_FOUND
        * 找不到该收藏

    ----

    ## 检查是否已经收藏

    收藏的url从软件信息中的`actions`.`mark`中获取

    #### 访问方式

        HEAD /api/bookmarks/3/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    #### 响应内容

    * 200 HTTP_200_OK
        * 有该收藏
    * 404 HTTP_404_NOT_FOUND
        * 找不到该收藏

    ----

    """

    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer
    authentication_classes = (PlayerTokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    filter_backends = (
        DjangoDataFilterBackend,
        filters.DjangoFilterBackend,
    )
    filter_fields = (
        'package_name',
    )
    search_fields = tuple()

    def _prepare_queryset(self, request):
        self.queryset = self.queryset.filter(profile=request.user.profile)

    def list(self, request, *args, **kwargs):
        self._prepare_queryset(request)
        return super(PackageBookmarkViewSet, self) \
            .list(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            pass  # Deprecation warning

        obj = get_object_or_404(queryset)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.bookmarks.add(self.object)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        bookmarks = request.user.profile.bookmarks
        queryset, self.queryset = \
            self.queryset, bookmarks.filter(pk=kwargs.get('pk'))
        obj = self.get_object()
        bookmarks.remove(obj)
        self.queryset = queryset
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        bookmarks = request.user.profile.bookmarks
        queryset, self.queryset = \
            self.queryset, bookmarks.filter(pk=kwargs.get('pk'))
        obj = self.get_object()

        serializer = self.get_serializer(obj)
        self.queryset = queryset
        return Response(serializer.data, status=status.HTTP_200_OK)

#----------------------------------------------------------------
from django.contrib.contenttypes.models import ContentType


#----------------------------------------------------------------
from mobapi.serializers import CommentSerializer, CommentCreateSerializer
from comment.models import Comment
from django.core import exceptions
from django.conf import settings


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
    queryset = Comment.objects.published().with_site().by_submit_order()

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

#----------------------------------------------------------------
from mobapi.serializers import ClientPackageVersionSerializer
from clientapp.models import ClientPackageVersion


class SelfUpdateView(generics.RetrieveAPIView):
    """ 客户端自更新接口

    #### 访问方式

        GET /api/selfupdate

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
    queryset = ClientPackageVersion.objects.published()

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
