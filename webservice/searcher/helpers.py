# -*- coding: utf-8 -*-
from haystack.query import SearchQuerySet
from haystack.constants import ID
from haystack.utils import get_identifier


def get_default_package_query(result_class=None):
    sqs = SearchQuerySet('package')
    if result_class:
        return sqs.result_class(result_class)
    return sqs


def get_search_package(sqs, instance):
    try:
        return sqs.filter(**{ID: get_identifier(instance)})[0]
    except IndexError:
        return None

