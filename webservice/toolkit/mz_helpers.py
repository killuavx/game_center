# -*- coding: utf-8 -*-
from mezzanine.conf import registry, register_setting as mz_register_setting


def register_setting(name="", label="", editable=False, description="",
                     default=None, choices=None, append=False, **kwargs):
    mz_register_setting(name=name, label=label,
                        editable=editable, description=description,
                        default=default, choices=choices, append=append)
    if 'widget' in kwargs:
        registry[name]['widget'] = kwargs.get('widget')


