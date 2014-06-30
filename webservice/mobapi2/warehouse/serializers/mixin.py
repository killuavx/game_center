# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from mobapi2.helpers import (
    get_packageversion_comment_queryset,
    get_packageversion_comments_url, get_object_star, get_object_stars_rate)
from mobapi2.settings import IMAGE_COVER_SIZE, IMAGE_ICON_SIZE
from mobapi2.warehouse.serializers.helpers import (
    get_versions_url,
    get_packageversion_download_url,
    get_packageversion_download_size,
    get_packageversion_supported_languages)
from django.core.cache import cache


class PackageRelatedTagMin(object):
    def get_tags(self, obj):
        if not obj.tags_text:
            return list()
        return obj.tags_text.split()


class PackageActionsMixin(object):
    def get_action_links(self, obj):
        mark_url = None
        try:
            request = self.context.get('request')
            base_name = self.opts.router.get_base_name('bookmark-detail')
            mark_url = request.build_absolute_uri(
                reverse(base_name, kwargs=dict(pk=obj.pk))
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
        names = (cat.name for cat in obj.main_categories)
        return names


class PackageRelatedVersionsMixin(object):

    def get_version_count(self, obj):
        return obj.versions.published().count()

    def get_versions_url(self, obj):
        return get_versions_url(request=self.context.get('request'),
                                package=obj, router=self.opts.router)


class PackageRelatedLatestVersinoMixin(object):

    _package_latest_version_maps = dict()

    def _latest_version(self, obj):
        #if obj.pk not in self._package_latest_version_maps:
        #    self._package_latest_version_maps[obj.pk] = obj.versions.latest_published()
        #return self._package_latest_version_maps[obj.pk]
        return obj.versions.latest_published()

    def get_latest_version_title(self, obj):
        try:
            version = self._latest_version(obj)
            return version.subtitle
        except:
            return obj.title

    def get_latest_version_stars_good_rate(self, obj):
        try:
            version = self._latest_version(obj)
            return get_object_stars_rate(version, 'good')
        except:
            return 0

    def get_latest_version_stars_medium_rate(self, obj):
        try:
            version = self._latest_version(obj)
            return get_object_stars_rate(version, 'medium')
        except:
            return 0

    def get_latest_version_stars_low_rate(self, obj):
        try:
            version = self._latest_version(obj)
            return get_object_stars_rate(version, 'low')
        except:
            return 0

    def get_latest_version_star(self, obj):
        try:
            version = self._latest_version(obj)
            return get_object_star(version)
        except:
            return 0

    def get_latest_version_name(self, obj):
        try:
            return self._latest_version(obj).version_name
        except:
            return ''

    def get_latest_version_code(self, obj):
        try:
            return self._latest_version(obj).version_code
        except:
            return ''

    def get_latest_version_whatsnew(self, obj):
        try:
            return self._latest_version(obj).whatsnew
        except:
            return ''

    def get_latest_version_cover_url(self, obj):
        try:
            version = self._latest_version(obj)
            if IMAGE_COVER_SIZE is None:
                return version.cover.url
            return version.cover[IMAGE_COVER_SIZE].url
        except:
            return None

    def get_latest_version_icon_url(self, obj):
        try:
            version = self._latest_version(obj)
            return version.icon[IMAGE_ICON_SIZE].url
        except:
            return None

    def get_latest_version_screenshots(self, obj):
        from mobapi2.warehouse.serializers.packageversion import (
            PackageVersionScreenshotSerializer)
        self.serializer_class_screenshot = PackageVersionScreenshotSerializer
        try:
            latest_version = self._latest_version(obj)
            screenshots_serializer = self.serializer_class_screenshot(
                latest_version.screenshots.all(),
                many=True)
            return screenshots_serializer.data
        except:
            return dict()

    def get_latest_version_download(self, obj):
        latest_version = self._latest_version(obj)
        kwargs = dict()
        if hasattr(self, 'entrytype'):
            kwargs['entrytype'] = self.entrytype
        return get_packageversion_download_url(request=self.context.get('request'),
                                               version=latest_version,
                                               **kwargs)

    def get_latest_version_download_count(self, obj):
        latest_version = self._latest_version(obj)
        return latest_version.download_count

    def get_latest_version_download_size(self, obj):
        latest_version = self._latest_version(obj)
        return get_packageversion_download_size(latest_version)

    def get_latest_version_comment_count(self, obj):
        latest_version = self._latest_version(obj)
        return get_packageversion_comment_queryset(latest_version).count()

    def get_latest_version_comments_url(self, obj):
        latest_version = self._latest_version(obj)
        url = get_packageversion_comments_url(latest_version, self.opts.router)
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(url)
        except AttributeError:
            pass
        return url

    def get_latest_version_comment(self, obj):
        latest_version = self._latest_version(obj)
        return get_packageversion_comment_queryset(latest_version)\
            .by_submit_order()

    def get_latest_version_supported_languages(self, obj):
        latest_version = self._latest_version(obj)
        return get_packageversion_supported_languages(latest_version)


class PackageRelatedPackageUrlMixin(object):

    def get_related_packages_url(self, obj):
        request = self.context.get('request')
        view_name = self.opts.router.get_base_name('package-relatedpackages')
        related_url = reverse(view_name, kwargs=dict(pk=obj.pk))
        try:
            related_url = request.build_absolute_uri(related_url)
        except AttributeError:
            pass
        return related_url


class PackageRelatedAuthorMixin(object):

    def get_author(self, obj):
        from mobapi2.warehouse.serializers.author import AuthorSummarySerializer
        return AuthorSummarySerializer(obj.author, context=self.context).data
