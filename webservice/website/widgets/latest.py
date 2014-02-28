# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.promotion import BaseSingleAdvWidget
from .common.package import BasePackageListWidget, BasePackageVersionListWidget

class LatestSingleAdvWidget(BaseSingleAdvWidget, Widget):

    template = 'pages/widgets/latest/single-adv.haml'


class LatestPackageTimelinePanelWidget(BasePackageListWidget):

    title = '首发时间线'

    template = 'pages/widgets/latest/package-timeline-list.haml'

class LatestPackageVersionListWidget(BasePackageVersionListWidget):

    template = 'pages/widgets/latest/packageversion-list.haml'
