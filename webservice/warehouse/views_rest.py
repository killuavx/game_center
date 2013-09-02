# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author

from rest_framework import viewsets
from warehouse.serializers import PackageSerializer, AuthorSerializer

# ViewSets define the view behavior.
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(status=Package.STATUS.published).all()
    serializer_class = PackageSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.filter(status=Author.STATUS.activated).all()
    serializer_class = AuthorSerializer
