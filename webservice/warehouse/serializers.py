# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author, PackageVersionScreenshot, PackageVersion

class ImageUrlField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return ''

    def from_native(self, data):
        pass

class FileUrlField(serializers.FileField):

    def to_native(self, obj):
        try:
            return obj.url
        except ValueError:
            return ''

    def from_native(self, data):
        pass

class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'name')

class PackageSummarySerializer(serializers.HyperlinkedModelSerializer):

    author = AuthorSummarySerializer()
    class Meta:
        model = Package
        fields = ('url',
                  'package_name',
                  'title',
                  'tags',
                  'summary',
                  'author',
                  'released_datetime')

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

class PackageVersionSerializer(serializers.ModelSerializer):

    icon = ImageUrlField()

    download = FileUrlField(allow_empty_file=True)

    class Meta:
        model = PackageVersion
        fields =( 'icon', 'version_code', 'version_name',
                  'whatsnew', 'download',
        )

class PackageDetailSerializer(serializers.HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_latest_version_icon_url')
    serializer_class_screenshot = PackageVersionScreenshotSerializer
    screenshots = serializers.SerializerMethodField('get_latest_version_screenshots')

    author = AuthorSummarySerializer()
    versions = PackageVersionSerializer(many=True)

    def get_latest_version_screenshots(self, obj):
        try:
            latest_version = obj.versions.latest_published()
            screenshots_serializer = self.serializer_class_screenshot(
                latest_version.screenshots.all() ,
                many=True)
            return screenshots_serializer.data
        except:
            return dict()

    def get_latest_version_icon_url(self, obj):
        try:
            return obj.versions.latest_published().icon.url
        except:
            return ''

    class Meta:
        model = Package
        fields = ('url',
                  'icon',
                  'package_name',
                  'title',
                  'tags',
                  'summary',
                  'description',
                  'author',
                  'released_datetime',
                  'screenshots',
                  'versions',
        )

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('url', 'name', 'packages')

    class PackageSummarySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Package
            fields = ( 'url',
                       'package_name',
                       'title',
                       'summary',
                       'released_datetime',
            )

    packages = PackageSummarySerializer(many=True)


