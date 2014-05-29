# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BasePackageSearchListWidget

__all__ = ['PCSearchPackageListWidget']


class PCSearchPackageListWidget(BasePackageSearchListWidget, Widget):
    search_param = 'q'

