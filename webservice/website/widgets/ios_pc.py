# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from .masterpiece import MasterpiecePackageListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget
from taxonomy.models import Topic
from warehouse.models import Package


class BannerToprightWidget(BaseSingleAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_right.html'


class BannerTopleftWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_left.html'


def filter_packages_by_category(packages, category, limit=12):
    items = []

    for pkg in packages:
        for cat in pkg.categories.all():
            #if category in cat.slug:
            if cat.get_root().slug == category:
                items.append(pkg)
                if len(items) >= limit:
                    return items
                else:
                    break
    return items


class PackageListRollBoxWidget(MasterpiecePackageListWidget):

    template = 'pages/widgets/ios_pc/roll_box.html'

    def get_context(self, value=None, options=dict(), context=None):
        type = options.get('type', None)
        cat = 'application' if type == 'soft' else type
        tmp = super(PackageListRollBoxWidget, self).get_context(value, options, context)
        tmp['items']  = filter_packages_by_category(tmp['items'], cat)

        return tmp



class TopicPackageListBoxWidget(BaseTopicPackageListWidget):

    template = 'pages/widgets/ios_pc/package_list_box_left.html'

    def get_context(self, value=None, options=dict(), context=None):
        slugs =  options.get('slugs', None)
        type = options.get('type', None)
        cat = 'application' if type == 'soft' else type
        result = []

        if slugs:
            slug_lst = slugs.split('|')
            for slug in slug_lst:
                #print (slug)
                if slug == 'latest_published':
                    packages =  Package.objects.all().by_published_order()
                    items = filter_packages_by_category(packages, cat)
                    tmp = {}
                    tmp['items'] = items
                    tmp['topic_name']  = '最新发布'
                    result.append(tmp)
                else:
                    new_options = options.copy()
                    new_options['slug'] = slug
                    tmp = super(TopicPackageListBoxWidget, self).get_context(value, new_options, context)
                    tmp['items'] = filter_packages_by_category(tmp['items'], cat)
                    try:
                        topic = Topic.objects.filter(slug=self.slug).published().get()
                        tmp['topic_name']  = topic.name
                    except:
                        pass
                    #print (tmp)
                    result.append(tmp)

        #print ({'result': result})
        return {'result': result, 'type': type}


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

