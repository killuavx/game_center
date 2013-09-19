# -*- encoding: utf-8-*-
from rest_framework import (viewsets,
                            mixins)

from searcher.models import TipsWord
from searcher.serializers import TipsWordSerializer

class TipsWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TipsWordSerializer
    queryset = TipsWord.objects.published()



