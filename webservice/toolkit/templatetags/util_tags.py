# -*- coding: utf-8 -*-
from django.template import defaultfilters
from django.template.base import Library, VariableDoesNotExist, Variable
import datetime
from django.conf import settings

register = Library()

@register.assignment_tag()
def resolve(lookup, target):
    """
    {% resolve some_list some_index as value %}
    {% resolve some_dict some_dict_key as value %}
    """
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


@register.filter
def partition(thelist, n):
    """
    Template tags for working with lists.
    You'll use these in templates thusly::

        {% for sublist in mylist|parition:"3" %}
            {% for item in mylist %}
                do something with {{ item }}
            {% endfor %}
        {% endfor %}

    Break a list into ``n`` pieces. The last list may be larger than the rest if
    the list doesn't break cleanly. That is::

        >>> l = range(10)

        >>> partition(l, 2)
        [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

        >>> partition(l, 3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

        >>> partition(l, 4)
        [[0, 1], [2, 3], [4, 5], [6, 7, 8, 9]]

        >>> partition(l, 5)
        [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    p = len(thelist) / n
    return [thelist[p*i:p*(i+1)] for i in range(n - 1)] + [thelist[p*(i+1):]]

@register.filter
def partition_horizontal(thelist, n):
    """
    Break a list into ``n`` peices, but "horizontally." That is,
    ``partition_horizontal(range(10), 3)`` gives::

        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9],
         [10]]

    Clear as mud?
    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    newlists = [list() for i in range(n)]
    for i, val in enumerate(thelist):
        newlists[i%n].append(val)
    return newlists


intwordcn_converters = (
    (4, lambda number: (
        '%(value).1f 万',
        '%(value)s 万',
    )),
    (8, lambda number: (
        '%(value).1f 亿',
        '%(value)s 亿',
    )),
    (12, lambda number: (
        '%(value).1f 兆',
        '%(value)s 兆',
    )),
)

from decimal import Decimal

@register.filter
def intwordcn(value):
    """
        same to intword
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 10000:
        return value

    def _check_for_float(value, float_formatted, string_formatted):
        """
        Use the i18n enabled defaultfilters.floatformat if possible
        """
        value = defaultfilters.floatformat(value)
        value = Decimal(value)
        if value - int(value) == 0:
            value = int(value)
            template = string_formatted
        else:
            template = float_formatted
        return template % {'value': value}

    for exponent, converters in intwordcn_converters:
        large_number = 10 ** exponent
        if value < large_number * 10000:
            new_value = value / float(large_number)
            return _check_for_float(new_value, *converters(new_value))
    return value


@register.simple_tag
def unique_list(*args):
    result = set()
    for array in args:
        result.update(array)
    return list(result)


@register.simple_tag
def unique_tags_text(*args, **kwargs):
    result = set()
    for tags in args:
        result.update([t.name for t in tags])
    return ", ".join(list(result))

