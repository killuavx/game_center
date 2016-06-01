# -*- coding: utf-8 -*-
from haystack.fields import CharField, FacetField


class CharGeneralField(CharField):
    field_type = 'text_general'

    def __init__(self, **kwargs):
        if kwargs.get('facet_class') is None:
            kwargs['facet_class'] = FacetCharGeneralField

        super(CharGeneralField, self).__init__(**kwargs)


class FacetCharGeneralField(FacetField, CharGeneralField):
    pass
