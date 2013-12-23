# -*- coding: utf-8 -*-
from rest_framework import serializers
from analysis.documents.event import Event
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _


class DocumentSerializer(serializers.Serializer):

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            [setattr(instance, key, value) for key, value in attrs.items()]
        return instance


def choices_validate(choise_dict, attrs, source,
                     validation_error_class=exceptions.ValidationError):
    value = attrs[source]
    if value not in choise_dict:
        raise validation_error_class(
            _('Value must be one of %s' % list(choise_dict.keys())
            ))
    return attrs


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

    def validate_eventtype(self, attrs, source):
        return choices_validate(
            attrs=attrs,
            source=source,
            choise_dict=dict(Event.EVENT_TYPES),
            validation_error_class=serializers.ValidationError)

    def validate_entrytype(self, attrs, source):
        return choices_validate(
            attrs=attrs,
            source=source,
            choise_dict=dict(Event.ENTRY_TYPES),
            validation_error_class=serializers.ValidationError)
