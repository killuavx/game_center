# -*- coding: utf-8 -*-
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist
from easy_thumbnails.exceptions import InvalidImageFormatError

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import (
    ModelSerializer as RFModelSerializer,
    ModelSerializerOptions,
    HyperlinkedModelSerializerOptions,
    HyperlinkedModelSerializer as RFHyperlinkedModelSerializer)
from django.db import models

from mobapi2.rest_router import rest_router
from mobapi2.rest_fields import DateTimeField
from mobapi2.settings import GC_RESOURCE_ALIAS, IMAGE_COVER_SIZE
from toolkit.helpers import import_from


class GetResourceFileMixin(object):

    def get_resource(self, inst_resources, kind, alias='default'):
        return getattr(inst_resources, kind)[alias].file


class ModelGetResourceMixin(GetResourceFileMixin):

    DEFAULT_COVER_SIZE = IMAGE_COVER_SIZE

    def get_cover(self, obj):
        try:
            file = self.get_resource(obj.resources, 'cover', GC_RESOURCE_ALIAS)
            return file.url
        except ObjectDoesNotExist:
            return self.get_default_cover(obj)

    def get_default_cover(self, obj):
        try:
            return obj.cover[self.DEFAULT_COVER_SIZE].url
        except (ValueError, KeyError, InvalidImageFormatError):
            return None


class ModelSerializerWithRouterOptions(ModelSerializerOptions):

    def __init__(self, meta):
        self.router = getattr(meta, 'router', rest_router)
        super(ModelSerializerWithRouterOptions, self).__init__(meta)


_serializer_field_mapping = deepcopy(RFModelSerializer.field_mapping)
_serializer_field_mapping.update({
    models.DateTimeField: DateTimeField
})


class ModelWithRouterSerializer(RFModelSerializer):

    field_mapping = _serializer_field_mapping

    _options_class = ModelSerializerWithRouterOptions


ModelSerializer = ModelWithRouterSerializer


class HyperlinkedModelSerializerWithRouterOptions(HyperlinkedModelSerializerOptions):

    def __init__(self, meta):
        self.router = getattr(meta, 'router', rest_router)
        super(HyperlinkedModelSerializerWithRouterOptions, self).__init__(meta)


_hlink_serializer_field_mapping = deepcopy(RFHyperlinkedModelSerializer.field_mapping)
_hlink_serializer_field_mapping.update({
    models.DateTimeField: DateTimeField
})


class HyperlinkedWithRouterModelSerializer(RFHyperlinkedModelSerializer):

    field_mapping = _hlink_serializer_field_mapping

    _options_class = HyperlinkedModelSerializerWithRouterOptions

    def _get_default_view_name(self, model):
        view_name = super(HyperlinkedWithRouterModelSerializer, self)\
            ._get_default_view_name(model)
        return self.opts.router.get_base_name(view_name)


HyperlinkedModelSerializer = HyperlinkedWithRouterModelSerializer


class HyperlinkedSearchSerializerWithRouterOptions(serializers.SerializerOptions):

    def __init__(self, meta):
        self.model = getattr(meta, 'model', None)
        self.router = getattr(meta, 'router', rest_router)
        self.view_name = getattr(meta, 'view_name', None)
        self.lookup_field = getattr(meta, 'lookup_field', None)
        super(HyperlinkedSearchSerializerWithRouterOptions, self).__init__(meta)


class HyperlinkedSearchSerializer(serializers.Serializer):

    field_mapping = _hlink_serializer_field_mapping

    _options_class = HyperlinkedSearchSerializerWithRouterOptions
    _default_view_name = '%(model_name)s-detail'

    def get_default_fields(self):
        fields = super(HyperlinkedSearchSerializer, self).get_default_fields()

        if self.opts.view_name is None:
            self.opts.view_name = self._get_default_view_name(self.opts.model)

        if 'url' not in fields:
            url_field = HyperlinkedIdentityField(
                view_name=self.opts.view_name,
                lookup_field=self.opts.lookup_field
            )
            ret = self._dict_class()
            ret['url'] = url_field
            ret.update(fields)
            fields = ret
        return fields

    def _get_default_view_name(self, search):
        format_kwargs = {
            'model_name': search._module_name()
        }
        view_name = self._default_view_name % format_kwargs
        return self.opts.router.get_base_name(view_name)

    def get_identity(self, data):
        """
        This hook is required for bulk update.
        We need to override the default, to use the url as the identity.
        """
        try:
            return data.get('url', None)
        except AttributeError:
            return None


class SerializerRelatedField(serializers.RelatedField):

    serializer_class = None

    def __init__(self, serializer_class, *args, **kwargs):
        self.serializer_class = serializer_class
        super(SerializerRelatedField, self).__init__(*args, **kwargs)

    def get_serializer_class(self):
        if isinstance(self.serializer_class, str):
            self.serializer_class = import_from(self.serializer_class)
        return self.serializer_class

    def to_native(self, value):
        return self.get_serializer_class()(value,
                                     many=self.many,
                                     context=self.context).data


from rest_framework.pagination import PaginationSerializer, PaginationSerializerOptions


class PaginationSerializerWithRouterOptions(PaginationSerializerOptions):

    def __init__(self, meta):
        self.router = getattr(meta, 'router', rest_router)
        super(PaginationSerializerWithRouterOptions, self).__init__(meta)


class NotePaginationSerializer(PaginationSerializer):

    _options_class = PaginationSerializerWithRouterOptions

    note_url = serializers.SerializerMethodField('get_note_url')

    def get_note_url(self, obj):
        raise NotImplementedError
