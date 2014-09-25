# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import DateField
from warehouse.models import Package
from mobapi2.warehouse.serializers.mixin import (
    PackageRelatedVersionsMixin,
    PackageRelatedLatestVersinoMixin,
    PackageRelatedCategoryMixin,
    PackageRelatedTagMin,
    PackageRelatedPackageUrlMixin,
    PackageActionsMixin,
    PackageRelatedAuthorMixin)
from mobapi2.serializers import HyperlinkedModelSerializer


class PackageSummarySerializer(PackageRelatedVersionsMixin,
                               PackageRelatedLatestVersinoMixin,
                               PackageRelatedCategoryMixin,
                               PackageRelatedTagMin,
                               PackageRelatedAuthorMixin,
                               PackageActionsMixin,
                               HyperlinkedModelSerializer):

    entrytype = 'client'

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    title = serializers.SerializerMethodField('get_latest_version_title')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    version_count = serializers.SerializerMethodField('get_version_count')
    download_type = serializers.SerializerMethodField('get_latest_version_download_type')
    download = serializers.SerializerMethodField(
        'get_latest_version_download')
    download_size = serializers.SerializerMethodField(
        'get_latest_version_download_size')
    comments_url = serializers.SerializerMethodField(
        'get_latest_version_comments_url')
    actions = serializers.SerializerMethodField('get_action_links')
    tags = serializers.SerializerMethodField('get_tags')
    star = serializers.SerializerMethodField('get_latest_version_star')

    author = serializers.SerializerMethodField('get_author')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    versions_url = serializers.SerializerMethodField('get_versions_url')
    flags = serializers.SerializerMethodField('get_latest_version_flags')

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'flags',
                  'tags',
                  'star',
                  'category_name',
                  'categories_names',
                  'version_count',
                  'summary',
                  'author',
                  'download_type',
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
                              PackageRelatedAuthorMixin,
                              PackageRelatedPackageUrlMixin,
                              HyperlinkedModelSerializer):

    entrytype = 'client'

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    title = serializers.SerializerMethodField('get_latest_version_title')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    whatsnew = serializers.SerializerMethodField('get_latest_version_whatsnew')
    screenshots = serializers.SerializerMethodField(
        'get_latest_version_screenshots')
    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')
    download_type = serializers.SerializerMethodField('get_latest_version_download_type')
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

    star = serializers.SerializerMethodField('get_latest_version_star')
    stars_good_rate = serializers.SerializerMethodField('get_latest_version_stars_good_rate')
    stars_medium_rate = serializers.SerializerMethodField('get_latest_version_stars_medium_rate')
    stars_low_rate = serializers.SerializerMethodField('get_latest_version_stars_low_rate')

    actions = serializers.SerializerMethodField('get_action_links')

    author = serializers.SerializerMethodField('get_author')

    related_packages_url = serializers.SerializerMethodField('get_related_packages_url')

    versions_url = serializers.SerializerMethodField('get_versions_url')

    supported_languages = serializers.SerializerMethodField('get_latest_version_supported_languages')

    has_award = serializers.SerializerMethodField('get_latest_version_has_award')

    award_coin = serializers.SerializerMethodField('get_latest_version_award_coin')

    flags = serializers.SerializerMethodField('get_latest_version_flags')

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'version_code',
                  'version_name',
                  'download_type',
                  'download',
                  'download_count',
                  'download_size',
                  'comment_count',
                  'comments_url',
                  'star',
                  'stars_good_rate',
                  'stars_medium_rate',
                  'stars_low_rate',
                  'flags',
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
                  'supported_languages',
                  'has_award',
                  'award_coin',
        )


class PackageUpdateSummarySerializer(PackageSummarySerializer):

    entrytype = 'client'

    title = serializers.SerializerMethodField('get_latest_version_title')
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


class PackageSummaryWithMyCommentSerializer(PackageSummarySerializer):
    entrytype = 'client'

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    cover = serializers.SerializerMethodField('get_latest_version_cover_url')
    title = serializers.SerializerMethodField('get_latest_version_title')
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
    star = serializers.SerializerMethodField('get_latest_version_star')

    author = serializers.SerializerMethodField('get_author')
    version_name = serializers.SerializerMethodField('get_latest_version_name')
    version_code = serializers.SerializerMethodField('get_latest_version_code')
    versions_url = serializers.SerializerMethodField('get_versions_url')

    def _get_comment(self, obj):
        request = self.context.get('request')
        qs = self.get_latest_version_comment(obj).filter(user=request.user)
        comment = qs[0]
        return comment

    comment = serializers.SerializerMethodField('get_comment')
    def get_comment(self, obj):
        try:
            comment = self._get_comment(obj)
            return comment.comment
        except (AttributeError, ObjectDoesNotExist) as e:
            return None

    submit_date = serializers.SerializerMethodField('get_comment_submit_date')
    def get_comment_submit_date(self, obj):
        try:
            comment = self._get_comment(obj)
            return DateField().to_native(comment.submit_date)
        except (AttributeError, ObjectDoesNotExist) as e:
            return None

    flags = serializers.SerializerMethodField('get_latest_version_flags')

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'flags',
                  'tags',
                  'star',
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
                  'comment',
                  'submit_date',
        )


