# -*- coding: utf-8 -*-
__author__ = 'me'
from behave.matchers import register_type

def str2empty(s):
    if s.upper() == 'NONE':
        return None
    else:
        return s

register_type(emptys=str2empty)
