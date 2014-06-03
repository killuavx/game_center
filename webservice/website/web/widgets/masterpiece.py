# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import BaseTopicalPackageListWidget
from website.web.widgets.base import ProductPropertyWidgetMixin

__all__ = ['WebMasterpiecePackageListWidget']


class WebMasterpiecePackageListWidget(BaseTopicalPackageListWidget,
                                      ProductPropertyWidgetMixin,
                                      Widget):
    pass
