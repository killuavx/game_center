# -*- coding: utf-8 -*-
from copy import deepcopy
from rest_framework import serializers
from analysis.documents.event import Event
from analysis.tasks import record_event, event_fields_datetime_format_to_isostring
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class DocumentSerializer(serializers.Serializer):

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            [setattr(instance, key, value) for key, value in attrs.items()]
            return instance
        return attrs


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


class EventCreateSerializer(EventSerializer):

    def set_request_datas(self, request):
        if request and self.object:
            self.object.user = request.user
            if hasattr(request, 'get_client_ip'):
                self.object.client_ip = request.get_client_ip()
                self.object.domain = request.get_host()

    def save_object(self, obj, **kwargs):
        _data = deepcopy(obj._data)
        if not getattr(obj, 'created_datetime', None):
            obj.created_datetime = now().astimezone()
        event_fields_datetime_format_to_isostring(_data)
        record_event.delay(**_data)
        #record_event.apply_async(kwargs=_data, retry=False)


class DownloadEventCreateSerializer(EventCreateSerializer):

    imei = serializers.CharField(default='', required=False)

    eventtype = serializers.CharField(default='download', required=False)

    entrytype = serializers.CharField(default='web', required=False)

    download_package_name = serializers.CharField(required=True)

    download_version_name = serializers.CharField(required=True)

    @classmethod
    def factory_serializer(cls, instance=None, data=None, request=None, response=None):
        if data and not instance:
            instance = cls.Meta.model(**data)
        obj = cls(instance=instance, data=data)
        obj.set_request_datas(request)
        obj.set_response_datas(response)
        return obj

    def set_request_datas(self, request):
        super(DownloadEventCreateSerializer, self).set_request_datas(request)
        if request and self.object:
            self.object.current_uri = request.build_absolute_uri()
            self.object.referer = request.META.get('HTTP_REFERER')

    def set_response_datas(self, response):
        if response and self.object:
            self.object.redirect_to = response.get('Location')

    def save_object(self, obj, **kwargs):
        # FIX client 2.2 bug
        if obj.entrytype == 'client':
            if not hasattr(obj, 'package_name'):
                setattr(obj, 'package_name', 'com.lion.market')
        #obj.eventtype = 'download'
        super(DownloadEventCreateSerializer, self).save_object(obj, **kwargs)

