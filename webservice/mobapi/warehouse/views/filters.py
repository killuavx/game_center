# -*- coding: utf-8 -*-
from rest_framework import filters
from django.http import Http404
from searcher.search_filters import PackageSearchRestFilter as SolrSearchFilter


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

