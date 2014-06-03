# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.promotion import BaseSingleAdvWidget, BaseMultiAdvWidget
from website.widgets.common import package as pkgwidget
from website.widgets.common import topic as tpwidget
from website.widgets.common.webspide import BaseForumThreadPanelWdiget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from . import base

__all__ = ['WebHomeTopBannersWidget',
           'WebHomeTopicalPackageListWidget',
           'WebHomeMasterpiecePackageListWidget',
           'WebHomeLatestPackageListWidget',
           'WebSingleAdvertisementWidget',
           'WebHomeComplexPackagePanelWidget',
           'WebRankingPackageListWidget',
           'WebHomeForumHotThreadPanelWidget',
           'WebHomeForumNoviceThreadPanelWidget',
           'WebHomeVendorListWidget',
           'WebHomeCollectionListWidget',
           ]


class WebHomeTopBannersWidget(BaseMultiAdvWidget,
                              base.ProductPropertyWidgetMixin,
                              Widget):

    template='pages/widgets/home/banner.haml'


class WebHomeMasterpiecePackageListWidget(pkgwidget.BaseTopicalPackageListWidget,
                                          base.ProductPropertyWidgetMixin,
                                          Widget):

    per_page = 10

    template='pages/widgets/home/roll-masterpiece.haml'


class WebHomeLatestPackageListWidget(pkgwidget.BasePackageListWidget,
                                     base.ProductPropertyWidgetMixin,
                                     Widget):
    pass


class WebHomeTopicalPackageListWidget(pkgwidget.BaseTopicalPackageListWidget,
                                      base.ProductPropertyWidgetMixin,
                                      Widget):
    pass


class WebSingleAdvertisementWidget(BaseSingleAdvWidget,
                                   base.ProductPropertyWidgetMixin,
                                   Widget):

    template = 'pages/widgets/common/single-adv.haml'


class WebHomeComplexPackagePanelWidget(pkgwidget.BaseComplexPackageListWidget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):

    template = 'pages/widgets/home/complex-package-panel.haml'


class WebRankingPackageListWidget(pkgwidget.BaseRankingPackageListWidget,
                                  base.ProductPropertyWidgetMixin,
                                  Widget):

    template = 'pages/widgets/common/ranking-list.haml'

    def get_title(self):
        return self.ranking.ranking_type.title

    def get_more_url(self):
        return self.ranking.get_absolute_url_as(product=self.product)


class WebHomeCollectionListWidget(tpwidget.BaseTopicListWidget,
                                  base.ProductPropertyWidgetMixin,
                                  Widget):

    template = 'pages/widgets/home/roll-collections.haml'


class WebHomeForumHotThreadPanelWidget(BaseForumThreadPanelWdiget,
                                       base.ProductPropertyWidgetMixin,
                                       Widget):

    title = '热帖'

    per_page = 12

    template = 'pages/widgets/home/forum-hot-list.haml'


class WebHomeForumNoviceThreadPanelWidget(BaseForumThreadPanelWdiget,
                                          base.ProductPropertyWidgetMixin,
                                          Widget):

    title = '新手'

    per_page = 12

    template = 'pages/widgets/home/forum-novice-list.haml'


class WebHomeVendorListWidget(BaseTopicAuthorPanelWidget,
                              base.ProductPropertyWidgetMixin,
                              Widget):

    template = 'pages/widgets/home/vendor-list.haml'

    title = '厂商'

    def get_more_url(self):
        return self.get_model().page_absolute_url_as(self.product)

