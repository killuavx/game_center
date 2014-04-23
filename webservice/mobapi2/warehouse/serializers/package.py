# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package
from mobapi2.warehouse.serializers.mixin import (
    PackageRelatedVersionsMixin,
    PackageRelatedLatestVersinoMixin,
    PackageRelatedCategoryMixin,
    PackageRelatedTagMin,
    PackageRelatedPackageUrlMixin,
    PackageActionsMixin,
)
from mobapi.warehouse.serializers.author import AuthorSummarySerializer


class PackageSummarySerializer(PackageRelatedVersionsMixin,
                               PackageRelatedLatestVersinoMixin,
                               PackageRelatedCategoryMixin,
                               PackageRelatedTagMin,
                               PackageActionsMixin,
                               serializers.HyperlinkedModelSerializer):

    entrytype = 'client'

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    version_count = serializers.SerializerMethodField('get_version_count')
    download = serializers.SerializerMethodField(
        'get_latest_version_download')
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
        fields = ('url',
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


class PackageDetailSerializer(PackageRelatedLatestVersinoMixin,
                              PackageRelatedVersionsMixin,
                              PackageRelatedCategoryMixin,
                              PackageRelatedTagMin,
                              PackageActionsMixin,
                              PackageRelatedPackageUrlMixin,
                              serializers.HyperlinkedModelSerializer):

    entrytype = 'client'

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
    comment_count = serializers.SerializerMethodField(
        'get_latest_version_comment_count')
    comments_url = serializers.SerializerMethodField(
        'get_latest_version_comments_url')
    tags = serializers.SerializerMethodField('get_tags')


    actions = serializers.SerializerMethodField('get_action_links')

    author = AuthorSummarySerializer()

    related_packages_url = serializers.SerializerMethodField('get_related_packages_url')

    versions_url = serializers.SerializerMethodField('get_versions_url')

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'version_code',
                  'version_name',
                  'download',
                  'download_count',
                  'download_size',
                  'comment_count',
                  'comments_url',
                  'tags',
                  'category_name',
                  'categories_names',
                  'whatsnew',
                  'summary',
                  'description',
                  'author',
                  'released_datetime',
                  'screenshots',
                  'actions',
                  'versions_url',
                  'related_packages_url',
        )


class PackageUpdateSummarySerializer(PackageSummarySerializer):

    entrytype = 'client'

    version_code = serializers.SerializerMethodField('get_latest_version_code')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    download = serializers.SerializerMethodField('get_latest_version_download')
    download_size = serializers. \
        SerializerMethodField('get_latest_version_download_size')
    is_updatable = serializers.SerializerMethodField('get_is_updatable')

    def get_is_updatable(self, obj):
        if getattr(obj, 'update_info', None) \
            and obj.update_info.get('version_code') is None:
            return False
        return self.get_latest_version_code(obj) > obj.update_info. \
            get('version_code')

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'package_name',
                  'title',
                  'download',
                  'download_size',
                  'version_code',
                  'version_name',
                  'released_datetime',
                  'actions',
                  'is_updatable',
        )

