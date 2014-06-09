# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BaseTopicalPackageListWidget
from website.widgets.pc.base import ProductPropertyWidgetMixin

__all__ = ['PCMasterpiecePackageListWidget']


class PCMasterpiecePackageListWidget(BaseTopicalPackageListWidget,
                                     ProductPropertyWidgetMixin,
                                     Widget):
    pass
