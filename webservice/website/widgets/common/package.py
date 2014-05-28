# -*- coding: utf-8 -*-
from warehouse.models import Package, PackageVersion
from . import base


class BasePackageListWidget(base.BaseListWidget):

    def get_list(self):
        return Package.objects.all()


class BasePackageVersionListWidget(base.BaseListWidget):

    def get_list(self):
        qs = Package.objects.published()
        return PackageVersion.objects.filter(package__in=qs).by_published_order(True)


class BaseRankingPackageListWidget(BasePackageListWidget):

    def get_list(self):
        return Package.objects.published().by_rankings_order()

