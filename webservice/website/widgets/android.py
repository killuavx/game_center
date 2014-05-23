# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseMultiAdvWidget
from .masterpiece import MasterpiecePackageListWidget


class HomeTopBannersWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/home-top-banner.html'

class HomeMasterpiecePackageListWidget(MasterpiecePackageListWidget):

    per_page = 10
    template = 'pages/widgets/android/masterpiece.html'

