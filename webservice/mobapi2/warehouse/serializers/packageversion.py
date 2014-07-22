# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from rest_framework import serializers
from rest_framework.fields import DateField
from warehouse.models import PackageVersion, PackageVersionScreenshot
from mobapi2.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE
from mobapi2.rest_fields import factory_imageurl_field
from mobapi2.helpers import (
    get_packageversion_comment_queryset,
    get_packageversion_comments_url, get_object_star, get_object_stars_rate)
from mobapi2.warehouse.serializers.mixin import (
    PackageRelatedCategoryMixin,
    PackageRelatedTagMin,
    PackageActionsMixin,
    PackageRelatedVersionsMixin,
    PackageRelatedPackageUrlMixin)
from mobapi2.warehouse.serializers.helpers import (
    get_packageversion_download_url,
    get_packageversion_download_size,
    get_packageversion_supported_languages)
from mobapi2.serializers import ModelSerializer,HyperlinkedModelSerializer


class PackageVersionScreenshotSerializer(ModelSerializer):
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


class PackageVersionSerializer(ModelSerializer):

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
        url = get_packageversion_comments_url(obj, router=self.opts.router)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    star = serializers.SerializerMethodField('get_star')

    def get_star(self, obj):
        return get_object_star(obj)

    class Meta:
        model = PackageVersion
        fields = ('icon',
                  'cover',
                  'version_code',
                  'version_name',
                  'screenshots',
                  'whatsnew',
                  'star',
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
        from mobapi2.warehouse.serializers.author import AuthorSummarySerializer
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


class PackageVersionSummarySerializer(HyperlinkedModelSerializer):

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
        url = get_packageversion_comments_url(obj, self.opts.router)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    star = serializers.SerializerMethodField('get_star')

    def get_star(self, obj):
        return get_object_star(obj)

    class Meta:
        model = PackageVersion
        fields = ('url',
                  'icon',
                  'version_code',
                  'version_name',
                  'star',
                  'download',
                  'download_count',
                  'download_size',
                  'comments_url',
                  'comment_count',
                  'released_datetime')


class PackageVersionDetailSerializer(PackageVersionRelatedPackageMixin,
                                     HyperlinkedModelSerializer):

    entrytype = 'client'

    package_name = serializers.SerializerMethodField('get_package_name')

    title = serializers.CharField(source='subtitle')

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
        url = get_packageversion_comments_url(obj, router=self.opts.router)
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
        view_name = self.opts.router.get_base_name('packageversion-list')
        uri = "%s?package=%d" % (reverse(view_name), obj.package.pk)
        if request:
            return request.build_absolute_uri(uri)
        return uri

    star = serializers.SerializerMethodField('get_star')

    def get_star(self, obj):
        return get_object_star(obj)

    stars_good_rate = serializers.SerializerMethodField('get_stars_good_rate')
    def get_stars_good_rate(self, obj):
        return get_object_stars_rate(obj, 'good')

    stars_medium_rate = serializers.SerializerMethodField('get_stars_medium_rate')
    def get_stars_medium_rate(self, obj):
        return get_object_stars_rate(obj, 'medium')

    stars_low_rate = serializers.SerializerMethodField('get_stars_low_rate')
    def get_stars_low_rate(self, obj):
        return get_object_stars_rate(obj, 'low')


    supported_languages = serializers.SerializerMethodField('get_supported_languages')
    def get_supported_languages(self, obj):
        return get_packageversion_supported_languages(obj)

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
                  'star',
                  'stars_good_rate',
                  'stars_medium_rate',
                  'stars_low_rate',
                  'author',
                  'screenshots',
                  'actions',
                  'versions_url',
                  'related_packages_url',
                  'released_datetime',
                  'supported_languages'
        )


class PettionPackageVersionSummarySerializer(PackageVersionRelatedPackageMixin,
                                             PackageVersionSummarySerializer):

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)
    cover = factory_imageurl_field(IMAGE_COVER_SIZE)
    download = serializers.SerializerMethodField('get_version_download_url')
    download_size = serializers.SerializerMethodField(
        'get_version_download_size')
    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')
    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    star = serializers.SerializerMethodField('get_star')

    package_name = serializers.RelatedField(source='package.package_name')

    title = serializers.RelatedField(source='package.title')

    summary = serializers.RelatedField(source='package.summary')

    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = PackageVersion
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  #'tags',
                  'petition_tags',
                  'star',
                  #'category_name',
                  #'version_count',
                  'summary',
                  'author',
                  'download',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  #'actions',
                  'version_name',
                  'version_code',
                  #'versions_url',
        )


class BasePackageVersionSummarySerializer(PackageVersionRelatedPackageMixin,
                                          PackageRelatedTagMin,
                                          PackageVersionSummarySerializer):

    package_name = serializers.SerializerMethodField('get_package_name')

    #title = serializers.SerializerMethodField('get_title')
    title = serializers.CharField(source='subtitle')

    author = serializers.SerializerMethodField('get_author')

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')

    actions = serializers.SerializerMethodField('get_action_links')

    versions_url = serializers.SerializerMethodField('get_versions_url')

    version_count = serializers.SerializerMethodField('get_version_count')

    tags = serializers.SerializerMethodField('get_tags')

    star = serializers.SerializerMethodField('get_star')
    def get_star(self, obj):
        return get_object_star(obj)

    class Meta:
        model = PackageVersion
        fields = ('url',
                  'icon',
                  'cover',
                  'title',
                  'package_name',
                  'version_name',
                  'version_code',
                  'version_count',
                  'versions_url',
                  'tags',
                  'star',
                  'category_name',
                  'categories_names',
                  'summary',
                  'author',
                  'download',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  'actions',
        )

class PackageVersionWithMyCommentSummarySerializer(
    BasePackageVersionSummarySerializer):

    package_name = serializers.SerializerMethodField('get_package_name')

    title = serializers.CharField(source='subtitle')

    author = serializers.SerializerMethodField('get_author')

    icon = factory_imageurl_field(IMAGE_ICON_SIZE)

    cover = factory_imageurl_field(IMAGE_COVER_SIZE)

    download = serializers.SerializerMethodField('get_version_download_url')

    download_size = serializers.SerializerMethodField(
        'get_version_download_size')

    comment_count = serializers.SerializerMethodField(
        'get_version_comment_count')

    comments_url = serializers.SerializerMethodField('get_version_comments_url')

    category_name = serializers.SerializerMethodField('get_main_category_name')
    categories_names = serializers.SerializerMethodField('get_categories_names')

    actions = serializers.SerializerMethodField('get_action_links')

    versions_url = serializers.SerializerMethodField('get_versions_url')

    version_count = serializers.SerializerMethodField('get_version_count')

    star = serializers.SerializerMethodField('get_star')

    tags = serializers.SerializerMethodField('get_tags')

    def _get_comment(self, obj):
        request = self.context.get('request')
        if request:
            try:
                return get_packageversion_comment_queryset(obj)\
                    .filter(user=request.user)[0]
            except (IndexError, ObjectDoesNotExist) as e:
                pass
        return None

    comment = serializers.SerializerMethodField('get_comment_content')
    def get_comment_content(self, obj):
        comment = self._get_comment(obj)
        if comment:
            return comment.comment
        return ''

    submit_date = serializers.SerializerMethodField('get_comment_submit_date')
    def get_comment_submit_date(self, obj):
        comment = self._get_comment(obj)
        if comment:
            return DateField().to_native(comment.submit_date)
        return ''

    class Meta:
        model = PackageVersion
        fields = ('url',
                  'icon',
                  'cover',
                  'title',
                  'package_name',
                  'version_name',
                  'version_code',
                  'version_count',
                  'versions_url',
                  'tags',
                  'star',
                  'category_name',
                  'categories_names',
                  'summary',
                  'author',
                  'download',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  'actions',
                  'comment',
                  'submit_date',
        )

