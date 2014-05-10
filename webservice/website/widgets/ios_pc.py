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

#    def get_context(self, value=None, options=dict(), context=None):
#        pass
