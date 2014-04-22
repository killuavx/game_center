# -*- coding: utf-8 -*-
from django_widgets import Widget
from .common.category import BaseTopicAuthorPackageListWidget


class DeveloperPackageShowcaseWidget(BaseTopicAuthorPackageListWidget, Widget):

    template = 'pages/widgets/developers_package_page.haml'

