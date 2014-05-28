# -*- coding: utf-8 -*-
from django_widgets import Widget


class PackageSummaryWidget(Widget):

    template = 'pages/widgets/packages/summary-panel.haml'

    def get_context(self, value=None, options=dict(), context=dict()):
        return options


class PackageSharePanelWidget(Widget):

    template = 'pages/widgets/packages/share-panel.haml'

    def get_context(self, value=None, options=dict(), context=dict()):
        return options


class PackageRelatedListPanelWidget(Widget):

    template = 'pages/widgets/packages/related-package-panel.haml'

    def get_context(self, value=None, options=dict(), context=dict()):
        return options


class PackageMoreDetailWidget(Widget):

    template = 'pages/widgets/packages/detail-panel.html'

    def get_context(self, value=None, options=dict(), context=dict()):
        return options

class PackagePostPanelWidget(Widget):

    template = 'pages/widgets/packages/post-panel.html'

    def get_context(self, value=None, options=dict(), context=dict()):
        return options
