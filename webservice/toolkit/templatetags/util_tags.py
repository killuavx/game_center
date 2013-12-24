# -*- coding: utf-8 -*-
from django.template.base import Library, VariableDoesNotExist, Variable
import datetime

register = Library()

@register.assignment_tag()
def resolve(lookup, target):
    try:
        return Variable(lookup).resolve(target)
    except VariableDoesNotExist:
        return None


@register.filter
def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)
