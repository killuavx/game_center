# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse

_ENTRY_TYPES = None


class AbsoluteUrlMixin(object):

    PAGE_TYPE_SPECIAL = 'special'

    PAGE_TYPE_DETAIL = 'detail'

    PAGE_TYPE_LIST = 'list'

    _page_view_name = 'mezzanine.pages.views.page'


    @classmethod
    def _get_entry_types(cls):
        global _ENTRY_TYPES
        if not _ENTRY_TYPES:
            _ENTRY_TYPES = settings.ENTRY_TYPES()
        return _ENTRY_TYPES

    def get_absolute_url_as(self, product, **kwargs):
        raise NotImplementedError


class ModelAbsoluteUrlMixin(AbsoluteUrlMixin):

    def get_absolute_url_as(self, product, **kwargs):
        ETS = self._get_entry_types()
        name = self.__class__._meta.module_name
        if product == ETS.web:
            view_name = 'website.%s.views.%s_detail' % (product, name)
        elif product == ETS.pc:
            view_name = 'website.views.%s.%s_detail' % (product, name)
        else:
            return None
        return reverse(view_name, kwargs=dict(pk=self.pk))


class AuthorAbsoluteUrlMixin(AbsoluteUrlMixin):

    @classmethod
    def page_absolute_url_as(cls, product, **kwargs):
        ETS = cls._get_entry_types()
        if product in (ETS.web, ETS.pc):
            page_slug = '%s/vendors' % product
            return reverse(cls._page_view_name, kwargs=dict(slug=page_slug))
        return None

    def get_absolute_url_as(self, product,
                            pagetype=AbsoluteUrlMixin.PAGE_TYPE_LIST,
                            **kwargs):
        ETS = self._get_entry_types()
        if product == ETS.web:
            if pagetype == self.PAGE_TYPE_DETAIL:
                view_name = 'website.%s.views.author_detail' % product
                return reverse(view_name, kwargs=dict(pk=self.pk))
            else:
                page_slug = 'vendors'
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                       + "?author=%s" % self.pk
        elif product == ETS.pc:
            if pagetype == self.PAGE_TYPE_DETAIL:
                view_name = 'website.views.%s.author_detail' % product
                return reverse(view_name, kwargs=dict(pk=self.pk))
            else:
                page_slug = '%s/vendors' % product
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                       + "?author=%s" % self.pk
        return None


class CategoryAbsoluteUrlMixin(AbsoluteUrlMixin):

    ROOT_SLUGS = ('game', 'application')

    def get_absolute_url_as(self, product, **kwargs):
        ETS = self._get_entry_types()
        if product == ETS.web:
            if self.slug in self.ROOT_SLUGS:
                page_slug = self.slug
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug))
            else:
                page_slug = self.get_root().slug
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                       + '?category=%s' % self.pk
        elif product == ETS.pc:
            if self.slug in self.ROOT_SLUGS:
                page_slug = "%s/%s" % (product, self.slug)
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                       + '?category=%s' % self.pk
            else:
                page_slug = "%s/%s" % (product, self.get_root().slug)
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                       + '?category=%s' % self.pk
        return None


class TopicAbsoluteUrlMixin(AbsoluteUrlMixin):

    def _special_views(self):
        from mezzanine.conf import settings as mz_settings
        return {mz_settings.GC_TOPICS_MASTERPIECE_SLUG: 'masterpiece',
                mz_settings.GC_TOPICS_COLLECTIONS_SLUG: 'collections'}

    def get_absolute_url_as(self, product,
                            pagetype=AbsoluteUrlMixin.PAGE_TYPE_DETAIL,
                            **kwargs):
        ETS = self._get_entry_types()
        if product == ETS.web:
            spec_views = self._special_views()
            if self.slug in spec_views:
                page_slug = spec_views[self.slug]
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug))

            if pagetype == self.PAGE_TYPE_DETAIL:
                view_name = 'website.%s.views.topic_detail' % product
                return reverse(view_name, kwargs=dict(slug=self.slug))

            if pagetype == self.PAGE_TYPE_SPECIAL:
                view_name = 'website.%s.views.topic_detail' % product
                return reverse(view_name, kwargs=dict(slug=self.slug))

        elif product == ETS.pc:
            if pagetype == self.PAGE_TYPE_DETAIL:
                view_name = 'website.views.%s.topic_detail' % product
                return reverse(view_name, kwargs=dict(slug=self.slug))

            spec_views = self._special_views()
            if self.slug in spec_views:
                page_slug = "%s/%s" % (product, spec_views[self.slug])
                return reverse(self._page_view_name, kwargs=dict(slug=page_slug))
        return None


class PackageRankingAbsoluteUrlMixin(AbsoluteUrlMixin):

    def get_absolute_url_as(self, product, **kwargs):
        ETS = self._get_entry_types()
        if product == ETS.web \
            and self.category.slug in CategoryAbsoluteUrlMixin.ROOT_SLUGS:
            page_slug = "ranking/%s" % self.category.slug
            return reverse(self._page_view_name, kwargs=dict(slug=page_slug)) \
                   + '#ranking_%s' % self.pk
        return None