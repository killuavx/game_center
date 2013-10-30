# -*- coding: utf-8 -*-
from django.utils import importlib


def import_from(fullname):
    if callable(fullname):
        return fullname
    splited = fullname.split('.')
    classname = splited[-1]
    packagename = ".".join(splited[:-1])
    return getattr(importlib.import_module(packagename), classname)

