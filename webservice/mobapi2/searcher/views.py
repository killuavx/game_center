# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets, filters
from searcher.models import TipsWord
from mobapi2.searcher.serializers import TipsWordSerializer


class TipsWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TipsWordSerializer
    model = TipsWord
    filter_backends = (
        filters.OrderingFilter,
    )

    def get_queryset(self):
        if not self.queryset:
            self.queryset = self.model.objects.published()
        return self.queryset.order_weight()


