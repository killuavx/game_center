# -*- coding: utf-8 -*-
from rest_framework import serializers
from warehouse.models import Package, Author, PackageScreenshot, PackageVersion

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

class PackageIconField(serializers.ImageField):

    def to_native(self, obj):
        try:
            return obj.versions.latest('version_code').icon.url
        except:
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

class PackageScreenshotSerializer(serializers.ModelSerializer):

    large = serializers.SerializerMethodField('get_large_url')
    preview = serializers.SerializerMethodField('get_preview_url')

    # TODO 截图的预览地址，以及后台上传时的尺寸处理，
    def get_preview_url(self, obj):
        return obj.image.url

    # TODO 截图的大图地址，以及后台上传时的尺寸处理，
    def get_large_url(self, obj):
        return obj.image.url

    class Meta:
        model = PackageScreenshot
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

    author = AuthorSummarySerializer()
    screenshots = PackageScreenshotSerializer(many=True)
    versions = PackageVersionSerializer(many=True)

    class Meta:
        model = Package
        fields = ('url',
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
        #icon = PackageIconField()
        class Meta:
            model = Package
            fields = ( 'url',
                       #'icon',
                       'package_name',
                       'title',
                       'summary',
                       'released_datetime',
            )

    packages = PackageSummarySerializer(many=True)


