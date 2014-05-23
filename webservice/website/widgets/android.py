# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseMultiAdvWidget
from .common.base import BaseListWidget
from .masterpiece import MasterpiecePackageListWidget
from warehouse.models import Package
from taxonomy.models import Category


class HomeTopBannersWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/home-top-banner.html'


class HomeMasterpiecePackageListWidget(MasterpiecePackageListWidget):

    per_page = 10
    template = 'pages/widgets/android/masterpiece.html'


class LatestPackageListWidget(BaseListWidget):

    template = 'pages/widgets/android/latest-release.html'
    slug = None

    def get_list(self):
        try:
            cat = Category.objects.get(slug=self.slug)
        except:
            return []

        cats = cat.get_descendants(True)

        try:
            packages = Package.objects.filter(categories__in=cats).\
                distinct().by_published_order(True)
        except:
            return []

        return packages

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', None)
        packages = self.get_list()
        options.update(items=packages)
        #print(packages.count())
        return options
