# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.decorators import link
from warehouse.models import Author
from mobapi.warehouse.serializers.author import AuthorSerializer
from mobapi.warehouse.views.package import PackageViewSet


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.activated()
    serializer_class = AuthorSerializer

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.queryset, pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.published()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)