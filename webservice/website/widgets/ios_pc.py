# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from .masterpiece import MasterpiecePackageListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget
from taxonomy.models import Topic, Category, TopicalItem
from warehouse.models import Package


class BannerToprightWidget(BaseSingleAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_right.html'


class BannerTopleftWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_left.html'


def filter_packages_by_category_slug(packages, slug):
    try:
        root_cat = Category.objects.get(slug=slug)
    except:
        return []

    cats = root_cat.get_descendants(True)
    #print (cats)
    pkgs =  packages.filter(categories__in=cats)

    if not pkgs:
        return []

    return  pkgs.distinct().by_published_order()



class PackageListRollBoxWidget(MasterpiecePackageListWidget):

    template = 'pages/widgets/ios_pc/roll_box.html'

    def get_list(self, type):
        return filter_packages_by_category_slug(Package.objects.published(), type)

    def get_context(self, value=None, options=dict(), context=None):
        type = options.get('type', None)
        cat = 'application' if type == 'soft' else type
        packages = self.get_list(cat)
        tmp = {}
        tmp['items'] = packages

        return tmp



class TopicPackageListBoxWidget(BaseTopicPackageListWidget):

    template = 'pages/widgets/ios_pc/package_list_box_left.html'

    def get_packages_by_category_slug(self, packages, slug):
        return filter_packages_by_category_slug(packages, slug)

    def get_packages_by_topic_slug(self, packages, slug):
        tmp = {}
        prefix = 'iospc'
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
        tmp['more_url'] ='/%s/%s' % (prefix, slug)

        return tmp


    def get_context(self, value=None, options=dict(), context=None):
        slugs =  options.get('slugs', None)
        cat  = options.get('type', None)
        category_slug = 'application' if cat == 'soft' else cat
        packages = self.get_packages_by_category_slug(Package.objects.all(), category_slug)
        result = []

        if slugs:
            for slug in slugs.split('|'):
                result.append(self.get_packages_by_topic_slug(packages, slug))

        #print ({'result': result})
        return {'result': result, 'type': cat}


class IosPcRankingPackageListWidget(BaseRankingPackageListWidget):

    template = 'pages/widgets/ios_pc/package_list_box_right.html'

    def get_list(self, type):
        from ranking.models import PackageRanking
        pkgRks = PackageRanking.objects.filter(cycle_type=0).filter(ranking_type__slug="total").filter(category__slug=type)
        if not pkgRks:
            return []
        else:
            return pkgRks[0].packages.all()

    def get_context(self, value=None, options=dict(), context=None):
        type = options.get('type', None)
        cat = 'application' if type == 'soft' else type
        items = self.get_list(cat)
        return {'items': items, 'type': type}

