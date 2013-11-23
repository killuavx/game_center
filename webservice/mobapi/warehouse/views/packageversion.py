# -*- coding: utf-8 -*-
from rest_framework import viewsets
from warehouse.models import PackageVersion
from mobapi.warehouse.serializers.packageversion import PackageVersionSerializer


class PackageVersionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = PackageVersion.objects.published()
    serializer_class = PackageVersionSerializer