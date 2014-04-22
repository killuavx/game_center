# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import serializers
from warehouse.models import PackageVersion, PackageVersionScreenshot
from mobapi.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi.rest_fields import factory_imageurl_field
from mobapi.helpers import (
    get_packageversion_comment_queryset,
    get_packageversion_comments_url)
from mobapi.warehouse.serializers.mixin import (
    PackageRelatedCategoryMixin,
    PackageActionsMixin,
    PackageRelatedVersionsMixin,
    PackageRelatedPackageUrlMixin)
from mobapi.warehouse.serializers.author import AuthorSummarySerializer
from mobapi.warehouse.serializers.helpers import (
    get_packageversion_download_url,
    get_packageversion_download_size)


class PackageVersionScreenshotSerializer(serializers.ModelSerializer):
    large = serializers.SerializerMethodField('get_large_url')
    preview = serializers.SerializerMethodField('get_preview_url')

    def get_preview_url(self, obj):
        try:
            return obj.image['middle'].url
        except:
            return ''

    def get_large_url(self, obj):
        try:
            return obj.image['large'].url
        except:
            return ''

    class Meta:
        model = PackageVersionScreenshot
        fields = ('large', 'preview', 'rotate')


class PackageVersionSerializer(serializers.ModelSerializer):

    entrytype = 'client'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    def get_version_download_url(self, obj):
        kwargs = dict()
        if hasattr(self, 'entrytype'):
            kwargs['entrytype'] = self.entrytype
        return get_packageversion_download_url(request=self.context.get('request'),
                                               version=obj,
                                               **kwargs)

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    def get_version_download_size(self, obj):
        return get_packageversion_download_size(obj)

    screenshots = PackageVersionScreenshotSerializer(many=True)

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    def get_version_comment_count(self, obj):
        version_cmt = get_packageversion_comment_queryset(obj)
        return version_cmt.count()

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    def get_version_comments_url(self, obj):
        url = get_packageversion_comments_url(obj)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    class Meta:
        model = PackageVersion
        fields = ('icon',
                  'cover',
                  'version_code',
                  'version_name',
                  'screenshots',
                  'whatsnew',
                  'download',
                  'download_count',
                  'download_size',
                  'comments_url',
                  'comment_count',
        )


class PackageVersionRelatedPackageMixin(PackageRelatedCategoryMixin,
                                        PackageActionsMixin,
                                        PackageRelatedVersionsMixin,
                                        PackageRelatedPackageUrlMixin,
                                        object):

    def get_main_category_name(self, obj):
        return super(PackageVersionRelatedPackageMixin, self) \
            .get_main_category_name(obj.package)

    def get_categories_names(self, obj):
        return super(PackageVersionRelatedPackageMixin, self) \
            .get_categories_names(obj.package)

    def get_author(self, obj):
        return AuthorSummarySerializer(obj.package.author,
                                       context=self.context).data

    def get_description(self, obj):
        return obj.package.description

    def get_summary(self, obj):
        return obj.package.summary

    def get_action_links(self, obj):
        return super(PackageVersionRelatedPackageMixin, self)\
            .get_action_links(obj.package)

    def get_version_count(self, obj):
        return super(PackageVersionRelatedPackageMixin, self)\
            .get_version_count(obj.package)

    def get_related_packages_url(self, obj):
        return super(PackageVersionRelatedPackageMixin, self)\
            .get_related_packages_url(obj.package)

    def get_title(self, obj):
        return obj.package.title

    def get_package_name(self, obj):
        return obj.package.package_name

    def get_versions_url(self, obj):
        return super(PackageVersionRelatedPackageMixin, self)\
            .get_versions_url(obj=obj.package)


class PackageVersionSummarySerializer(serializers.HyperlinkedModelSerializer):

    entrytype = 'client'

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    def get_version_download_url(self, obj):
        kwargs = dict()
        if hasattr(self, 'entrytype'):
            kwargs['entrytype'] = self.entrytype
        return get_packageversion_download_url(request=self.context.get('request'),
                                               version=obj,
                                               **kwargs)

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    def get_version_download_size(self, obj):
        return get_packageversion_download_size(obj)

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    def get_version_comment_count(self, obj):
        version_cmt = get_packageversion_comment_queryset(obj)
        return version_cmt.count()

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    def get_version_comments_url(self, obj):
        url = get_packageversion_comments_url(obj)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    class Meta:
        model = PackageVersion
        fields = ('url',
                  'icon',
                  'version_code',
                  'version_name',
                  'download',
                  'download_count',
                  'download_size',
                  'comments_url',
                  'comment_count',
                  'released_datetime')


class PackageVersionDetailSerializer(PackageVersionRelatedPackageMixin,
                                     serializers.HyperlinkedModelSerializer):

    entrytype = 'client'

    package_name = serializers.SerializerMethodField('get_package_name')

    title = serializers.SerializerMethodField('get_title')

    author = serializers.SerializerMethodField('get_author')

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    def get_version_download_url(self, obj):
        kwargs = dict()
        if hasattr(self, 'entrytype'):
            kwargs['entrytype'] = self.entrytype
        return get_packageversion_download_url(request=self.context.get('request'),
                                               version=obj,
                                               **kwargs)

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    def get_version_download_size(self, obj):
        return get_packageversion_download_size(obj)

    screenshots = PackageVersionScreenshotSerializer(many=True)

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    def get_version_comment_count(self, obj):
        version_cmt = get_packageversion_comment_queryset(obj)
        return version_cmt.count()

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    def get_version_comments_url(self, obj):
        url = get_packageversion_comments_url(obj)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')

    description = serializers.SerializerMethodField('get_description')

    summary = serializers.SerializerMethodField('get_summary')

    actions = serializers.SerializerMethodField('get_action_links')

    related_packages_url = serializers\
        .SerializerMethodField('get_related_packages_url')

    versions_url = serializers.SerializerMethodField('get_versions_url')

    def get_version_url(self, obj):
        request = self.context.get('request')
        uri = "%s?package=%d" % (reverse('packageversion-list'), obj.package.pk)
        if request:
            return request.build_absolute_uri(uri)
        return uri

    class Meta:
        model = PackageVersion
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
                  'category_name',
                  'categories_names',
                  'whatsnew',
                  'summary',
                  'description',
                  'author',
                  'screenshots',
                  'actions',
                  'versions_url',
                  'related_packages_url',
                  'released_datetime',
        )
