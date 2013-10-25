# -*- coding: utf-8 -*-
__author__ = 'me'
from behave.matchers import register_type

def str2empty(s):
    if s.upper() == 'NONE':
        return None
    else:
        return s

register_type(emptys=str2empty)

def in2boolean(s):
    is_ = s.split(" ")
    if is_[0].lower() == 'not':
        return False
    else:
        return True

register_type(inb=in2boolean)
