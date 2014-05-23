# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseMultiAdvWidget


class HomeTopBannersWidget(BaseMultiAdvWidget, Widget):

   template='pages/widgets/android/home-top-banner.html'
