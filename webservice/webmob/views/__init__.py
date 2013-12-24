# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from warehouse.models import Package, Author
from mobapi.warehouse.views.package import (
    PackageViewSet as PackageRestViewSet,
    PackageSearchViewSet as PackageSearchRestViewSet
)
from mobapi.searcher.views import TipsWordViewSet
from mobapi.searcher.serializers import TipsWordSerializer

from mobapi.taxonomy.views.topic import TopicViewSet as TopicRestViewSet
from taxonomy.models import Topic

from clientapp.models import ClientPackageVersion

from rest_framework import serializers
from rest_framework import status
from mobapi.warehouse.serializers.mixin import (
    PackageActionsMixin,
    PackageRelatedTagMin,
    PackageRelatedCategoryMixin,
    PackageRelatedLatestVersinoMixin,
    PackageRelatedVersionsMixin,
    PackageRelatedPackageUrlMixin
)


class AuthorSummarySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='pk')

    class Meta:
        model = Author
        fields = (
            'name',
            'id',
        )


class PackageDetailSerializer(PackageRelatedLatestVersinoMixin,
                              PackageRelatedVersionsMixin,
                              PackageRelatedCategoryMixin,
                              PackageRelatedTagMin,
                              PackageActionsMixin,
                              PackageRelatedPackageUrlMixin,
                              serializers.ModelSerializer):

    id = serializers.IntegerField(source='pk')
    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    whatsnew = serializers.SerializerMethodField('get_latest_version_whatsnew')
    screenshots = serializers.SerializerMethodField(
        'get_latest_version_screenshots')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    download = serializers.SerializerMethodField('get_latest_version_download')
    download_count = serializers.SerializerMethodField(
        'get_latest_version_download_count')
    download_size = serializers.SerializerMethodField(
        'get_latest_version_download_size')
    tags = serializers.SerializerMethodField('get_tags')
    author = AuthorSummarySerializer()
    related_packages_url = serializers.SerializerMethodField('get_related_packages_url')
    versions_url = serializers.SerializerMethodField('get_versions_url')

    class Meta:
        model = Package
        fields = ('id',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'version_code',
                  'version_name',
                  'download',
                  'download_count',
                  'download_size',
                  'tags',
                  'category_name',
                  'categories_names',
                  'whatsnew',
                  'summary',
                  'description',
                  'author',
                  'released_datetime',
                  'screenshots',
                  'versions_url',
        )


class PackageSummarySerializer(PackageRelatedVersionsMixin,
                              PackageRelatedLatestVersinoMixin,
                              PackageRelatedCategoryMixin,
                              PackageRelatedTagMin,
                              PackageActionsMixin,
                              serializers.ModelSerializer):

    id = serializers.IntegerField(source='pk')
    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    version_count = serializers.SerializerMethodField('get_version_count')
    download = serializers.SerializerMethodField('get_latest_version_download')
    download_size = serializers.SerializerMethodField(
        'get_latest_version_download_size')
    comments_url = serializers.SerializerMethodField(
        'get_latest_version_comments_url')
    actions = serializers.SerializerMethodField('get_action_links')
    tags = serializers.SerializerMethodField('get_tags')
    author = AuthorSummarySerializer()
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    versions_url = serializers.SerializerMethodField('get_versions_url')

    class Meta:
        model = Package
        fields = ('id',
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
                  'download',
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
    serializer_class_detail = PackageDetailSerializer
    filter_fields = ('package_name', 'title',
                     'author',
                     'categories',
                     'categories__name',
                     'categories__slug')
    ordering = ('-released_datetime',
                '-updated_datetime',
                'title',
                'package_name'
    )


class PackageSearchViewSet(PackageSearchRestViewSet):
    serializer_class = PackageSummarySerializer
    serializer_class_detail = PackageDetailSerializer
    search_fields = ('title',
                     'tags_text',
                     'package_name',
                     'categories')


def home(request, *args, **kwargs):
    slug = 'home-recommend-game'
    topic = get_object_or_404(Topic, slug=slug)
    queryset = TopicRestViewSet.item_list_view_queryset(topic)
    ViewSet = TopicRestViewSet.item_list_view(topic)
    ViewSet.serializer_class = PackageSummarySerializer
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
    if response.status_code is not status.HTTP_200_OK:
        return HttpResponseNotFound('Not found')
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


def client_latest_download(request, *args, **kwargs):
    try:
        clientapp = ClientPackageVersion.objects.published().latest_version()
    except ClientPackageVersion.DoesNotExist:
        return HttpResponseNotFound('No Content')

    if clientapp.download:
        return HttpResponseRedirect(clientapp.download.url)

    return HttpResponseNotFound('No Package')


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

