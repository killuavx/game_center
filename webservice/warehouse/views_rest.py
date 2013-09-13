# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author
from rest_framework.decorators import link
from rest_framework import (viewsets,
                            generics,
                            filters)
from warehouse.serializers import (PackageSummarySerializer,
                                   PackageDetailSerializer,
                                   AuthorSerializer)

# ViewSets define the view behavior.
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.published()
    serializer_class = PackageSummarySerializer
    filter_backends = (filters.OrderingFilter,
                       filters.DjangoFilterBackend,
    )
    filter_fields = ('package_name', 'title',)
    ordering = ('title',
                'package_name',
                'updated_datetime',
                'released_datetime' )

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class
        self.serializer_class = PackageDetailSerializer
        response = super(PackageViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.activated()
    serializer_class = AuthorSerializer

    @link()
    def packages(self, request, pk, *args, **kwargs):
        author = generics.get_object_or_404(self.queryset, pk=pk)
        ViewSet = PackageViewSet
        queryset = author.packages.published()
        list_view =  ViewSet.as_view({'get':'list'}, queryset=queryset)
        return list_view(request, *args, **kwargs)
