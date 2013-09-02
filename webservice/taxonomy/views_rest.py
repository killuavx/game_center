# -*- encoding=utf-8 -*-
from taxonomy.models import Category
from tagging.models import Tag
from taxonomy.serializers import CategoryDetailSerializer, CategorySummarySerializer
from rest_framework import viewsets

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySummarySerializer

    def retrieve(self, request, *args, **kwargs):
        list_serializer_class = self.serializer_class

        self.serializer_class = CategoryDetailSerializer
        response = super(CategoryViewSet, self).retrieve(request, *args, **kwargs)
        self.serializer_class = list_serializer_class
        return response

