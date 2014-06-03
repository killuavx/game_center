# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BaseRankingPackageListWidget

__all__ = ['WebRankingDetailPackageListWidget']


class WebRankingDetailPackageListWidget(BaseRankingPackageListWidget, Widget):

    per_page = 10

    template = 'pages/widgets/ranking/ranking-list.haml'

    def get_title(self):
        try:
            return self.ranking.ranking_type.title
        except:
            return None
