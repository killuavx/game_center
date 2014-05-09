# -*- coding: utf-8 -*-
from promotion.models import Place, Advertisement

class BaseMultiAdvWidget(object):

    slug = None

    def get_list(self, slug, max_items=None):
        try:
            place = Place.objects.get(slug=slug)

            items = list(place.advertisements.published())
            if max_items is None:
                return items
            return items[0:max_items]
        except (Place.DoesNotExist, Advertisement.DoesNotExist):
            return list()

    def get_context(self, value=None, options=dict(), context=None):
        slug = options.get('slug', self.slug)
        max_items = options.get('max_items', None)
        items = self.get_list(slug=slug, max_items=max_items)
        options.update(
            slug=slug,
            items=items,
            max_items=max_items
        )
        return options


class BaseSingleAdvWidget(object):

    slug = None

    def get_object(self, slug):
        try:
            place = Place.objects.get(slug=slug)
            return place.advertisements.published()[0]
        except (Place.DoesNotExist, Advertisement.DoesNotExist):
            return None
        except IndexError:
            return None

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', self.slug)
        item = self.get_object(slug=self.slug)
        options.update(
            slug=self.slug,
            item=options.get('item', item),
        )
        return options
