# -*- coding: utf-8 -*-
from rest_framework import filters
from haystack.query import SearchQuerySet, SQ
from functools import reduce
import operator
import six

class SolrSearchFilter(filters.SearchFilter):

    collection_name = 'package'

    search_param = 'q'

    search_ordering = ()

    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__startswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__exact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__in" % field_name[1:]
        else:
            return field_name

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        sqs = SearchQuerySet(using=self.collection_name)

        if not search_fields:
            return queryset

        lookups = [self.construct_search(str(search_field))
                   for search_field in search_fields]
        for search_term in self.get_search_terms(request):
            or_queries = [SQ(**{lookup: search_term}) for lookup in lookups]
            sqs = sqs.filter(reduce(operator.or_, or_queries))


        ordering = self.get_search_ordering(view)
        if all(ordering):
            sqs = sqs.order_by(*ordering)

        queryset = self.convert_orm_queryset(
            orm_queryset=queryset,
            search_queryset=sqs)

        return queryset

    def convert_orm_queryset(self, orm_queryset, search_queryset):
        return [result.object for result in search_queryset]

    def get_search_ordering(self, view):
        ordering = getattr(view, 'search_ordering', self.search_ordering)
        if isinstance(ordering, six.string_types):
            return (ordering,)
        return ordering


class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'


class RelatedPackageSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if not hasattr(view, 'object') or not view.object:
            return queryset

        if not hasattr(view, 'related_package_list') \
            or view.related_package_list is not None:
            return queryset

        qs = queryset._clone()
        qs = qs.exclude(pk=view.object.pk).filter(
            categories__in=list(view.object.categories.published())).distinct()
        tags = list(view.object.tags)
        if len(tags) and qs.count():
            return type(view.object).tagged.with_any(tags, qs)
        return queryset.filter(pk=None)