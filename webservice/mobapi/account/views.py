# -*- coding: utf-8 -*-
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from account.forms import mob as account_forms
from mobapi.authentications import PlayerTokenAuthentication
from mobapi.account.serializers import AccountDetailSerializer
from mobapi.warehouse.serializers.package import PackageSummarySerializer
from warehouse.models import Package, PackageVersion
from comment.models import Comment


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
documentation_account_view(AccountCommentPackageView)