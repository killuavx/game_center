# -*- coding: utf-8 -*-
import copy
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from warehouse.models import PackageVersion
from mobapi2.warehouse.serializers.packageversion import (
    PackageVersionSummarySerializer,
    PackageVersionDetailSerializer,
)
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.utils import (
    default_list_cache_key_func,
    default_object_cache_key_func)
from rest_framework_extensions.etag.decorators import etag
from mobapi2.decorators import default_cache_control


class PackageVersionViewSet(viewsets.ReadOnlyModelViewSet):

    model = PackageVersion

    serializer_class = PackageVersionSummarySerializer

    filter_backends = (filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filter_fields = ('package', )
    ordering = ('-version_code', )

    def get_queryset(self):
        return self.model.objects.published()

    @etag(default_object_cache_key_func)
    @cache_response(key_func=default_object_cache_key_func)
    @default_cache_control()
    def retrieve(self, request, *args, **kwargs):
        list_serializer_class, self.serializer_class = \
            self.serializer_class, PackageVersionDetailSerializer
        response = super(PackageVersionViewSet, self)\
            .retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

    @etag(default_list_cache_key_func)
    @cache_response(key_func=default_list_cache_key_func)
    @default_cache_control()
    def list(self, request, *args, **kwargs):
        querydict = copy.deepcopy(dict(request.GET))
        q = querydict.get('package')
        q = q.pop() if isinstance(q, list) else q
        if not q or not (q and q.strip()):
            data = {'detail': 'Not Allow without package parameter'
                              ' /api/packageversions/?package={package_pk}'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return super(PackageVersionViewSet, self).list(request, *args, **kwargs)

