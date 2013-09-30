# -*- encoding=utf-8 -*-
import copy
from rest_framework import  mixins
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

class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'

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
    * `download_count`:下载量
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

    """
    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
                       filters.SearchFilter,
    )
    filter_fields = ('package_name', 'title',)
    ordering = ('title',
                'package_name',
                'updated_datetime',
                'released_datetime' )

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self) \
            .retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
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
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)

class PackageRankingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PackageSummarySerializer
    queryset = Package.objects.published().by_rankings_order()

#------------------------------------------------------------------
from taxonomy.models import Category, Topic, TopicalItem
from mobapi.serializers import ( CategoryDetailSerializer,
                                 CategorySummarySerializer,
                                 TopicSummarySerializer,
                                 TopicDetailWithPackageSerializer )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.as_root().all()
    serializer_class = CategorySummarySerializer
    lookup_field = 'slug'
    paginate_by = None

    @link()
    def packages(self, request, slug, *args, **kwargs):
        category =  generics.get_object_or_404(self.queryset, slug=slug)

        ViewSet = PackageViewSet
        queryset = category.packages.all()
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class, self.serializer_class = self.serializer_class, CategoryDetailSerializer
        origin_queryset, self.queryset = self.queryset, Category.objects.all()

        response = super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
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
    ordering = ('released_datetime',)

    def list(self, request, *args, **kwargs):
        #origin_queryset, self.queryset = self.queryset, self.queryset.as_root()
        origin_queryset, self.queryset = self.queryset, self.queryset.filter(parent=None)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        self.queryset = origin_queryset
        return res

    @link()
    def children(self, request, slug, *args, **kwargs):
        """子专区列表"""
        queryset = self.queryset.filter(slug=slug)
        topic =  generics.get_object_or_404(queryset, slug=slug)

        origin_queryset, self.queryset = self.queryset, self.queryset.filter(parent=topic)
        res = super(TopicViewSet, self).list(request, *args, **kwargs)
        return res

    @link()
    def items(self, request, slug, *args, **kwargs):
        topic =  generics.get_object_or_404(self.queryset, slug=slug)

        list_view = self._get_item_list_view(topic)
        return list_view(request, *args, **kwargs)

    def _get_item_list_view(self, topic):
        ViewSet = get_viewset_by_topic(topic)
        model = get_item_model_by_topic(topic)
        queryset = TopicalItem.objects.get_items_by_topic(topic, model)
        # FIXME 重构此处queryset，使之与ViewSet.queryset可以合并查询
        queryset = queryset.published()
        return ViewSet.as_view({'get':'list'}, queryset=queryset)

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
            data = {'detail': 'Not Allow without search parameter %{url}s/?place=slug'
                        .format(url=reverse('advertisement-list') ) }
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
        url =  "%s%s/?place=%s" % (host_url, '/api/advertisements', p.slug)
        a = '[%s](%s)'%(url, url, )
        contents.append( "\n * `%s`: %s %s" %( p.slug, p.help_text, a ))

    AdvertisementViewSet.__doc__ = AdvertisementViewSet.__doc__.format(apis="".join(contents))

from mobapi.serializers import AccountDetailSerializer
from mobapi.authentications import PlayerTokenAuthentication
from account.models import Player, Profile
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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
            raise ValidationError('password should not be empty')


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
            raise ValidationError(e)

        profile.save()
        return user

    def post(self, request, *args, **kwargs):
        try:
            queryparams = self.get_query_params(request.DATA)
            user = self.run_validate_and_save(queryparams)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.messages},
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
        return Response({'detail': 'sign out successful'}, status=status.HTTP_200_OK)

from django.utils.timezone import utc, datetime
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

def documentation_account_view(view):
    _link_mask = '* %s: [%s](%s)'
    _maps = (
        ('注册', '/api/accounts/signup/'),
        ('登陆', '/api/accounts/signin/'),
        ('注销', '/api/accounts/signout/'),
        ('账户信息', '/api/accounts/myprofile/'),
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
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
