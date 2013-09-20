# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author, PackageVersionScreenshot, PackageVersion
from django.core.urlresolvers import reverse

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

class FileUrlField(serializers.FileField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name')

class PackageLatestIconUrlField(serializers.FileField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return ''

def _package_latest_version_icon_url(self, obj):
    try:
        return obj.versions.latest_published().icon.url
    except:
        return ''

def _package_latest_version_screenshots(self, obj):
    try:
        latest_version = obj.versions.latest_published()
        screenshots_serializer = self.serializer_class_screenshot(
            latest_version.screenshots.all() ,
            many=True)
        return screenshots_serializer.data
    except:
        return dict()

class PackageVersionScreenshotSerializer(serializers.ModelSerializer):

    large = serializers.SerializerMethodField('get_large_url')
    preview = serializers.SerializerMethodField('get_preview_url')

    # TODO 截图的预览地址，以及后台上传时的尺寸处理，
    def get_preview_url(self, obj):
        return obj.image.url

    # TODO 截图的大图地址，以及后台上传时的尺寸处理，
    def get_large_url(self, obj):
        return obj.image.url

    class Meta:
        model = PackageVersionScreenshot
        fields = ('large', 'preview', 'rotate')

class PackageSummarySerializer(serializers.HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    get_latest_version_icon_url = _package_latest_version_icon_url

    author = AuthorSummarySerializer()
    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'package_name',
                  'title',
                  'tags',
                  'summary',
                  'author',
                  'released_datetime')

class PackageVersionSerializer(serializers.ModelSerializer):

    icon = ImageUrlField()

    download = FileUrlField(allow_empty_file=True)

    screenshots = PackageVersionScreenshotSerializer(many=True)

    class Meta:
        model = PackageVersion
        fields =( 'icon', 'version_code', 'version_name',
                  'screenshots', 'whatsnew', 'download',
        )

class PackageDetailSerializer(serializers.HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    serializer_class_screenshot = PackageVersionScreenshotSerializer
    screenshots = serializers.SerializerMethodField('get_latest_version_screenshots')

    author = AuthorSummarySerializer()
    versions = PackageVersionSerializer(many=True)

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    get_latest_version_icon_url = _package_latest_version_icon_url

    serializer_class_screenshot = PackageVersionScreenshotSerializer
    screenshots = serializers.SerializerMethodField('get_latest_version_screenshots')
    get_latest_version_screenshots = _package_latest_version_screenshots

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'package_name',
                  'title',
                  'tags',
                  'categories',
                  'summary',
                  'description',
                  'author',
                  'released_datetime',
                  'screenshots',
                  'versions',
        )

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    icon = ImageUrlField()

    cover = ImageUrlField()

    packages_url = serializers.SerializerMethodField('get_packages_url')
    def get_packages_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('author-packages', kwargs=dict(pk=obj.pk))
        )

    class Meta:
        model = Author
        fields = ('url','icon', 'cover', 'name', 'packages_url')

#---------------------------------------------------------------
from taxonomy.models import Category, Topic, TopicalItem
from mobapi.helpers import get_item_model_by_topic

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return None

    def from_native(self, data):
        pass

def get_url_for_taxonomy(request, obj, related_items, reverse_viewname):
    if related_items.count() > 0:
        path = reverse(reverse_viewname, kwargs=dict(slug=obj.slug))
        if request:
            return request.build_absolute_uri(path)
        return path
    return None

class CategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    PREFIX = 'category'

    icon = ImageUrlField()

    packages_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'parent',
                  'children',
                  'packages_url',
        )

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):

    PREFIX = 'category'

    icon = ImageUrlField()

    packages_url = serializers.SerializerMethodField('get_items_url')
    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.packages,
                                    '%s-packages' % self.PREFIX)

    class Meta:
        model = Category
        fields = ('url',
                  'icon',
                  'name',
                  'slug',
                  'packages_url',
        )

class TopicRelatedItemCountUrlAndChildrenUrlMixin(object):

    PREFIX = 'topic'

    item_model_class = None

    def get_items_queryset(self, obj):
        return TopicalItem.objects \
            .get_items_by_topic(obj, get_item_model_by_topic(obj))

    def get_items_count(self, obj):
        return self.get_items_queryset(obj).count()

    def get_items_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    self.get_items_queryset(obj),
                                    '%s-items' %self.PREFIX)

    def get_children_url(self, obj):
        return get_url_for_taxonomy(self.context.get('request'),
                                    obj,
                                    obj.children,
                                    '%s-children' %self.PREFIX)

class TopicDetailWithPackageSerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    serializers.HyperlinkedModelSerializer):
    icon = ImageUrlField()

    cover = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'name',
                  'slug',
                  'summary',
                  'children_url',
                  'items_url',
                  'items_count',
                  'updated_datetime',
                  'released_datetime')

class TopicSummarySerializer(
    TopicRelatedItemCountUrlAndChildrenUrlMixin,
    serializers.HyperlinkedModelSerializer):
    icon = ImageUrlField()

    cover = ImageUrlField()

    items_url = serializers.SerializerMethodField('get_items_url')

    items_count = serializers.SerializerMethodField('get_items_count')

    children_url = serializers.SerializerMethodField('get_children_url')

    class Meta:
        model = Topic
        fields = ('url',
                  'icon',
                  'cover',
                  'children_url',
                  'items_url',
                  'items_count',
                  'name',
                  'slug',
                  'updated_datetime',
                  'released_datetime')

