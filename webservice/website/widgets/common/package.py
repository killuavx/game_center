# -*- coding: utf-8 -*-
from . import base


class BasePackageListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    ordering = ('-released_datetime', )

    def get_list(self):
        from warehouse.models import Package
        qs = Package.objects.all().published()
        return self.filter_queryset(qs)


class BasePackageVersionListWidget(base.BaseListWidget):

    def get_list(self):
        qs = Package.objects.published()
        return PackageVersion.objects.filter(package__in=qs).by_published_order(True)


class BaseRankingPackageListWidget(BasePackageListWidget):

    def get_list(self):
        return Package.objects.published().by_rankings_order()

