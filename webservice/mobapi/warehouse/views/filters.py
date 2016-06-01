# -*- coding: utf-8 -*-
from rest_framework import filters
from django.http import Http404
from searcher.searchers import SearchException, PackageSearcher
from searcher.search_filters import PackageSearchRestFilter as SolrSearchFilter


class SphinxSearchFilter(filters.SearchFilter):
    search_param = 'q'


class RelatedPackageSearchFilter(filters.BaseFilterBackend):

    search_max_items = 30

    def get_search_filter(self, request, view, terms):
        search_fields = ('tags_text',)
        search_ordering = ('-released_datetime', )
        return PackageSearcher(search_fields, terms, search_ordering)

    def filter_queryset(self, request, queryset, view):
        if not hasattr(view, 'object') or not view.object:
            return queryset

        if not hasattr(view, 'related_package_list') \
            or view.related_package_list is not None:
            return queryset

        tags = view.object.tags_text.split()
        try:
            main_category = view.object.main_category
            category_name = main_category.name
        except:
            category_name = None
        searcher = self.get_search_filter(request, view, tags)
        try:
            sqs = searcher.search()
            sqs = sqs.exclude(django_id=view.object.pk)
            if category_name:
                sqs = sqs.filter(categories=category_name)
        except SearchException:
            return queryset.none()

        return self.convert_queryset(queryset, sqs)

    def convert_queryset(self, orm_queryset, search_query):
        return search_query.values_list('object', flat=True)


class PackageIdsFilter(filters.BaseFilterBackend):

    ids_param = 'ids'

    def validate(self, request, view):
        _ids = request.GET.get(self.ids_param)
        if not _ids:
            raise Http404('not allow empty parameter')
        ids = [self.validate_id(id.strip()) for id in _ids.split(',')]
        return dict(id__in=ids)

    def validate_id(self, val):
        try:
            return int(val)
        except ValueError:
            raise Http404

    def filter_queryset(self, request, queryset, view):
        qs = queryset._clone()
        filter_dict = self.validate(request=request, view=view)
        return qs.filter(**filter_dict)

