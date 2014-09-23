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
            #slugs = self.get_category_descendant_slugs(category)
            slugs = [category.slug]
            sqs = self.get_search_queryset(queryset, slugs).search()
            return sqs
        else:
            if self.hit_category:
                return queryset.none()
            else:
                return queryset


class SearchByLanguageFilterBackend(base.BaseWidgetFilterBackend):

    language_param = 'lang'

    choices = [
        {'code': 'ZH', 'name': '中文'},
        {'code': 'EN', 'name': '英文'},
    ]

    lang_choices = {}
    for c in choices:
        lang_choices[c['code']] = c['code']

    def filter_queryset(self, request, queryset, widget):
        lang = getattr(widget, self.language_param, None)
        if lang is None:
            return queryset
        lang = lang.upper()
        if lang not in self.lang_choices:
            return queryset
        return queryset.filter(support_language_codes__in=[lang])


class SearchByPkgSizeFilterBackend(base.BaseWidgetFilterBackend):

    M = 1024 * 1024

    G = M * 1024

    size_param = 'size'

    choices = [
        {'code': '0-10m', 'name': '10M以内', 'value': (None, 10*M)},
        {'code': '10-50m', 'name': '10-50M', 'value': (10*M, 50*M)},
        {'code': '50-100m', 'name': '50-100M', 'value': (50*M, 100*M)},
        {'code': '100-300m', 'name': '100-300M', 'value': (100*M, 300*M)},
        {'code': '300-500m', 'name': '300-500M', 'value': (300*M, 500*M)},
        {'code': '500-800m', 'name': '500-800M', 'value': (500*M, 800*M)},
        {'code': '800m-1g', 'name': '800M-1G', 'value': (800*M, 1*G)},
        {'code': '1g', 'name': '1G以上', 'value': (1*G, None)},
    ]

    size_choices = {}
    for c in choices:
        size_choices[c['code']] = c['value']

    def filter_queryset(self, request, queryset, widget):
        size = getattr(widget, self.size_param, None)
        if size is None:
            return queryset
        size = size.lower()
        if size not in self.size_choices:
            return queryset
        min_size, max_size = self.size_choices[size]
        if min_size:
            queryset = queryset.filter(download_size__gte=min_size)
        if max_size:
            queryset = queryset.filter(download_size__lt=max_size)
        return queryset


class SearchByPkgReportsFilterBackend(base.BaseWidgetFilterBackend):

    reports_param = 'reps'

    choices = [
        {'code': 'no-network', 'name': '无需网络'},
        {'code': 'no-adv', 'name': '无需广告'},
        {'code': 'no-google', 'name': '无需谷歌市场'},
    ]

    report_choices = {}
    for c in choices:
        report_choices[c['code']] = c['code']

    def filter_queryset(self, request, queryset, widget):
        reps = getattr(widget, self.reports_param, [])
        if not reps:
            return queryset

        for r in reps:
            r = r.lower()
            if r in self.report_choices:
                queryset = queryset.filter(reports__in=[r['code']])
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


import operator
from functools import reduce
from haystack.constants import ID
from haystack.query import SQ


class RelatedPackageSearcherBySearchFilterBackend(BaseWidgetFilterBackend):

    package_search_result_param = 'package'

    def filter_queryset(self, request, queryset, widget):
        package = getattr(widget, self.package_search_result_param, None)
        qs = queryset.exclude(**{ID:package.id})
        if package.main_category_ids:
            cats_or_queries = [SQ(main_category_ids=cid) for cid in package.main_category_ids]
            qs = qs.filter(reduce(operator.or_, cats_or_queries))
        else:
            qs = qs.filter(root_category_id=package.root_category_id)
        tags = package.tags_text.split() if package.tags_text else None
        if tags:
            or_queries = [SQ(**{'tags_text': tag}) for tag in tags]
            qs = qs.filter(reduce(operator.or_, or_queries))
        return qs
