# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from mobapi.settings import IMAGE_COVER_SIZE, IMAGE_ICON_SIZE
from mobapi.warehouse.serializers.packageversion import (
    PackageVersionScreenshotSerializer,
    get_packageversion_download_url,
    get_packageversion_download_size)
from mobapi.serializers import (get_packageversion_comment_queryset,
                                get_packageversion_comments_url)


class PackageRelatedTagMin(object):
    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)


class PackageActionsMixin(object):
    def get_action_links(self, obj):
        mark_url = None
        try:
            request = self.context.get('request')
            mark_url = request.build_absolute_uri(
                reverse('bookmark-detail', kwargs=dict(pk=obj.pk))
            )
        except AttributeError:
            pass
        return dict(
            mark=mark_url,
        )


class PackageRelatedCategoryMixin(object):
    def get_main_category_name(self, obj):
        try:
            return obj.main_category.name
        except AttributeError:
            return None

    def get_categories_names(self, obj):
        names = (cat.name for cat in obj.categories.all())
        return names


class PackageRelatedVersionsMixin(object):
    def get_version_count(self, obj):
        return obj.versions.published().count()


class PackageRelatedLatestVersinoMixin(object):
    serializer_class_screenshot = PackageVersionScreenshotSerializer

    def get_latest_version_name(self, obj):
        try:
            return obj.versions.latest_published().version_name
        except:
            return ''

    def get_latest_version_code(self, obj):
        try:
            return obj.versions.latest_published().version_code
        except:
            return ''

    def get_latest_version_whatsnew(self, obj):
        try:
            return obj.versions.latest_published().whatsnew
        except:
            return ''

    def get_latest_version_cover_url(self, obj):
        try:
            version = obj.versions.latest_published()
            if IMAGE_COVER_SIZE is None:
                return version.cover.url
            return version.cover[IMAGE_COVER_SIZE].url
        except:
            return None

    def get_latest_version_icon_url(self, obj):
        try:
            return obj.versions.latest_published().icon[IMAGE_ICON_SIZE].url
        except:
            return None

    def get_latest_version_screenshots(self, obj):
        try:
            latest_version = obj.versions.latest_published()
            screenshots_serializer = self.serializer_class_screenshot(
                latest_version.screenshots.all(),
                many=True)
            return screenshots_serializer.data
        except:
            return dict()

    def get_latest_version_download(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_download_url(latest_version)

    def get_latest_version_download_count(self, obj):
        latest_version = obj.versions.latest_published()
        return latest_version.download_count

    def get_latest_version_download_size(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_download_size(latest_version)

    def get_latest_version_comment_count(self, obj):
        latest_version = obj.versions.latest_published()
        return get_packageversion_comment_queryset(latest_version).count()

    def get_latest_version_comments_url(self, obj):
        latest_version = obj.versions.latest_published()
        url = get_packageversion_comments_url(latest_version)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url