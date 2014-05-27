# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.decorators import link
from warehouse.models import Author
from mobapi2.warehouse.serializers.author import AuthorSerializer
from mobapi2.warehouse.views.package import PackageViewSet
from rest_framework_extensions.cache.decorators import cache_response
from mobapi2 import cache_keyconstructors as ckc
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from mobapi2.warehouse.views.filters import TopicalAuthorFilter


class AuthorViewSet(CacheResponseMixin,
                    viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    filter_backends = (TopicalAuthorFilter, )

    model = Author

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.get_queryset(), pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.all()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)