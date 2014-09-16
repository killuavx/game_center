# -*- coding: utf-8 -*-
from rest_framework import generics, status, viewsets, filters, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from account.forms import mob as account_forms
from mobapi2.authentications import PlayerTokenAuthentication
from mobapi2.account.serializers import AccountDetailSerializer, MultiAppAuthTokenSerializer
from mobapi2.warehouse.serializers.package import PackageSummarySerializer
from mobapi2.warehouse.serializers.packageversion import PackageVersionWithMyCommentSummarySerializer
from warehouse.models import Package, PackageVersion
from comment.models import Comment
from mobapi2.account.serializers import *


import logging
logger = logging.getLogger('scripts')


def errors_flat_to_str(errors):
    messages = []
    for field, _messages in errors.items():
        messages.append(", ".join(_messages))
    return ", ".join(messages)


class AccountCreateView(generics.CreateAPIView):
    """ 账户注册

    ## 接口访问形式

        POST /api/v2/accounts/signup/
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
    serializer_class = AccountProfileSignupSerizlizer

    form_class = account_forms.SignupForm

    def create(self, request, *args, **kwargs):
        form = self.form_class(request.DATA, files=request.FILES)
        if form.is_valid():
            user = form.save()
            self.object = user.profile
            self.post_save(self.object, created=True)
            serializer = self.serializer_class(self.object)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response({'detail': errors_flat_to_str(form.errors)},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountDeviceCreateView(generics.CreateAPIView):
    """ 设备账户登陆

    ## 接口访问形式

        POST /api/v2/accounts/signup/device
        Content-Type:application/x-www-form-urlencoded
        ....

        imei=3S355D6F6A7A7K88Z8CL6ADFK

    ## 请求数据:

    1. `imei`: 设备国际标识码

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

    form_class = account_forms.DeviceAnonymousSignupForm
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


class AccountMyProfileView(mixins.UpdateModelMixin, generics.RetrieveAPIView):
    """ 账户信息

    ## 获取账户信息

        GET /api/v2/accounts/myprofile/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 修改账户信息

        POST /api/v2/accounts/myprofile/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

        email=test@test.com&sex=male

    ## 上传头像图片

        POST /api/v2/accounts/myprofile/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: multipart/form-data; boundary=---------------------------11535082321677973755949647881
        Content-Length: 35856

        -----------------------------11535082321677973755949647881
        Content-Disposition: form-data; name="icon"; filename="aboutme.icon.png"
        Content-Type: image/png

        .PNG
        ....
        ...


    ## 请求数据:

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应状态

    * 200 HTTP_200_OK
        * 返回用户profile信息,
        * {"username": "admin1", "email": "test@admin.com", "phone": "+86-021-123321123", "icon": null, ...}
    * 400 HTTP_400_BAD_REQUEST
        * 编辑用户信息格式有误
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization
    """
    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = AccountProfileStatsSerializer

    def get_object(self, queryset=None):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        """
        update profile basic infomation
        """
        partial = kwargs.pop('partial', True)
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)
        created = False
        save_kwargs = {'force_update': True}
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(**save_kwargs)
            self.post_save(self.object, created=created)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


from django.contrib.auth.forms import PasswordChangeForm


class AccountChangePasswordView(APIView):
    """ 更改密码接口

    ## 访问方式

        POST /api/v2/accounts/newpassword/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

        new_password=123123&old_password=abcdefg

    ## 请求数据

    1. `new_password`: 新密码
    2. `old_password`: 老密码确认

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

    ## 响应内容

    * 200 HTTP_200_OK
        * 修改成功
    * 400 HTTP_400_BAD_REQUEST
        * 错误请求参数
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    """

    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        new_password = request.DATA.get('new_password')
        data = dict(
            old_password=request.DATA.get('old_password'),
            new_password1=new_password,
            new_password2=new_password,
        )
        chpass = PasswordChangeForm(user=request.user, data=data)
        if chpass.is_valid():
            chpass.save()
            response = Response({'detail': 'ok'}, status=status.HTTP_200_OK)
        else:
            response = Response(chpass.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class AccountSignoutView(APIView):
    """ 注销接口

    ## 访问方式

        GET /api/accounts/signout/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

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


class AccountAuthTokenView(ObtainAuthToken):
    """ 账户登陆

    ## 请求方式

        POST /api/v2/accounts/signin/
        Content-Type:application/x-www-form-urlencoded
        ...

        username=your_name&password=asdf1235s

    ## 请求参数

       1. `username`: 登陆用户名、电话号码或电子邮箱
       1. `password`: 登陆密码
       1. `app`: 指定登陆平台, 指定参数为bbs, 则以bbs方式登陆，未传值则以默认港式登陆

    ## 响应内容

    1. 200 HTTP_200_OK
        * 登陆成功
        * HTTP Response Content: {"token": "ee98b0f181d5ba43ec450008eca3f2a59e6dd9ff"}
        * `token`用于用户登陆后的相关接口操作，需要在请求的Http Header上添加 `Authorization: Token ee98b0f181d5ba43ec450008eca3f2a59e6dd9ff`
    2. 400 HTTP_400_BAD_REQUEST
        * 错误请求，请求数据错误

    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = MultiAppAuthTokenSerializer
    serializer_class_myprofile = AccountProfileSigninSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            myprofile_serializer = self.serializer_class_myprofile(
                serializer.object['user'].profile)
            return Response(myprofile_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCommentedPackageVersionFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user = request.user
        qs = Comment.objects.for_model(PackageVersion).visible().by_submit_order()
        version_ids = list(qs.filter(user=user).values_list('object_pk', flat=True))
        if not version_ids:
            return queryset.none()
        return queryset.filter(pk__in=version_ids)


class AccountCommentPackageView(generics.ListAPIView):
    """ 已评论软件接口

    ## 访问方式

        GET /api/v2/accounts/commented_packages/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    ## 请求数据

    * `HTTP Header`: Authorization: Token `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`,
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

    ## 列表软件结构

    * 响应内容跟一般软件接口结构基本相同, 参考[/api/v2/packages/](PackageSummarySerializer)
    * 新增字段
        * `comment`: 评论内容
        * `submit_date`: 发表时间, 时间戳(秒)



    ## 响应内容

    * 200 HTTP_200_OK
        * 获取成功
    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    """

    authentication_classes = (PlayerTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = PackageVersionWithMyCommentSummarySerializer
    model = PackageVersion
    filter_backends = (
        MyCommentedPackageVersionFilter,
    )

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published()
        return self.queryset


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
    * 通过登陆接口 [/api/v2/accounts/signin/](/api/v2/accounts/signin/)，获得登陆`Token <Key>`

    ### 无效访问

    当请求收藏相关的接口时，未包含Authorization头，或无效的Token将得到如下的响应状态

    * 401 HTTP_401_UNAUTHORIZED
        * 未登陆
        * 无效的HTTP Header: Authorization

    ----

    ## 收藏列表

    #### 访问方式

        GET /api/v2/bookmarks/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功
        * 返回软件列表信息,没有则返回空results列表

    ----

    ## 添加收藏

    #### 访问方式

        POST /api/v2/bookmarks/
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

        DETELE /api/v2/bookmarks/3/
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

        HEAD /api/v2/bookmarks/3/
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    #### 响应内容

    * 200 HTTP_200_OK
        * 有该收藏
    * 404 HTTP_404_NOT_FOUND
        * 找不到该收藏

    ----

    """

    model = Package
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

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Package.objects.published()
        return self.queryset

    def _prepare_queryset(self, request):
        self.queryset = self.get_queryset().filter(profile=request.user.profile)

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


def documentation_account_view(view):
    _link_mask = '* %s: [%s](%s)'
    _maps = (
        ('注册', '/api/v2/accounts/signup/'),
        ('登陆', '/api/v2/accounts/signin/'),
        ('注销', '/api/v2/accounts/signout/'),
        ('账户信息', '/api/v2/accounts/myprofile/'),
        ('更改密码', '/api/v2/accounts/newpassword/'),
        ('收藏', '/api/v2/bookmarks/'),
        ('评论软件列表', '/api/v2/accounts/commented_packages/'),
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
documentation_account_view(AccountCommentPackageView)
documentation_account_view(PackageBookmarkViewSet)
documentation_account_view(AccountChangePasswordView)

"""
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
"""

