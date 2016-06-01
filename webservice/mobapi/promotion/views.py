# -*- coding: utf-8 -*-
import copy
from django.core.urlresolvers import reverse
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from promotion.models import Advertisement, Place
from mobapi.promotion.serializers import AdvertisementSerializer


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
        url = "%s%s/?place=%s" % (host_url, '/api/advertisements', p.slug)
        a = '[%s](%s)' % (url, url, )
        contents.append("\n * `%s`: %s %s" % (p.slug, p.help_text, a))

    AdvertisementViewSet.__doc__ = AdvertisementViewSet.__doc__.format(
        apis="".join(contents))