# -*- coding: utf-8 -*-
from django_widgets import Widget
from warehouse.models import Package
from taxonomy.models import Category, Topic, TopicalItem
from .common.promotion import BaseMultiAdvWidget
from .common.base import BaseListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget
from .masterpiece import MasterpiecePackageListWidget


def get_root_category_by_slug(slug):
    try:
        root_cat = Category.objects.get(slug=slug)
    except:
        root_cat = None

    return root_cat

def filter_packages_by_category_slug(packages, slug):

    root_cat = get_root_category_by_slug(slug)

    if root_cat is None:
        return []

    cats = root_cat.get_descendants(True)
    pkgs =  packages.filter(categories__in=cats)
    if not pkgs:
        return []

    return  pkgs.distinct().by_published_order()


class HomeTopBannersWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/home-top-banner.html'

class HomeTopAdWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/home-top-ad.html'


class HomeMasterpiecePackageListWidget(MasterpiecePackageListWidget):

    per_page = 10
    template = 'pages/widgets/android/masterpiece.html'


class LatestPackageListWidget(BaseListWidget):

    template = 'pages/widgets/android/latest-release.html'
    cat = None
    slug = None

    def get_list(self):
        try:
            cat = Category.objects.get(slug=self.slug)
        except:
            return []

        cats = cat.get_descendants(True)
        self.cat = cat

        try:
            packages = Package.objects.filter(categories__in=cats).\
                distinct().by_published_order(True)
        except:
            return []

        return packages

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = options.get('slug', None)
        packages = self.get_list()
        options.update(
            items=packages,
            cat=self.cat,
        )
        #print(packages.count())
        return options


class CategorizedPackageListWidget(LatestPackageListWidget):

    template = 'pages/widgets/android/first-publish-crack.html'


class HomeTopicsPackageListWidget(BaseTopicPackageListWidget):

    template = 'pages/widgets/android/selected-webgames.html'


class HomeTabsPackageListWidget(BaseTopicPackageListWidget):

    template = 'pages/widgets/android/left-tab-box.html'
    cat = None

    def get_packages_by_category_slug(self, packages, slug):
        return filter_packages_by_category_slug(packages, slug)

    def get_packages_by_topic_slug(self, packages, slug):
        tmp = {}
        if slug == 'latest_published':
            tmp['items'] =  packages.by_published_order()
            tmp['topic_name']  = '最新发布'
        else:
            try:
                topic = Topic.objects.filter(slug=slug).published().get()
                tmp['items'] = TopicalItem.objects.filter_items_by_topic(topic, Package, packages)
                tmp['topic_name']  = topic.name
            except:
                pass

        #print (tmp)
        return tmp


    def get_context(self, value=None, options=dict(), context=None):
        slugs =  options.get('slugs', None)
        cat  = options.get('cat', None)
        cat_dic = {
            'game': '游戏',
            'application': '软件',
        }
        packages = self.get_packages_by_category_slug(Package.objects.all(), cat)
        result = []

        if slugs and packages:
            for slug in slugs.split('|'):
                result.append(self.get_packages_by_topic_slug(packages, slug))

        #print ({'result': result})
        #print (len(result))
        return {'result': result, 'cat': cat_dic.get(cat)}


class HomeRankingPackageListWidget(BaseRankingPackageListWidget):

    template = 'pages/widgets/android/right-ranking-box.html'
    cat = None

    def get_list(self):
        from ranking.models import PackageRanking
        pkgRks = PackageRanking.objects.filter(cycle_type=0).filter(ranking_type__slug="total").filter(category__slug=self.cat)
        if not pkgRks:
            return []
        else:
            return pkgRks[0].packages.all()

    def get_context(self, value=None, options=dict(), context=None):
        self.cat = options.get('cat', None)
        items = self.get_list()
        print(len(items))
        return {'items': items, 'cat': self.cat}

