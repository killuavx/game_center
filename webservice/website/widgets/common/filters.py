# -*- coding: utf-8 -*-
from . import base
from django.db.models.query import EmptyQuerySet
from website.widgets.common.base import BaseWidgetFilterBackend


class ItemListByTopicFilterBackend(base.BaseWidgetFilterBackend):

    topic_param = 'topic'

    ordering_param = 'topic_ordering'

    filter_ignore = True

    def filter_queryset(self, request, queryset, widget):
        from taxonomy.models import TopicalItem
        if not getattr(widget, self.topic_param, None):
            if self.filter_ignore:
                return queryset
            else:
                return queryset.none()

        topic = getattr(widget, self.topic_param)
        queryset = TopicalItem.objects \
            .filter_items_by_topic(topic=topic,
                                   item_model=queryset.model,
                                   queryset=queryset,
                                   order=getattr(widget,
                                                 self.ordering_param,
                                                 True)
        )
        return queryset


class PackageReleasedOrderFilterBackend(base.BaseWidgetFilterBackend):

    released_param = 'by_released'

    def filter_queryset(self, request, queryset, widget):
        if getattr(widget, self.released_param, None) \
            and not isinstance(queryset, EmptyQuerySet):
            return queryset.by_released_order(True)
        return queryset


class PackageByCategorySearcherFilter(base.BaseWidgetFilterBackend):

    hit_category = False

    cat_slugs = ('game', 'application')

    cat_param = 'cat'

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
        if isinstance(slug, Category):
            return slug
        return Category.objects.get(slug=slug)

    def get_category_descendant_slugs(self, category):
        return list(category.get_descendants(include_self=True) \
            .values_list('slug', flat=True))

    def filter_queryset(self, request, queryset, widget):
        cat = widget.options.get(self.cat_param)
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


class CategorizedPackageFilterbackend(base.BaseWidgetFilterBackend):

    category_param = 'category'

    filter_ignore = True

    def filter_queryset(self, request, queryset, widget):
        if not getattr(widget, self.category_param):
            if self.filter_ignore:
                return queryset
            else:
                return queryset.none()

        category = widget.category
        if category.is_leaf_node():
            return queryset.filter(categories=category)

        cat_ids = list(category \
            .get_descendants(include_self=True) \
            .values_list('pk', flat=True))
        return queryset.filter(categories__pk__in=cat_ids).distinct()


class AuthorPackageWidgetFilter(BaseWidgetFilterBackend):

    author_param = 'author'

    def filter_queryset(self, request, queryset, widget):
        if hasattr(widget, self.author_param):
            author = getattr(widget, self.author_param)
            return queryset.filter(author=author)
        return queryset