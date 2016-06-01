# -*- coding: utf-8 -*-
from rest_framework import serializers
from searcher.models import TipsWord


class TipsWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsWord
        fields = ('keyword',
                  'weight')

