# -*- coding: utf-8 -*-
from warehouse import models as mods
from warehouse import documents as docs
from searcher import search_results as results, search_indexes as indexes
from mobapi2.serializers import HyperlinkedSearchSerializer, DateTimeField
from mobapi2.helpers import get_packageversion_comments_url
from mobapi2.settings import IMAGE_COVER_SIZE, IMAGE_ICON_SIZE
from mobapi2.warehouse.serializers.author import AuthorSummarySerializer, Author
from rest_framework import serializers
from toolkit.helpers import qurl_to
from mobapi2.warehouse.serializers.mixin import PackageActionsMixin


class PackageDocumentSearchIndex(indexes.PackageSearchIndex):

    def read_queryset(self, using=None):
        return docs.Package.objects.all()


class PackageSearchResult(results.PackageSearchResult):

    searchindex = PackageDocumentSearchIndex()


class PackageDetailSearchResult(results.PackageDetailSearchResult):

    searchindex = PackageDocumentSearchIndex()

    @property
    def screenshots(self):
        return self.object.screenshots

    @property
    def screenshots_default(self):
        for screenshot in self.object.screenshots:
            if screenshot.kind == 'default':
                yield screenshot

    @property
    def screenshots_ipad(self):
        for screenshot in self.object.screenshots:
            if screenshot.kind == 'ipad':
                yield screenshot


class PackageSummarySerializer(PackageActionsMixin,
                               HyperlinkedSearchSerializer):

    entrytype = 'client'

    icon = serializers.SerializerMethodField('get_icon_url')

    def get_icon_url(self, obj):
        return getattr(obj, 'icon_%s_url' % IMAGE_ICON_SIZE,
                       getattr(obj, 'icon_default_url', None)
        )

    cover = serializers.SerializerMethodField('get_cover_url')

    def get_cover_url(self, obj):
        return getattr(obj, 'cover_%s_url' % IMAGE_COVER_SIZE,
                       getattr(obj, 'cover_default_url', None)
        )

    title = serializers.CharField()

    package_name = serializers.CharField()

    version_name = serializers.CharField()

    version_code = serializers.IntegerField()

    category_name = serializers.CharField(source='primary_category_name')

    summary = serializers.CharField()

    has_award = serializers.BooleanField()

    award_coin = serializers.FloatField()

    author = serializers.SerializerMethodField('get_author')

    def get_author(self, obj):
        return AuthorSummarySerializer(Author(pk=obj.author_id,
                                              name=obj.author_name),
                                       context=self.context).data

    star = serializers.SerializerMethodField('get_stars_average')
    def get_stars_average(self, obj):
        return round(obj.star, 1)

    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return obj.tags_text.split()

    download = serializers.SerializerMethodField('get_download')

    def get_download(self, obj):
        request = self.context.get('request')
        url = qurl_to(obj.download_url,
                      entrytype=getattr(self, 'entrytype', None))
        if request:
            return request.build_absolute_uri(url)
        return url

    download_size = serializers.IntegerField()

    download_count = serializers.IntegerField()

    released_datetime = serializers.DateTimeField()

    comments_url = serializers.SerializerMethodField('get_comments_url')

    def get_comments_url(self, obj):
        url = get_packageversion_comments_url(
            mods.PackageVersion(pk=obj.latest_version_id),
            self.opts.router)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    actions = serializers.SerializerMethodField('get_action_links')

    class Meta:
        model = PackageSearchResult
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'tags',
                  'star',
                  'category_name',
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
                  'has_award',
                  'award_coin',
        )


class PackageVersionScreenshotSerializer(serializers.Serializer):

    large = serializers.SerializerMethodField('get_large_url')

    def get_large_url(self, obj):
        try:
            return obj.images['large']
        except:
            return None

    preview = serializers.SerializerMethodField('get_preview_url')

    def get_preview_url(self, obj):
        try:
            return obj.images['middle']
        except:
            return None

    rotate = serializers.CharField()

    class Meta:
        fields = (
            'large',
            'preview',
            'rotate'
        )


class PackageDetailSerializer(PackageSummarySerializer):

    def _get_stars_rate(self, obj, rate_type):
        return round(getattr(obj, 'stars_%s_rate'% rate_type, 0), 3)

    stars_good_rate = serializers.SerializerMethodField('get_stars_good_rate')
    def get_stars_good_rate(self, obj):
        return self._get_stars_rate(obj, 'good')

    stars_medium_rate = serializers.SerializerMethodField('get_stars_medium_rate')
    def get_stars_medium_rate(self, obj):
        return self._get_stars_rate(obj, 'medium')

    stars_low_rate = serializers.SerializerMethodField('get_stars_low_rate')
    def get_stars_low_rate(self, obj):
        return self._get_stars_rate(obj, 'low')

    whatsnew = serializers.CharField()
    description = serializers.CharField()

    screenshots = serializers.SerializerMethodField('get_screenshots')
    serializer_class_screenshot = PackageVersionScreenshotSerializer

    def get_screenshots(self, search_obj):
        try:
            if not isinstance(search_obj, PackageDetailSearchResult):
                search_obj.__class__ = PackageDetailSearchResult
            return self.serializer_class_screenshot(search_obj.object.screenshots,
                                                    many=True).data
        except:
            return list()

    comment_count = serializers.SerializerMethodField('get_comments_count')
    def get_comments_count(self, search_obj):
        return 0

    class Meta:
        model = PackageDetailSearchResult
        fields = ('url',
                  'icon',
                  'cover',
                  'package_name',
                  'title',
                  'tags',
                  'star',
                  'category_name',
                  'summary',
                  'whatsnew',
                  'description',
                  'author',
                  'download',
                  'download_size',
                  'download_count',
                  'comments_url',
                  'released_datetime',
                  'actions',
                  'version_name',
                  'version_code',
                  'has_award',
                  'award_coin',
                  'screenshots',
                  'stars_good_rate',
                  'stars_medium_rate',
                  'stars_low_rate',
                  'comment_count',
        )
