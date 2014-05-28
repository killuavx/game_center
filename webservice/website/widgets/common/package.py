# -*- coding: utf-8 -*-
from . import base


class BasePackageListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    ordering = ('-released_datetime', )

    def get_list(self):
        from warehouse.models import Package
        qs = Package.objects.all().published()
        return self.filter_queryset(qs)


