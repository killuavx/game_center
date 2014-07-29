# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from django.http import Http404
from taxonomy.models import Category
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


class RelatedPackageSearchFilter2(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if not hasattr(view, 'object') or not view.object:
            return queryset

        if not hasattr(view, 'related_package_list') \
            or view.related_package_list is not None:
            return queryset

        main_category = view.object.main_category
        qs = queryset._clone()
        qs = qs.exclude(pk=view.object.pk).filter(categories=main_category)
        tags = view.object.tags_text.split()
        if len(tags):
            return type(view.object).tagged.with_any(tags, qs)
        return queryset.none()


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


class PetitionPackageVersionFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        from comment.models import Petition
        finished = Petition.STATUS.finished
        return queryset.filter(petitions__status=finished) \
            .order_by('-petitions__finished_at')


class PetitionOwnerPackageVersionFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.GET.get('byme'):
            return queryset.filter(petitions__user=request.user)
        return queryset


from rest_framework.filters import django_filters


class DjangoFilterWithCustomFilterSetBackend(filters.DjangoFilterBackend):

    custom_filter_set = None

    def get_filter_class(self, view, queryset=None):
        if self.custom_filter_set:
            return self.custom_filter_set
        return None


def factory_topicalitem_filterbackend(for_model):

    class TopicalItemFilterSet(filters.FilterSet):

        strict = False

        topic_slug = django_filters.CharFilter(name='topics__topic__slug')

        order_by_field = 'ordering'
        order_by = (
            ('topical', 'Topical Ordering'),
        )

        def get_order_by(self, order_value):
            if order_value == 'topical':
                return ['topics__ordering']
            return super(TopicalItemFilterSet, self).get_order_by(order_value)


        class Meta:
            model = for_model
            fields = ['topic_slug', ]
            order_by = ['topical', 'released_datetime' ]

    class TopicalItemFilterBackend(DjangoFilterWithCustomFilterSetBackend):

        custom_filter_set = TopicalItemFilterSet

    return TopicalItemFilterBackend


from warehouse.models import Package, Author
TopicalPackageFilter = factory_topicalitem_filterbackend(Package)
TopicalAuthorFilter = factory_topicalitem_filterbackend(Author)


class AffiliatedCategoryPackageFilter(filters.BaseFilterBackend):

    request_cat_param = 'category'

    def filter_queryset(self, request, queryset, view):
        cat_pk = request.GET.get(self.request_cat_param)
        if not cat_pk:
            return queryset
        try:
            category = Category.objects.get(pk=cat_pk)
        except ObjectDoesNotExist:
            return queryset

        if not category.is_leaf_node():
            cat_ids = list(category.get_descendants(include_self=True) \
                .values_list('pk', flat=True))
            return queryset.filter(categories__pk__in=cat_ids).distinct()
        else:
            return queryset.filter(categories=category.pk)
