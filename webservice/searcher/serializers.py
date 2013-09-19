# -*- encoding: utf-8-*-
from searcher.models import TipsWord
from rest_framework import serializers

class TipsWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsWord
        fields = ( 'keyword',
                  'weight' )

