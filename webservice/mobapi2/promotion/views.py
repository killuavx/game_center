# -*- coding: utf-8 -*-
import copy
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.timezone import now
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from promotion.models import Advertisement, Place, Recommend
from mobapi2.promotion.serializers import AdvertisementSerializer, RecommendSerializer
from mobapi2.decorators import default_cache_control


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

    model = Advertisement
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering = ('-relation_advertisement__ordering',)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.published().by_ordering()
        return self.queryset

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

        self.queryset = self.get_queryset().place_in(place)
        return super(AdvertisementViewSet, self).list(request, *args, **kwargs)


def documentation_advertisement_viewset():
    host_url = ''
    places = Place.objects.all()
    contents = list()
    for p in places:
        url = "%s%s/?place=%s" % (host_url, '/api/v2/advertisements', p.slug)
        a = '[%s](%s)' % (url, url, )
        contents.append("\n * `%s`: %s %s" % (p.slug, p.help_text, a))

    AdvertisementViewSet.__doc__ = AdvertisementViewSet.__doc__.format(
        apis="".join(contents))

from rest_framework import generics
from dateutil import parser as dateparser


class RecommendView(generics.RetrieveAPIView):
    """ 推荐接口

    接口访问基本形式:

        GET /api/v2/recommends/2014-09-01/

        {
            "title": "\u6697\u9ed1\u6218\u795e",
            "icon": "http://a.ccplay.com.cn:8080/media/package/94276/v9/240.png",
            "cover": "http://a.ccplay.com.cn:8080/media/recommend/2014/09/01/1527-29-500760/anheizhanshen.png",
            "summary": "\u6697\u9ed1\u6218\u795e",
            "content_url": "http://a.ccplay.com.cn:8080/api/v2/packages/94276/.api",
            "content_type": "package",
            "package_name": "com.ahzs.sy4399"
        }


    RecommendSerializer结构:

    * `title`: 推荐标题
    * `summary`: 推荐描述
    * `icon`: 应用icon的url
    * `cover`: 应用cover的url
    * `content_type`: 用于区别content_url所指内容类型, 现在只有package
    * `content_url`: 访问内容的url，content_type为package, 则content_url为package detail
    * `package_name`: 应用包名
    """

    model = Recommend
    serializer_class = RecommendSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering = ('-released_datetime', )
    lookup_field = None

    def get_queryset(self):
        if not self.queryset:
            self.queryset = self.model.objects.all()
        return self.queryset.filter(status=Recommend.STATUS.published)

    def get_object(self, queryset=None):
        try:
            return queryset.order_by('-released_datetime')[0]
        except IndexError:
            raise Http404

    def filter_date(self, queryset, *args, **kwargs):
        d = dateparser.parse(kwargs.get('date'))
        return queryset.published_with_date(d)

    @default_cache_control(max_age=3600)
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            #queryset = self.filter_date(queryset, *args, **kwargs)
        except ValueError:
            return Response(dict(detail='bad request'), status=status.HTTP_400_BAD_REQUEST)

        dt = now().astimezone()
        self.object = self.get_object(queryset)
        if not self.object.allow_show(dt):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class RecommendListView(generics.ListAPIView):
    """ 推荐列表接口

    接口访问基本形式:

        GET /api/v2/recommends/

        [{
            "title": "\u6697\u9ed1\u6218\u795e",
            "icon": "http://a.ccplay.com.cn:8080/media/package/94276/v9/240.png",
            "cover": "http://a.ccplay.com.cn:8080/media/recommend/2014/09/01/1527-29-500760/anheizhanshen.png",
            "summary": "\u6697\u9ed1\u6218\u795e",
            "content_url": "http://a.ccplay.com.cn:8080/api/v2/packages/94276/.api",
            "content_type": "package",
            "package_name": "com.ahzs.sy4399"
        },
        ...]


    RecommendSerializer结构:

    * `title`: 推荐标题
    * `summary`: 推荐描述
    * `icon`: 应用icon的url
    * `cover`: 应用cover的url
    * `content_type`: 用于区别content_url所指内容类型, 现在只有package
    * `content_url`: 访问内容的url，content_type为package, 则content_url为package detail
    * `package_name`: 应用包名
    """

    model = Recommend
    serializer_class = RecommendSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering = ('-released_datetime', )
    lookup_field = None
    paginate_by = None

    def get_queryset(self):
        if not self.queryset:
            self.queryset = self.model.objects.all()
        return self.queryset.filter(status=Recommend.STATUS.published)

    def filter_allow_show(self, queryset, dt):
        showed = []
        for recommend in queryset:
            if recommend.allow_show(dt):
                showed.append(recommend)
        return showed

    @default_cache_control(max_age=3600)
    def list(self, request, *args, **kwargs):
        self.get_queryset()
        self.object_list = self.filter_queryset(self.get_queryset())
        self.object_list = self.filter_allow_show(self.object_list, now())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data)
