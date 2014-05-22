# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
from rest_framework_extensions.key_constructor import (bits,
                                                       constructors)




class OrderingKeyBit(bits.QueryParamsKeyBit):

    def get_data(self, **kwargs):
        kwargs['params'] = []
        if hasattr(kwargs['view_instance'], 'ordering'):
            kwargs['params'].append('ordering')
        return super(OrderingKeyBit, self).get_data(**kwargs)


class LookupKeyBit(bits.KeyBitBase):

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        lookup_value = view_instance.kwargs[view_instance.lookup_field]
        return force_text(lookup_value)


class LookupListKeyConstructor(constructors.DefaultKeyConstructor):
    lookup = LookupKeyBit()
    pagination = bits.PaginationKeyBit()


class LookupOrderingListKeyConstructor(LookupListKeyConstructor):
    ordering = OrderingKeyBit()
