# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.pc import base
from website.widgets.common.promotion import BaseMultiAdvWidget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common.package import (
    BaseTopicalPackageListWidget,
    BaseRankingPackageListWidget,
    BaseComplexPackageListWidget)

__all__ = ['PCBannerWidget',
           'PCRollMasterpiecesWidget',
           'PCRollVendorsWidget',
           'PCHomeComplexPackageListWidget',
           'PCRankingPackageListWidget',
           ]


class PCBannerWidget(BaseMultiAdvWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/banner.haml'


class PCRollAdvertisementsWidget(BaseMultiAdvWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollVendorsWidget(BaseTopicAuthorPanelWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollMasterpiecesWidget(BaseTopicalPackageListWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCHomeComplexPackageListWidget(BaseComplexPackageListWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/home-complex-package-list-panel.haml'


class PCRankingPackageListWidget(BaseRankingPackageListWidget, base.ProductPropertyWidgetMixin, Widget):

    template = 'pages/pc/widgets/ranking-package-list-panel.haml'
