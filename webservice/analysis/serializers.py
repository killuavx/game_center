# -*- coding: utf-8 -*-
from rest_framework import serializers
from analysis.documents.event import Event


class DocumentSerializer(serializers.Serializer):

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            [setattr(instance, key, value) for key, value in attrs.items()]
        return instance


class EventSerializer(DocumentSerializer):

    imei = serializers.CharField()

    eventtype = serializers.CharField()

    entrytype = serializers.CharField()

    class Meta:
        model = Event
        fields = (
            'imei',
            'eventtype',
            'entrytype',
        )
