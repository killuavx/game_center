# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.db.models.query import EmptyQuerySet
from django.core.paginator import Paginator
from django_widgets import Widget
from website.widgets.common.base import PaginatorPageMixin
from website.widgets.common.promotion import BaseMultiAdvWidget
from website.widgets.common.author import BaseTopicAuthorPanelWidget
from website.widgets.common.topic import BaseTopicPackageListWidget, ItemListByTopicFilterBackend
from website.widgets.common.base import BaseWidgetFilterBackend, FilterWidgetMixin

__all__ = ['PCBannerWidget',
           'PCRollMasterpiecesWidget',
           'PCRollVendorsWidget',
           'PCHomeComplexPackageListWidget',
           'PCRankingPackageListWidget',
           ]

class PCBannerWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/pc/widgets/banner.haml'


class PCRollAdvertisementsWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollVendorsWidget(BaseTopicAuthorPanelWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class PCRollMasterpiecesWidget(BaseTopicPackageListWidget, Widget):

    template = 'pages/pc/widgets/roll-place.haml'


class BaseComplexPackageListWidget(FilterWidgetMixin, PaginatorPageMixin):

    class ByCategoryFilterBackend(BaseWidgetFilterBackend):

        def filter_queryset(self, request, queryset, widget):
            category = widget.category
            cat_ids = list(category \
                .get_descendants(include_self=True) \
                .values_list('pk', flat=True))
            return queryset.filter(categories__pk__in=cat_ids).distinct()

    class ByTopicFilterBackend(ItemListByTopicFilterBackend):

        topic_param = 'current_topic'

        def filter_queryset(self, request, queryset, widget):
            if not getattr(widget, self.topic_param):
                return queryset
            return super(BaseComplexPackageListWidget.ByTopicFilterBackend, self)\
                .filter_queryset(request, queryset, widget)

    class OrderByFilterBackend(BaseWidgetFilterBackend):

        def filter_queryset(self, request, queryset, widget):
            if not widget.current_topic and\
                    not isinstance(queryset, EmptyQuerySet):
                return queryset.by_published_order(True)
            return queryset

    filter_backends = ()

    category = None

    current_topic = None

    topic_slugs = []

    per_page = 12

    TOPIC_NONE = 'NONE'

    def get_topic(self, topic_slug):
        from taxonomy.models import Topic
        return Topic.objects.get(slug=topic_slug)

    def get_category(self, cat_slug):
            from taxonomy.models import Category
            return Category.objects.get(slug=cat_slug)

    def get_list(self):
        from warehouse.models import Package
        return Package.objects.published()

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.options = options
        self.per_page, cur_page = self.get_paginator_vars(self.options)
        self.request = context.get('request')
        cat_slug = options.get('cat_slug')
        _slugs_txt = options.get('topic_slugs')
        self.topic_slugs = [slug.strip() for slug in _slugs_txt.split(',') if slug]

        # 过滤分类及其所有后代的列表
        self.category = self.get_category(cat_slug)
        self.filter_backends = (self.ByCategoryFilterBackend, )
        queryset = self.filter_queryset(self.get_list())

        results = []
        # 过滤专区，当前专区为空，则以最新发布排序
        self.filter_backends = (self.ByTopicFilterBackend, self.OrderByFilterBackend)
        for topic_slug in self.topic_slugs:

            if topic_slug == self.TOPIC_NONE:
                self.current_topic = None
                grp_name = '最新发布'
                grp_more_url = self.get_more_url_by(self.category, None)
            else:
                self.current_topic = self.get_topic(topic_slug)
                grp_name = self.current_topic.name
                grp_more_url =self.get_more_url_by(self.category, self.current_topic)

            paginator = Paginator(self.filter_queryset(queryset).all(), self.per_page)
            results.append(dict(
                name=grp_name,
                packages=paginator.page(cur_page),
                more_url=grp_more_url,
            ))

        options.update(
            result=results,
        )
        return options

    def get_more_url_by(self, category, topic):
        topic_param = 'topic'
        url = category.get_absolute_url_as(product='pc', pagetype='special')
        if topic:
            urlp = list(urlparse(url))
            qp = parse_qsl(urlp[4])
            qp = list(filter(lambda nv: not(nv[0] == topic_param), qp))
            qp.append((topic_param, topic.slug,))
            urlp[4] = urlencode(qp, True)
            url = urlunparse(urlp)
        return url


class PCHomeComplexPackageListWidget(BaseComplexPackageListWidget, Widget):

    template = 'pages/pc/widgets/home-complex-package-list-panel.haml'


class PCRankingPackageListWidget(PaginatorPageMixin, Widget):

    template = 'pages/pc/widgets/ranking-package-list-panel.haml'

    ranking_slug = 'main'

    cat_slug = None

    ranking = None

    def get_list(self):
        from warehouse.models import Package
        return Package.objects.filter(rankings__pk=self.ranking.pk)

    def get_ranking(self, cat_slug, ranking_slug, cycle_type=0):
        from ranking.models import PackageRanking
        return PackageRanking.objects.get(ranking_type__slug=ranking_slug,
                                          category__slug=cat_slug,
                                          cycle_type=cycle_type)


    def get_context(self, value, options):
        self.per_page, cur_page = self.get_paginator_vars(options)

        self.cat_slug = options.get('cat_slug')
        self.ranking = self.get_ranking(self.cat_slug, self.ranking_slug)
        paginator = Paginator(self.get_list(), self.per_page)

        data = dict(
            ranking=self.ranking,
            items=paginator.page(cur_page)
        )
        return data

