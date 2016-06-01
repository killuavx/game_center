# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.decorators import link
from warehouse.models import Author
from mobapi2.warehouse.serializers.author import AuthorSerializer
from mobapi2.warehouse.views.package import PackageViewSet
from rest_framework_extensions.cache.decorators import cache_response
from mobapi2 import cache_keyconstructors as ckc
from rest_framework_extensions.utils import default_list_cache_key_func, default_object_cache_key_func
from mobapi2.warehouse.views.filters import TopicalAuthorFilter
from mobapi2.decorators import default_cache_control
from rest_framework_extensions.etag.decorators import etag


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    filter_backends = (TopicalAuthorFilter, )

    model = Author

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
        return self.queryset

    packages_key_func = ckc.LookupOrderingListKeyConstructor()

    @etag(packages_key_func)
    @cache_response(key_func=packages_key_func)
    @default_cache_control()
    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.get_queryset(), pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.all()
        list_view = ViewSet.as_view({'get': 'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)


    @etag(default_list_cache_key_func)
    @cache_response(key_func=default_list_cache_key_func)
    @default_cache_control()
    def list(self, request, *args, **kwargs):
        return super(AuthorViewSet, self).list(request, *args, **kwargs)


    @etag(default_object_cache_key_func)
    @cache_response(key_func=default_object_cache_key_func)
    @default_cache_control()
    def retrieve(self, request, *args, **kwargs):
        return super(AuthorViewSet, self).retrieve(request, *args, **kwargs)