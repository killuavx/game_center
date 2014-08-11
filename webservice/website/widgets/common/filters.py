# -*- coding: utf-8 -*-
from . import base
from django.db.models.query import EmptyQuerySet
from mongoengine import queryset_manager
from website.widgets.common.base import BaseWidgetFilterBackend
from toolkit.helpers import get_global_site


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

# Backend using haystack.query.SearchQuerySet
class SearchBySiteFilterbackend(base.BaseWidgetFilterBackend):

    def filter_queryset(self, request, queryset, widget):
        return queryset.filter(site=get_global_site().pk)


class SearchByCategoryFilterBackend(base.BaseWidgetFilterBackend):

    filter_ignore = False

    category_param = 'category'

    category_id_param = 'category_id'

    category_slug_param = 'category_slug'

    def filter_queryset(self, request, queryset, widget):
        category = getattr(widget, self.category_param, None)
        category_id = getattr(widget, self.category_id_param, None)
        category_slug = getattr(widget, self.category_slug_param, None)
        if not category and not category_id and not category_slug:
            if self.filter_ignore:
                return queryset
            else:
                return queryset.none()

        if category is not None:
            if isinstance(category, int):
                category_id = category
            elif isinstance(category, str):
                category_slug = category
            else:
                category_id = category.pk

        if category_id:
            queryset = queryset.filter(category_ids=category_id)
        elif category_slug:
            queryset = queryset.filter(category_slugs=category_slug)
        return queryset


class SearchByTopicFilterBackend(base.BaseWidgetFilterBackend):

    topic_param = 'topic'
    topic_id_param = 'topic_id'
    topic_slug_param = 'topic_slug'

    filter_ignore = True

    def filter_queryset(self, request, queryset, widget):
        topic = getattr(widget, self.topic_param, None)
        topic_id = getattr(widget, self.topic_id_param, None)
        topic_slug = getattr(widget, self.topic_slug_param, None)
        if not topic and not topic_slug and not topic_id:
            if self.filter_ignore:
                return queryset
            else:
                return queryset.none()

        if topic is not None:
            if isinstance(topic, int):
                topic_id = topic
            elif isinstance(topic, str):
                topic_slug = topic
            else:
                topic_id = topic.pk

        if topic_id:
            return queryset.filter(topic_ids=topic_id)
        elif topic_slug:
            return queryset.filter(topic_slugs=topic_slug)
        else:
            return queryset


class SearchOrderByFilterBackend(base.BaseWidgetFilterBackend):

    def filter_queryset(self, request, queryset, widget):
        ordering = getattr(widget, 'search_ordering', None)
        if ordering is None:
            return queryset
        elif isinstance(ordering, str):
            ordering = (ordering,)
        qs = queryset.order_by(*ordering)
        return qs


class SearchByAuthorFilterBackend(base.BaseWidgetFilterBackend):

    author_param = 'author'
    author_id_param = 'author_id'

    filter_ignore = True

    def filter_queryset(self, request, queryset, widget):
        author = getattr(widget, self.author_param, None)
        author_id = getattr(widget, self.author_id_param, None)
        if not author and not author_id:
            if self.filter_ignore:
                return queryset
            else:
                return queryset.none()
        if author:
            author_id = author.pk
        return queryset.filter(author_id=author_id)


class SearchOrderByTopicalFilterBackend(base.BaseWidgetFilterBackend):

    topic_param = 'topic'
    topic_id_param = 'topic_id'

    def filter_queryset(self, request, queryset, widget):
        topic = getattr(widget, self.topic_param, None)
        topic_id = getattr(widget, self.topic_id_param, None)
        if topic:
            topic_id = topic.pk
        if topic_id:
            return queryset.order_by('topic_%d_ordering_i' % topic_id)
        else:
            return queryset

