# -*- coding: utf-8 -*-
from copy import copy
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from toolkit.helpers import current_request

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

    @classmethod
    def _module_name(cls):
        return cls._meta.module_name

    def _get_module_name(self):
        return self._module_name()

    def get_absolute_url_as(self, product, **kwargs):
        ETS = self._get_entry_types()
        name = self._get_module_name()
        if product == ETS.web:
            view_name = 'website.%s.views.%s_detail' % (product, name)
        elif product == ETS.pc:
            view_name = 'website.views.%s.%s_detail' % (product, name)
        else:
            return None
        return reverse(view_name, kwargs=dict(pk=self.pk))


class PackageAbsoluteUrlMixin(ModelAbsoluteUrlMixin):

    def get_absolute_url_as(self, product, v=2, **kwargs):
        ETS = self._get_entry_types()
        if product == ETS.client:
            from mobapi2.helpers import PackageDetailApiUrlEncode
            from mobapi2.rest_router import rest_router
            pec= PackageDetailApiUrlEncode(pk=self.pk,
                                           request=current_request(),
                                           router=rest_router)
            return pec.get_url()
        else:
            return super(PackageAbsoluteUrlMixin, self).get_absolute_url_as(product=product, **kwargs)


class AuthorAbsoluteUrlMixin(AbsoluteUrlMixin):

    @classmethod
    def page_absolute_url_as(cls, product, **kwargs):
        ETS = cls._get_entry_types()
        if product == ETS.pc:
            page_slug = '%s/vendors' % product
            return reverse(cls._page_view_name, kwargs=dict(slug=page_slug))
        elif product == ETS.web:
            page_slug = 'vendors'
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

    ROOT_SLUG_GAME = 'game'

    ROOT_SLUG_APPLICATION = 'application'

    ROOT_SLUGS = (
        ROOT_SLUG_GAME,
        ROOT_SLUG_APPLICATION
    )

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

    @classmethod
    def absolute_url_as(cls, slug, product, **kwargs):
        try:
            cat = cls.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None
        return cat.get_absolute_url_as(product=product, **kwargs)


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


class AdvertisementAbsoluteUrlMixin(AbsoluteUrlMixin):

    def _fill_queryparams(self, url, **kwargs):
        if kwargs:
            part = list(urlparse(url))
            query_idx = 4
            _args = list(filter(lambda x: x[0] is None, kwargs.items()))
            query_params = list(parse_qsl(part[query_idx])) + _args
            part[query_idx] = urlencode(query_params)
            url = urlunparse(part)
        return url

    def get_absolute_url_as(self, product, **kwargs):
        if self.link:
            data = copy(kwargs)
            data['product'] = product
            return self._fill_queryparams(self.link, **data)
        elif self.content and isinstance(self.content, AbsoluteUrlMixin):
            return self.content.get_absolute_url_as(product=product, **kwargs)
        else:
            return None




