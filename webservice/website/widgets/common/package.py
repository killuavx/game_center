# -*- coding: utf-8 -*-
from . import base


class BasePackageListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    ordering = ('-released_datetime', )

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        qs = self.get_queryset().published()
        return self.filter_queryset(qs)


class PackageByCategorySearcherFilter(base.BaseWidgetFilterBackend):

    hit_category = False

    cat_slugs = ('game', 'application')

    def get_search_queryset(self, search_queryset, terms):
        from searcher.searchers import BaseSearcher, PackageSearcher

        class ByCategoryFitler(BaseSearcher):
            collection_name = PackageSearcher.collection_name
            search_fields = ('@category_slugs', )
            search_ordering = ()
            def get_search_qeuryset(self):
                return search_queryset

        return ByCategoryFitler(terms=[terms])

    def get_category(self, slug):
        from taxonomy.models import Category
        return Category.objects.get(slug=slug)

    def get_category_descendant_slugs(self, category):
        return list(category.get_descendants(include_self=True)\
            .values_list('slug', flat=True))

    def filter_queryset(self, request, queryset, widget):
        cat = widget.options.get('cat')
        category = None
        if cat and cat in self.cat_slugs:
            category = self.get_category(cat)

        if category:
            slugs = self.get_category_descendant_slugs(category)
            sqs = self.get_search_queryset(queryset, slugs).search()
            return sqs
        else:
            if self.hit_category:
                return queryset.none()
            else:
                return queryset


class BasePackageSearchListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    search_param = 'q'

    search_fields = ()

    ordering = ()

    filter_backends = (PackageByCategorySearcherFilter, )

    def get_search_terms(self, options):
        querystr = options.get(self.search_param, '')
        return querystr.replace(',', ' ').split()

    def get_searcher(self, requset):
        from searcher.searchers import PackageSearcher
        return PackageSearcher(fields=self.search_fields,
                               terms=self.search_terms,
                               ordering=self.ordering)

    def get_list(self):
        from searcher.searchers import SearchException
        searcher = self.get_searcher(self.request)
        try:
            return self.filter_queryset(searcher.search())
        except SearchException as e:
            return searcher.get_search_qeuryset().none()

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.search_terms = self.get_search_terms(options)
        return super(BasePackageSearchListWidget, self)\
            .get_context(value=value,
                         options=options,
                         context=context,
                         pagination=pagination)

