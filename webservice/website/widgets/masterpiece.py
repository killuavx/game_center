# -*- coding: utf-8 -*-
from .common.topic import BaseTopicPackageListWidget, BaseTopicInformationWidget


class MasterpieceInformationWidget(BaseTopicInformationWidget):

    template = 'pages/widgets/masterpiece/information.haml'


class MasterpiecePackageListWidget(BaseTopicPackageListWidget):

    per_page = 8

    template = 'pages/widgets/masterpiece/package-list.haml'


