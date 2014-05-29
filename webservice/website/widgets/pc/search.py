# -*- coding: utf-8 -*-
from django_widgets import Widget
from website.widgets.common.package import SolrPackageSearchFilterBackend, BasePackageListWidget

__all__ = ['PCSearchPackageListWidget']

class PCSearchPackageListWidget(BasePackageListWidget, Widget):

    search_param = 'q'
    q = None

    filter_backends = (SolrPackageSearchFilterBackend, )

    def get_list(self):
        queryset = self.get_queryset()
        if not self.q:
            return queryset.none()
        return super(PCSearchPackageListWidget, self).get_list()

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.q = options.get(self.search_param)
        print(type(self.q), self.q)
        return super(PCSearchPackageListWidget, self).get_context(value=value,
                                                                  options=options,
                                                                  context=context,
                                                                  pagination=pagination)


