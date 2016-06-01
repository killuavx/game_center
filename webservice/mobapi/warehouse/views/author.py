# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.decorators import link
from warehouse.models import Author
from mobapi.warehouse.serializers.author import AuthorSerializer
from mobapi.warehouse.views.package import PackageViewSet


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer

    model = Author

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Author.objects.activated()
        return self.queryset

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.get_queryset(), pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)