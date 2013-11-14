# -*- encoding=utf-8 -*-
import copy
from rest_framework.settings import api_settings
from rest_framework import mixins
from warehouse.models import Package, Author
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework import (viewsets,
                            generics,
                            status,
                            filters)
from mobapi.serializers import (PackageSummarySerializer,
                                PackageDetailSerializer,
                                AuthorSerializer)


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


class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'


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


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.activated()
    serializer_class = AuthorSerializer

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.queryset, pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)


class PackageRankingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PackageSummarySerializer
    queryset = Package.objects.published().by_rankings_order()
    filter_backends = (PackageExcludeCategoryOfApplicationFilter, )

#------------------------------------------------------------------
from taxonomy.models import Category, Topic, TopicalItem
from mobapi.serializers import ( CategoryDetailSerializer,
                                 CategorySummarySerializer,
                                 TopicSummarySerializer,
                                 TopicDetailWithPackageSerializer )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ 分类接口

    ## 分类树接口

        GET /api/categories/

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功, 返回分类树状结构的列表数据

    ### 单个分类元素数据结构

    * `url`: 详细信息接口
    * `icon`: 图标地址
    * `name`: 分类名字
    * `slug`: 分类唯一标识的名字
    * `packages_url`: 分类软件列表接口
    * `parent`: 父级分类详细信息接口
    * `children`: 子级分裂列表

    ----

    ## 分类应用列表接口

        GET /api/topics/{slug}/packages/?page_size=10

    #### 请求信息

    * `{slug}`: 分类slug
    * `page_size`: 每页个数

    #### 响应内容

    * 200 HTTP_200_OK
        * 获取成功, 返回应用列表, 数据结构见[应用列表接口](/api/packages/)

    ----

    """
    queryset = Category.objects.as_root().showed()
    serializer_class = CategorySummarySerializer
    lookup_field = 'slug'
    paginate_by = None

    @link()
    def packages(self, request, slug, *args, **kwargs):
        queryset = Category.objects.published()
        category = generics.get_object_or_404(queryset, slug=slug)

        list_view = self.get_packages_list_view(request, category)
        return list_view(request, *args, **kwargs)

    def get_packages_list_view(self, request, category):
        ViewSet = PackageViewSet
        queryset = category.packages.all()
        queryset = queryset.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view

    def filter_packages_list_view(self, list_view, request, category):
        list_view.paginate_by = request.GET.get(
            api_settings.PAGINATE_BY_PARAM, api_settings.PAGINATE_BY)
        list_view.max_paginate_by = 50
        return list_view

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class, self.serializer_class = self.serializer_class, CategoryDetailSerializer
        origin_queryset, self.queryset = self.queryset, Category.objects.all()

        response = super(CategoryViewSet, self).retrieve(request, *args,
                                                         **kwargs)
        self.serializer_class = list_serializer_class
        self.queryset = origin_queryset
        return response


from mobapi.helpers import (get_item_model_by_topic,
                            get_viewset_by_topic)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """ 专区接口

    ## 接口访问基本形式:

    1. 专区详细信息:
        /api/topics/{slug}
    2. 子专区列表:
        /api/topics/{slug}/children
    3. 关联对象列表:
        /api/topics/{slug}/items

    ## 专区类型

    * 一级专区软件列表, `只有`items_url能有效访问关联软件列表

        * 精选推荐  slug:`home-recommend-game`

        * 网游专区  slug:`home-network-game`

        * 最新游戏  slug:`homebar-newest-game`

        * 大型游戏  slug:`homebar-big-game`

        * 中文游戏  slug:`homebar-cn-game`


    * 二级专区列表
        * 精选专辑, 通过访问对应的`*_url`，获得下一级的关联数据列表，
        从`*_url`获得关联对象列表的数据，
        再从author.packages_url/topic.items_url获得该级对象的软件列表

            slug:`spec-choice-topic`
            children_url: 子专区url, 类型Topic

        * 顶级开发商

            slug:`spec-top-author`
            item_url: 开发商列表url, 类型Author

    TODO 添加以上7个专区以及开发者和游戏数据
    """

    queryset = Topic.objects.published()
    serializer_class = TopicSummarySerializer
    lookup_field = 'slug'
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
    )
    filter_fields = ('name', 'slug',)
    ordering = ('released_datetime', )

    def list(self, request, *args, **kwargs):
        #origin_queryset, self.queryset = self.queryset, self.queryset.as_root()
        origin_queryset, self.queryset = self.queryset, self.queryset.filter(
            parent=None)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        return res

    @link()
    def children(self, request, slug, *args, **kwargs):
        """子专区列表"""
        queryset = self.queryset.filter(slug=slug)
        topic = generics.get_object_or_404(queryset, slug=slug)

        origin_queryset, self.queryset = \
            self.queryset, self.queryset.filter(parent=topic)
        self.ordering = ('ordering', )
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        return res

    @link()
    def items(self, request, slug, *args, **kwargs):
        topic = generics.get_object_or_404(self.queryset, slug=slug)

        list_view = self._get_item_list_view(topic)
        return list_view(request, *args, **kwargs)

    def _get_item_list_view(self, topic):
        ViewSet = get_viewset_by_topic(topic)
        model = get_item_model_by_topic(topic)
        queryset = TopicalItem.objects.get_items_by_topic(topic, model)
        # FIXME 重构此处queryset，使之与ViewSet.queryset可以合并查询
        # FIXME 重构此处，预先检查有无filter backend, OrderingFilter, 如果有OrderingFilter并有filter查询请求，则使用指定排序
        queryset = queryset.published()
        # ignore filter backend ordering
        # using queryset pass by TopicalItem.ordering,
        ViewSet.ordering = ()
        return ViewSet.as_view({'get': 'list'},
                               queryset=queryset)

    def retrieve(self, request, *args, **kwargs):
        origin_serializer_class, self.serializer_class = \
            self.serializer_class, TopicDetailWithPackageSerializer
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = origin_serializer_class
        return response

#------------------------------------------------------------------
from searcher.models import TipsWord
from mobapi.serializers import TipsWordSerializer


class TipsWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TipsWordSerializer
    queryset = TipsWord.objects.published()

#------------------------------------------------------------------
from promotion.models import Advertisement, Place
from mobapi.serializers import AdvertisementSerializer

from django.core.urlresolvers import reverse


class AdvertisementViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 广告接口

    接口访问基本形式:

    {apis}

    AdvertisementSerializer结构:

    * `title`: 广告标语, UI无体现则忽略
    * `cover`: 广告图片的url
    * `content_type`: 用于区别content_url所指内容类型, 现在只有package
    * `content_url`: 访问内容的url，content_type为package, 则content_url为package detail

    """

    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.published().by_ordering()

    def list(self, request, *args, **kwargs):
        querydict = copy.deepcopy(dict(request.GET))
        q = querydict.get('place')
        q = q.pop() if isinstance(q, list) else q
        if not q or not (q and q.strip()):
            data = {
                'detail': 'Not Allow without search parameter %{url}s/?place=slug'
                .format(url=reverse('advertisement-list'))}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        place = None
        try:
            place = Place.objects.get(slug=q)
        except Place.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.queryset = self.queryset.place_in(place)
        return super(AdvertisementViewSet, self).list(request, *args, **kwargs)


def documentation_advertisement_viewset():
    host_url = ''
    places = Place.objects.all()
    contents = list()
    for p in places:
        url = "%s%s/?place=%s" % (host_url, '/api/advertisements', p.slug)
        a = '[%s](%s)' % (url, url, )
        contents.append("\n * `%s`: %s %s" % ( p.slug, p.help_text, a ))

    AdvertisementViewSet.__doc__ = AdvertisementViewSet.__doc__.format(
        apis="".join(contents))


from mobapi.serializers import AccountDetailSerializer
from mobapi.authentications import PlayerTokenAuthentication
from account.models import Player, Profile
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.utils.translation import ugettext as _


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

    def get_query_param(self, query, name):
        return query.get(name)

    def get_query_params(self, attrs):
        attrs = dict(
            username=self.get_query_param(attrs, 'username'),
            password=self.get_query_param(attrs, 'password'),
            email=self.get_query_param(attrs, 'email'),
            phone=self.get_query_param(attrs, 'phone'),
        )
        return attrs

    def run_validate_and_save(self, attrs):
        user = Player(username=attrs.get('username'))

        if attrs.get('password'):
            user.set_password(attrs.get('password'))
        else:
            _mgs = [_('should not be empty')]
            raise ValidationError(dict(password=_mgs))

        user.full_clean()
        user.save()
        profile = Profile(user=user,
                          email=attrs.get('email'),
                          phone=attrs.get('phone'),
        )
        try:
            profile.full_clean(['user'])
        except ValidationError as e:
            user.delete()
            raise ValidationError(
                getattr(e, 'message_dict', False) or e.messages)

        profile.save()
        return user

    def prepare_validation_messages(self, e):

        mgs = list()
        if getattr(e, 'message_dict', False):
            for _key, _mgs in e.message_dict.items():
                mgs.append("%s %s" % (_key, _mgs
                if isinstance(_mgs, str) else ", ".join(_mgs)))
            return mgs

        if e.messages:
            mgs = e.messages

        return mgs

    def post(self, request, *args, **kwargs):
        try:
            queryparams = self.get_query_params(request.DATA)
            user = self.run_validate_and_save(queryparams)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            messages = self.prepare_validation_messages(e)
            return Response({'detail': ", ".join(messages)},
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
from rest_framework.settings import api_settings


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


from warehouse.models import PackageVersion


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
from rest_framework.parsers import JSONParser, FormParser
from mobapi.serializers import PackageUpdateSummarySerializer
from django.contrib.contenttypes.models import ContentType


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
