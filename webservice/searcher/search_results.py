# -*- coding: utf-8 -*-
from haystack.models import SearchResult
from toolkit.helpers import language_codes_to_names
from toolkit.model_url_mixin import PackageAbsoluteUrlMixin
from toolkit.cache_tagging_mixin import PackageTaggingMixin, PackageWithLatestVersionTaggingMixin


class PackageSearchResult(SearchResult,
                          PackageWithLatestVersionTaggingMixin,
                          PackageAbsoluteUrlMixin):

    @classmethod
    def _get_module_name(self):
        return 'package'

    # for ios
    @property
    def is_free(self):
        return self.is_free_b

    @property
    def formatted_price(self):
        return self.formatted_price_s

    @property
    def support_ipad(self):
        return self.support_ipad_b

    @property
    def support_iphone(self):
        return self.support_iphone_b

    @property
    def support_idevices(self):
        return self.support_idevices_b

    def _prepare_category(self, id, slug, name):
        from taxonomy.models import Category
        return Category(id=id, slug=slug, name=name, site_id=self.site)

    def root_category(self):
        return self._prepare_category(id=self.root_category_id,
                                      slug=self.root_category_slug,
                                      name=self.root_category_name)

    def primary_category(self):
        cat = self._prepare_category(id=self.primary_category_id,
                                     slug=self.primary_category_slug,
                                     name=self.primary_category_name)
        cat.get_root = lambda: self.root_category()
        return cat

    def language_names(self):
        if self.support_language_codes:
            return language_codes_to_names(self.support_language_codes)
        return []


class PackageDetailSearchResult(PackageSearchResult):

    @property
    def screenshots(self):
        from warehouse.models import PackageVersionScreenshot
        qs = PackageVersionScreenshot.objects\
            .filter(version_id=self.latest_version_id)

        class FilterKindDict(dict):

            def ipad(self):
                return qs.filter(kind='ipad')

            def default(self):
                return qs.filter(kind='default')

            def count(self):
                return qs.count()

            def __getattr__(self, kind):
                return qs.get(kind=kind)

            def __getitem__(self, kind):
                if hasattr(qs, kind):
                    return getattr(qs, kind)

                if isinstance(kind, int):
                    return qs[kind]
                return qs.get(kind=kind)

            def __iter__(self):
                return qs

            def __repr__(self):
                return '<FilterKindDict: screenshots of version:%d>' % self.latest_version_id

        return FilterKindDict()

