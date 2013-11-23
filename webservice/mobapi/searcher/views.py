# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets, filters
from searcher.models import TipsWord
from mobapi.searcher.serializers import TipsWordSerializer


class TipsWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TipsWordSerializer
    queryset = TipsWord.objects.published().order_weight()
    filter_backends = (
        filters.OrderingFilter,
    )

