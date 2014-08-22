# -*- coding: utf-8 -*-
from haystack.query import SearchQuerySet
from haystack.constants import ID, DJANGO_CT
from haystack.utils import get_identifier, get_model_ct


def get_default_package_query(result_class=None):
    sqs = SearchQuerySet('package')
    if result_class:
        return sqs.result_class(result_class)
    return sqs


def get_package_search_result(sqs, pk):
    from warehouse.models import Package
    _id = get_identifier(Package(pk=pk))
    try:
        return sqs.filter(**{ID:_id})[0]
    except IndexError:
        return None


def get_package_search_result_by_version_id(sqs, version_id):
    from warehouse.models import Package
    try:
        sqs.filter(**{DJANGO_CT:get_model_ct(Package),
                      'latest_version_id':version_id})
    except IndexError:
        return None

