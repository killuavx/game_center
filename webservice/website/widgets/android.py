# -*- coding: utf-8 -*-
import datetime
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib.comments import Comment
from mptt.models import MPTTModel
from django_widgets import Widget
from warehouse.models import Package
from taxonomy.models import Category, Topic, TopicalItem
from .common.promotion import BaseMultiAdvWidget
from .common.base import BaseListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget
from .common.webspide import BaseForumThreadPanelWdiget
from .masterpiece import MasterpiecePackageListWidget
from .common.category import BaseTopicAuthorPackageListWidget
from .common.base import PaginatorPageMixin
from .pc.home import PCRankingPackageListWidget


def get_limit_range(p, r, n=10):
    # p - request page number
    # r - paginator.page_range
    # n - num of links on a page

    l = r[-1]
    if n >= l:
        return r
    x, y = divmod(p, n)
    m = n//2
    if y > 0:
        if p-m <= 0:
            return range(1, 2*m+1)
        elif p+m > l:
            end = l
        else:
            end = p+m
        return range(end-n+1, end+1)
    else:
        if p-m <= 0:
            return range(1, 2*m+1)
        elif p+m > l:
            end = l+1
            return range(end-n, end)
        else:
            end = p+m
        return range(p-m, end)


def get_topic_by_slug(slug):
    try:
        topic = Topic.objects.filter(slug=slug).published().get()
    except:
        topic = None

    return topic


def get_all_topics():
    return Topic.objects.published()


def get_all_collections():
    collections = []
    topics = get_all_topics()

    for tp in topics:
        lst = tp.get_children()
        collections.extend(lst)

    return collections


def filter_packages_by_topic(packages, topic):
    return TopicalItem.objects.filter_items_by_topic(topic, Package, packages)


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


class HomeMasterpiecePackageListWidget(MasterpiecePackageListWidget, Widget):

    per_page = 10
    template = 'pages/widgets/android/masterpiece.html'


class LatestPackageListWidget(BaseListWidget, Widget):

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


class CategorizedPackageListWidget(LatestPackageListWidget, Widget):

    template = 'pages/widgets/android/first-publish-crack.html'


class HomeTopicsPackageListWidget(BaseTopicPackageListWidget, Widget):

    template = 'pages/widgets/android/selected-webgames.html'


class HomeTabsPackageListWidget(BaseTopicPackageListWidget, Widget):

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


class HomeRankingPackageListWidget(BaseRankingPackageListWidget, Widget):

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


class CategoriesPackagesListWidget(BaseListWidget, Widget):

    template = 'pages/widgets/android/app-list.html'
    slug = None
    current_cat = None
    current_topic = None
    current_packages = None

    def get_categorized_pagckages(self, packages, cat):
        return filter_packages_by_category(packages, cat)

    def get_all_published_packages(self):
        return Package.objects.published()

    def get_list(self):
        cats = get_all_sub_cats(self.slug)
        leaf_cats = get_leaf_categories(cats)
        return leaf_cats

    def get_all_items(self, cat_slug, root_packages, cats):
        items = []
        for cat in cats:
            #packages = self.get_categorized_pagckages(root_packages, cat)
            packages = cat.packages.published()
            if cat.slug == cat_slug:
                self.current_packages = packages
                self.current_cat = cat
            items.append({'cat': cat, 'packages': packages})

        return items


    def get_packages_by_topic_slug(self, topic_slug, packages):
        topic = get_topic_by_slug(topic_slug)
        if not topic:
            return
        self.current_topic = topic
        self.current_packages = filter_packages_by_topic(packages, topic)


    def get_latest_packages(self, packages):
        self.current_packages = packages.by_published_order()
        self.current_topic = {}
        self.current_topic['slug'] = 'latest'

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.current_packages, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)

    def get_translated_slug(self):
        dic = {
            'game': '游戏',
            'application': '软件',
        }

        return dic.get(self.slug, None)


    def get_context(self, value=None, options=dict(), context=None):
        #print (options)
        items = []
        self.current_cat = None
        self.current_topic = None
        self.page = None
        self.slug = options.get('slug', None)
        cat_slug = options.get('cat', None)
        topic_slug = options.get('topic', None)
        pub_slug = options.get('pub', None)
        root_cat = get_category_by_slug(self.slug)
        all_packages = self.get_all_published_packages()
        root_packages = self.get_categorized_pagckages(all_packages, root_cat)
        cats = self.get_list()
        items = self.get_all_items(cat_slug, root_packages, cats)
        if self.current_cat is None:
            if topic_slug:
                self.get_packages_by_topic_slug(topic_slug, root_packages)
            elif pub_slug:
                self.get_latest_packages(root_packages)

        if not self.current_cat and not self.current_topic:
            self.current_packages = root_packages

        current_page = self.paginize_items(options)
        limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
        #print (current_page.number)

        options.update(
            items=items,
            root_cat=root_cat,
            root_packages = root_packages,
            current_packages = current_page,
            current_page = current_page,
            limit_range = limit_range,
            current_cat = self.current_cat,
            current_topic = self.current_topic,
            translated_slug = self.get_translated_slug(),
        )
        #print (options['current_cat'])
        #print (options['current_topic'])

        return options


class CrackTopBannersWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/crack-top-banner.html'


class FirstReleaseCrackPackagesListWidget(BaseListWidget, Widget):

    template = 'pages/widgets/android/crack-first-release.html'
    crack_cat = None

    def get_all_crack_packages(self, slug):
        crack_cat = get_category_by_slug(slug)
        self.crack_cat = crack_cat

        if not crack_cat:
            return Package.objects.none()

        return crack_cat.packages.all()


    def get_crack_packages_by_delta_days(self, packages, date, future=False):
        packages = packages.filter(released_datetime__startswith=date)
        if future:
            packages = packages.filter(status=Package.STATUS.unpublished)
        return packages


    def get_date(self, delta_days):
        return now().date()-datetime.timedelta(days=delta_days)


    def get_context(self, value=None, options=dict(), context=None):
        slug = options.get('slug', None)
        all_crack_packages = self.get_all_crack_packages(slug)
        all_crack_packages_published = all_crack_packages.published()
        crack_packages_today = self.get_crack_packages_by_delta_days(\
            all_crack_packages_published, self.get_date(2))
        crack_packages_yesterday = self.get_crack_packages_by_delta_days(\
            all_crack_packages_published, self.get_date(4))
        crack_packages_yesterday_before = self.get_crack_packages_by_delta_days\
            (all_crack_packages_published, self.get_date(5))

        someday = self.get_date(36)
        crack_packages_someday = self.get_crack_packages_by_delta_days(\
            all_crack_packages_published, someday)
        crack_packages_tomorrow = self.get_crack_packages_by_delta_days(\
            all_crack_packages, self.get_date(-1), True)

        options.update(
            crack_packages_today = crack_packages_today,
            crack_packages_yesterday = crack_packages_yesterday,
            crack_packages_yesterday_before = crack_packages_yesterday_before,
            crack_packages_someday  = crack_packages_someday,
            crack_packages_tomorrow = crack_packages_tomorrow,
            cat = self.crack_cat,
            someday = someday,
        )

        return options


class AllCrackPackagesListWidget(FirstReleaseCrackPackagesListWidget):
    template = 'pages/widgets/android/crack-all.html'

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.current_packages, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)

    def get_context(self, value=None, options=dict(), context=None):
        slug = options.get('slug', None)
        all_crack_packages = self.get_all_crack_packages(slug)
        #print (all_crack_packages)
        all_crack_packages_published  = None
        if all_crack_packages:
            all_crack_packages_published = all_crack_packages.published()
        if all_crack_packages_published:
            self.current_packages = all_crack_packages_published
            current_page = self.paginize_items(options)
            limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
            options.update(
                current_page = current_page,
                limit_range = limit_range,
            )

        #print (options)
        return options


class CrackTopicPackagesListWidget(BaseListWidget, Widget):
    template = 'pages/widgets/android/crack-all.html'

    def get_list(self):
        pass

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.current_packages, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)

    def get_context(self, value=None, options=dict(), context=None):
        #topic = options.get('topic', None)
        topic = get_topic_by_slug('home-recommend-game')
        packages = filter_packages_by_topic(Package.objects.published(), topic)
        self.current_packages = packages
        if self.current_packages:
            current_page = self.paginize_items(options)
            limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
            options.update(
                current_page = current_page,
                limit_range = limit_range,
            )
        return options


class CollectionsPackagesListWidget(BaseListWidget, Widget):

    template = 'pages/widgets/android/collection-box.html'

    def get_all_collections(self):
        return get_all_collections()

    def get_list(self):
        lst = []

        for topic in self.collections:
            packages = TopicalItem.objects\
                .get_items_by_topic(topic=topic, item_model=Package)
            lst.append({'topic': topic, 'packages': packages})

        return lst

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.current_packages, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)


    def get_context(self, value=None, options=dict(), context=None):
        self.collections = self.get_all_collections()
        items = self.get_list()
        self.current_packages = items
        if self.current_packages:
            current_page = self.paginize_items(options)
            limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
            options.update(
                current_page = current_page,
                limit_range = limit_range,
            )
        #print (options)
        return options


class CollectionPackagesListWidget(BaseListWidget, Widget):

    template = 'pages/widgets/android/collection-detail.html'

    def get_list(self):
        packages = TopicalItem.objects\
            .get_items_by_topic(topic=self.topic, item_model=Package)

        return packages

    def get_context(self, value=None, options=dict(), context=None):
        topic_slug = options.get('topic', None)
        try:
            self.topic = Topic.objects.get(slug=topic_slug)
        except:
            self.topic = None

        packages = self.get_list()

        options.update(
            topic = self.topic,
            items = packages,
        )
        #print (options)
        return options


class MasterpiecePackagesListWidget(BaseTopicPackageListWidget, Widget):
    template = 'pages/widgets/android/master-list.html'


class VendorPackageListWidget(PaginatorPageMixin, BaseTopicAuthorPackageListWidget, Widget):
    template = 'pages/widgets/android/vendor-app-list.html'
    current_vendor = None
    current_packages = None

    def get_vendors(self):
        return self.get_topic_authors()

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.current_packages, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)

    def get_list(self):
        items = []
        for vendor in self.vendors:
            packages = self.get_package_list_by(vendor)
            if vendor.id == self.vendor_id:
                self.current_vendor = vendor
                self.current_packages = packages
            items.append({'vendor': vendor, 'packages': packages})

        return items


    def get_context(self, value=None, options=dict(), context=None):
        current_page = None
        limit_range = None
        self.current_vendor = None
        self.current_packages = None
        self.vendor_id = None
        self.slug = options.get('slug', self.slug)
        try:
            self.vendor_id = int(options.get('id', None))
        except:
            self.vendor_id = None

        #print (self.vendor_id)
        self.vendors = self.get_vendors()
        options.update(
            vendors = self.vendors,
        )
        items = self.get_list()

        if not self.current_vendor and items:
            self.current_vendor = items[0]['vendor']
            self.current_packages = items[0]['packages']

        #print (self.current_packages)
        if self.current_packages:
            current_page = self.paginize_items(options)
            limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
            options.update(
                current_vendor = self.current_vendor,
                current_packages = self.current_packages,
                current_page = current_page,
                limit_range = limit_range,
            )
        #print( current_page )
        #print(limit_range)
        return options

class RankPackageListWidget(PCRankingPackageListWidget):

    template='pages/widgets/android/ranking.html'

    def get_context(self, value, options):

        cat_slug = options.get('cat_slug', None)
        ranking_slug = options.get('ranking_slug', None)
        ranking = self.get_ranking(cat_slug, ranking_slug)
        options.update(
            ranking = ranking,
            items = ranking.packages.published(),
        )

        return options


class RankPackageDetailListWidget(RankPackageListWidget):

    template='pages/widgets/android/package-rank.html'


class PackageVersionCommentListWidget(BaseListWidget, Widget):

    template='pages/widgets/android/comment.html'
    per_page = 10

    def get_list(self):
        comments = Comment.objects.filter(object_pk=self.pkgv.pk)\
                .filter(is_public=True, is_removed=False)
        return comments

    def paginize_items(self, options):
        per_page, page = self.get_paginator_vars(options)
        self.page = page
        paginator = Paginator(self.comments, per_page=self.per_page)
        current_page = paginator.page(page)
        return current_page

    def get_limit_pages_range(self, page, range):
        return get_limit_range(page, range)

    def get_context(self, value=None, options=dict(), context=None):
        self.pkgv = options.get('pkgv', None)
        self.comments = self.get_list()
        print (self.comments)

        if self.comments:
            current_page = self.paginize_items(options)
            limit_range = self.get_limit_pages_range(self.page, current_page.paginator.page_range)
            options.update(
                current_page = current_page,
                limit_range = limit_range,
            )

        #print(options)
        return options
