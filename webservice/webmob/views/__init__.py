# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from warehouse.models import Package
from mobapi.warehouse.serializers.package import (
    PackageSummarySerializer as PackageSummaryRestSerializer
)
from mobapi.warehouse.views.package import (
    PackageViewSet as PackageRestViewSet,
    PackageSearchViewSet as PackageSearchRestViewSet
)
from mobapi.searcher.views import TipsWordViewSet
from mobapi.searcher.serializers import TipsWordSerializer

from mobapi.taxonomy.views.topic import TopicViewSet as TopicRestViewSet
from taxonomy.models import Topic

from rest_framework import serializers


class PackageSummarySerializer(PackageSummaryRestSerializer):

    id = serializers.IntegerField(source='pk')

    class Meta:
        model = Package
        fields = ('url',
                  'id',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'tags',
                  'category_name',
                  'categories_names',
                  'version_count',
                  'summary',
                  'author',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  'actions',
                  'version_name',
                  'version_code',
                  'versions_url',
        )


class PackageViewSet(PackageRestViewSet):

    serializer_class = PackageSummarySerializer
    filter_fields = ('package_name', 'title',
                     'categories',
                     'categories__name',
                     'categories__slug')
    ordering = ('-released_datetime',
                '-updated_datetime',
                'title',
                'package_name'
    )


class PackageSearchViewSet(PackageSearchRestViewSet):
    search_fields = ('title',
                     'tags_text',
                     'package_name',
                     'categories')


def home(request, *args, **kwargs):
    slug = 'home-recommend-game'
    topic = get_object_or_404(Topic, slug=slug)
    queryset = TopicRestViewSet.item_list_view_queryset(topic)
    ViewSet = TopicRestViewSet.item_list_view(topic)
    ListView = ViewSet.as_view({'get': 'list'}, queryset=queryset.published())
    response = ListView(request, *args, **kwargs)
    return render(request, 'webmob/home.haml',
                  response.data,
                  status=response.status_code)


def packages(request, *args, **kwargs):
    ListView = PackageViewSet.as_view(actions={'get': 'list'})
    response = ListView(request, *args, **kwargs)
    return render(request, 'webmob/home.haml', response.data)


def packagedetail(request, *args, **kwargs):
    ListView = PackageViewSet.as_view(actions={'get': 'retrieve'})
    response = ListView(request, *args, **kwargs)
    return render(request, 'webmob/package-detail.haml', response.data)


def searches(request, *args, **kwargs):
    ListView = PackageSearchViewSet.as_view(actions={'get': 'list'})
    response = ListView(request, *args, **kwargs)
    data = response.data

    tipswords_qs = TipsWordViewSet.queryset.all()[:10]
    tipswords_list = TipsWordSerializer(list(tipswords_qs), many=True,
                                            context=dict(request=request)).data
    if tipswords_list:
        data.update(dict(tipswords=tipswords_list))

    return render(request, 'webmob/search.haml', data)


class TopicViewSet(TopicRestViewSet):

    def list(self, request, *args, **kwargs):
        response = super(TopicViewSet, self).list(request, *args, **kwargs)
        return render(request, 'webmob/topic-list.haml',
                      response.data,
                      status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        response = super(TopicViewSet, self).retrieve(request, *args, **kwargs)
        return render(request, 'webmob/topic-.haml',
                      response.data,
                      status=response.status_code)

    def items(self, request, slug, *args, **kwargs):
        response = super(TopicViewSet, self).items(request, *args, **kwargs)
        return render(request, 'webmob/topic.items.haml',
                      response.data,
                      status=response.status_code)

    def children(self, request, slug, *args, **kwargs):
        response = super(TopicViewSet, self).items(request, *args, **kwargs)
        return render(request, 'webmob/topic.children.haml',
                      response.data,
                      status=response.status_code)

