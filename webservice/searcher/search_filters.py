# -*- coding: utf-8 -*-
from searcher.searchers import SearchException, PackageSearcher
from rest_framework import filters


class PackageSearchRestFilter(filters.SearchFilter):

    search_param = 'q'

    def get_search_filter(self, request, view):
        fields = getattr(view, 'search_fields', None)
        ordering = getattr(view, 'search_ordering', None)
        self.search_param = getattr(view, 'search_param', self.search_param)
        terms = self.get_search_terms(request)
        return PackageSearcher(fields, terms, ordering)

    def filter_queryset(self, request, queryset, view):
        package_searcher = self.get_search_filter(request, view)
        try:
            sqs = package_searcher.search()
        except SearchException:
            return queryset.none()
        return self.convert_queryset(orm_queryset=queryset, search_queryset=sqs)

    def convert_queryset(self, orm_queryset, search_queryset):
        return search_queryset.values_list('object', flat=True)

