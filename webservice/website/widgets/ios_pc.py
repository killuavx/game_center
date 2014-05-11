# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from .masterpiece import MasterpiecePackageListWidget
from .common.topic import BaseTopicPackageListWidget


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
                options['slug'] = slug
                tmp = super(TopicPackageListBoxWidget, self).get_context(value, options, context)
                result.append(tmp)

        #print ({'result': result})
        return {'result': result, 'type': type}


#class IosPcRankingPackageListWidget(BasePackageListWidget):
#
##    def get_list(self):
##        PackageRanking.objects.
#
#
#    template = 'pages/widgets/ios_pc/package_list_box_right.html'
