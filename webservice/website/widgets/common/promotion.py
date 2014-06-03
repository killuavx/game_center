# -*- coding: utf-8 -*-
from copy import deepcopy


class BaseMultiAdvWidget(object):

    slug = None

    def get_list(self, slug, max_items=None):
        from promotion.models import Place, Advertisement
        try:
            place = Place.objects.get(slug=slug)

            items = list(place.advertisements.published())
            if max_items is None:
                return items
            return items[0:max_items]
        except (Place.DoesNotExist, Advertisement.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        self.product = options.get('product')
        self.request = context.get('request')
        self.options = options
        self.slug = options.get('slug', self.slug)
        max_items = options.get('max_items', None)
        items = self.get_list(slug=self.slug, max_items=max_items)
        data = deepcopy(options)
        data.update(
            slug=self.slug,
            items=items,
            product=self.product,
            max_items=max_items
        )
        return data


class BaseSingleAdvWidget(object):

    slug = None

    def get_object(self, slug):
        from promotion.models import Place, Advertisement
        try:
            place = Place.objects.get(slug=slug)
            return place.advertisements.published()[0]
        except (Place.DoesNotExist, Advertisement.DoesNotExist):
            return None
        except IndexError:
            return None

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self.slug)
        self.request = context.get('request')
        self.product = options.get('product')
        item = self.get_object(slug=self.slug)
        self.options = options
        data = deepcopy(options)
        data.update(
            slug=self.slug,
            product=self.product,
            item=item,
        )
        return data
