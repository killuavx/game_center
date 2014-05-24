# -*- coding: utf-8 -*-
from django_widgets import Widget
from warehouse.models import Package
from taxonomy.models import Category, Topic, TopicalItem
from .common.promotion import BaseMultiAdvWidget
from .common.base import BaseListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget
from .common.webspide import BaseForumThreadPanelWdiget
from .masterpiece import MasterpiecePackageListWidget
from mptt.models import MPTTModel


def get_leaf_categories(cats):
    result =  []

    for cat in cats:
        if MPTTModel.is_leaf_node(cat):
            result.append(cat)

    return result


def get_all_sub_cats(slug):
    cat = get_category_by_slug(slug)

    if cat is None:
        return []
    else:
        return cat.get_descendants()


def get_category_by_slug(slug):
    try:
        cat = Category.objects.get(slug=slug)
    except:
        cat = None

    return cat

def filter_packages_by_category(packages, cat):
    cats = cat.get_descendants(True)
    pkgs =  packages.filter(categories__in=cats)
    if not pkgs:
        return pkgs.none()

    return  pkgs.distinct()


def filter_packages_by_category_slug(packages, slug):

    cat = get_category_by_slug(slug)

    if cat is None:
        return packages.none()

    cats = cat.get_descendants(True)
    pkgs =  packages.filter(categories__in=cats)
    if not pkgs:
        return pkgs.none()

    return  pkgs.distinct()


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
        #print(len(items))
        return {'items': items, 'cat': self.cat}



class HomeHotBbsWidget(BaseForumThreadPanelWdiget, Widget):

    template = 'pages/widgets/android/hot-bbs.html'


class HomeNoviceBbsWidget(BaseForumThreadPanelWdiget, Widget):

    template = 'pages/widgets/android/novice-bbs.html'


class CategoriesListWidget(BaseListWidget):

    template = 'pages/widgets/android/game-app-list.html'
    slug = None

    def get_categorized_pagckages(self, packages, cat):
        return filter_packages_by_category(packages, cat)

    def get_all_published_packages(self):
        return Package.objects.published()

    def get_list(self):
        cats = get_all_sub_cats(self.slug)
        leaf_cats = get_leaf_categories(cats)
        return leaf_cats

    def get_context(self, value=None, options=dict(), context=None):
        items = []
        self.slug = options.get('slug', None)
        root_cat = get_category_by_slug(self.slug)
        all_packages = self.get_all_published_packages()
        root_packages = self.get_categorized_pagckages(all_packages, root_cat)

        cats = self.get_list()
        for cat in cats:
            packages = self.get_categorized_pagckages(root_packages, cat)
            items.append({'cat': cat, 'packages': packages})

        options.update(
            items=items,
            root_cat=root_cat,
            root_packages = root_packages,
            current_packages = root_packages,
            current_cat = root_cat,
        )

        return options


class AppsListWidget(Widget):

    template = 'pages/widgets/android/cats-left-list.html'

