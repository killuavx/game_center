# -*- encoding=utf-8 -*-
from taxonomy.models import Category
from tagging.models import Tag
from taxonomy.serializers import CategorySerializer
from rest_framework import viewsets

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

