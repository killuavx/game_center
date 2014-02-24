# -*- coding: utf-8 -*-
from warehouse.models import PackageVersion


class BasePackageListWidget(object):

    def get_more_url(self):
        return None

    def get_list(self):
        return PackageVersion.objects.by_published_order(True)

    def get_context(self, value=None, options=dict(), context=None):
        items = self.get_list()
        max_items = options.get('max_items', 5)
        options.update(
            title=options.get('title'),
            more_url=self.get_more_url(),
            items=options.get('items', list(items[0:max_items])),
            max_items=max_items,
        )
        return options


class BaseRankingPackageListWidget(BasePackageListWidget):

    def get_list(self):
        return PackageVersion.objects.published().by_rankings_order()
