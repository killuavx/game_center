# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from .masterpiece import MasterpiecePackageListWidget
from .common.topic import BaseTopicPackageListWidget
from .common.package import BaseRankingPackageListWidget


class BannerToprightWidget(BaseSingleAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_right.html'


class BannerTopleftWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/widgets/ios_pc/banner_top_left.html'


class PackageListBoxWidget(MasterpiecePackageListWidget):

    template = 'pages/widgets/ios_pc/roll_box.html'


class TopicPackageListBoxWidget(BaseTopicPackageListWidget):

    template = 'pages/widgets/ios_pc/package_list_box_left.html'

    def get_context(self, value=None, options=dict(), context=None):
        #print (options['slugs'])
        slugs =  options.get('slugs', None)
        type = options.get('type', None)
        result = []
        if slugs:
            slug_lst = slugs.split('|')
            for slug in slug_lst:
                #print (slug)
                new_options = options.copy()
                new_options['slug'] = slug
                #print (options)
                tmp = super(TopicPackageListBoxWidget, self).get_context(value, new_options, context)
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
        items = self.get_list(options.get('type', None))
        return {'items': items}

