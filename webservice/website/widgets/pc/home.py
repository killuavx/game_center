# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django_widgets import Widget
from website.widgets.common.base import PaginatorPageMixin
from website.widgets.common.promotion import BaseMultiAdvWidget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common.topic import BaseTopicPackageListWidget
from website.widgets.pc.base import BaseComplexPackageListWidget

__all__ = ['PCBannerWidget',
           'PCRollMasterpiecesWidget',
           'PCRollVendorsWidget',
           'PCHomeComplexPackageListWidget',
           'PCRankingPackageListWidget',
           ]

class PCBannerWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/pc/widgets/banner.haml'


class PCRollAdvertisementsWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollVendorsWidget(BaseTopicAuthorPanelWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollMasterpiecesWidget(BaseTopicPackageListWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCHomeComplexPackageListWidget(BaseComplexPackageListWidget, Widget):

    template = 'pages/pc/widgets/home-complex-package-list-panel.haml'


class PCRankingPackageListWidget(PaginatorPageMixin, Widget):

    template = 'pages/pc/widgets/ranking-package-list-panel.haml'

    ranking_slug = 'main'

    cat_slug = None

    ranking = None

    def get_list(self):
        from warehouse.models import Package
        return Package.objects.filter(rankings__pk=self.ranking.pk)

    def get_ranking(self, cat_slug, ranking_slug, cycle_type=0):
        from ranking.models import PackageRanking
        return PackageRanking.objects.get(ranking_type__slug=ranking_slug,
                                          category__slug=cat_slug,
                                          cycle_type=cycle_type)


    def get_context(self, value, options):
        self.per_page, cur_page = self.get_paginator_vars(options)

        self.cat_slug = options.get('cat_slug')
        self.ranking = self.get_ranking(self.cat_slug, self.ranking_slug)
        paginator = Paginator(self.get_list(), self.per_page)

        data = dict(
            ranking=self.ranking,
            items=paginator.page(cur_page)
        )
        return data

