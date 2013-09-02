# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author

from rest_framework import viewsets
from warehouse.serializers import PackageSummarySerializer,\
    PackageDetailSerializer,\
    AuthorSerializer

# ViewSets define the view behavior.
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.filter(status=Package.STATUS.published).all()
    serializer_class = PackageSummarySerializer

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class

        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.filter(status=Author.STATUS.activated).all()
    serializer_class = AuthorSerializer
