# -*- coding: utf-8 -*-
from . import base
from functools import reduce
from haystack.backends import SQ
from haystack.query import SearchQuerySet
import operator
import six


class BasePackageListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    ordering = ('-released_datetime', )

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        qs = self.get_queryset().published()
        return self.filter_queryset(qs)


class SolrSearchFilterBackend(base.BaseWidgetFilterBackend):

    collection_name = 'package'

    search_param = 'q'

    search_ordering = ()

    search_fields = ()

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

    def get_search_terms(self, view):
        return getattr(view, self.search_param, list())

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', self.search_fields)
        sqs = SearchQuerySet(using=self.collection_name)

        if not search_fields:
            return queryset

        lookups = [self.construct_search(str(search_field))
                   for search_field in search_fields]
        for search_term in self.get_search_terms(view):
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


class SolrPackageSearchFilterBackend(SolrSearchFilterBackend):

    collection_name = 'package'

    search_param = 'q'

    search_fields = ('title', 'tags_text', 'package_name', 'categories')

    search_ordering = ('-released_datetime', )
