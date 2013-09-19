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
