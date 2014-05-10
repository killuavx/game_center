# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ModelSerializerOptions,
    HyperlinkedModelSerializerOptions,
    HyperlinkedModelSerializer)
from mobapi2.rest_router import rest_router
from toolkit.helpers import import_from


class ModelSerializerWithRouterOptions(ModelSerializerOptions):

    def __init__(self, meta):
        self.router = getattr(meta, 'router', rest_router)
        super(ModelSerializerWithRouterOptions, self).__init__(meta)


class ModelWithRouterSerializer(ModelSerializer):

    _options_class = ModelSerializerWithRouterOptions


class HyperlinkedModelSerializerWithRouterOptions(HyperlinkedModelSerializerOptions):

    def __init__(self, meta):
        self.router = getattr(meta, 'router', rest_router)
        super(HyperlinkedModelSerializerWithRouterOptions, self).__init__(meta)


class HyperlinkedWithRouterModelSerializer(HyperlinkedModelSerializer):

    _options_class = HyperlinkedModelSerializerWithRouterOptions

    def _get_default_view_name(self, model):
        view_name = super(HyperlinkedWithRouterModelSerializer, self)\
            ._get_default_view_name(model)
        return self.opts.router.get_base_name(view_name)


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