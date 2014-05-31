# -*- coding: utf-8 -*-
from haystack.query import SearchQuerySet, SQ
from functools import reduce
import operator
import six
from toolkit.helpers import current_site_id


class SearchException(Exception):
    pass


class EmptySearchTerms(SearchException):
    pass


class EmptySearchFields(SearchException):
    pass


class BaseSearcher(object):

    collection_name = None

    search_terms = ()

    search_fields = None

    search_ordering = ()

    def __init__(self, fields=None, terms=None, ordering=None):
        self.search_fields = fields if fields else self.search_fields
        self.search_terms = terms if terms else self.search_terms
        self.search_ordering = ordering if ordering else self.search_ordering

    def search(self):
        search_fields = self.get_search_fields()
        if not search_fields:
            raise EmptySearchFields()
        search_terms = self.get_search_terms()
        if not search_terms:
            raise EmptySearchTerms()
        ordering = self.get_search_ordering()
        sqs = self.filter_search_queryset(self.get_search_qeuryset(),
                                          search_fields,
                                          search_terms,
                                          ordering)
        return sqs

    def filter_search_queryset(self, search_queryset,
                               search_fields, search_terms, ordering):
        sqs = search_queryset._clone()
        lookups = [self.construct_search(str(search_field))
                   for search_field in search_fields]
        for search_term in search_terms:
            or_queries = [SQ(**{lookup: search_term}) for lookup in lookups]
            sqs = sqs.filter(reduce(operator.or_, or_queries))

        if ordering:
            sqs = sqs.order_by(*ordering)
        return sqs

    def get_search_qeuryset(self):
        return SearchQuerySet(using=self.collection_name)

    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__startswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__exact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__in" % field_name[1:]
        else:
            return field_name

    def get_search_fields(self):
        return self.search_fields

    def get_search_terms(self):
        return self.search_terms

    def get_search_ordering(self):
        ordering = self.search_ordering
        if isinstance(ordering, six.string_types):
            return (ordering,)
        return ordering


class BaseSearchCurrentSiteSearcher(BaseSearcher):

    def get_search_qeuryset(self):
        return super(BaseSearchCurrentSiteSearcher, self).get_search_qeuryset() \
            .filter(site=current_site_id())


class PackageSearcher(BaseSearchCurrentSiteSearcher):

    collection_name = 'package'
    search_fields = ('title',
                     'tags_text',
                     'package_name',
                     'categories',
    )
    search_ordering = ('-released_datetime', )


