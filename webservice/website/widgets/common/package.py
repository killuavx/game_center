# -*- coding: utf-8 -*-
from . import base
from copy import deepcopy
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import six
from website.widgets.common import filters


class BasePackageListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    ordering = ('-released_datetime', )

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        qs = self.get_queryset().published()
        return self.filter_queryset(qs)


class BasePackageSearchListWidget(base.FilterWidgetMixin, base.BaseListWidget):

    search_param = 'q'

    search_fields = ()

    ordering = ()

    filter_backends = (filters.PackageByCategorySearcherFilter, )

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
            qs = self.filter_queryset(searcher.search())
            return qs
        except SearchException as e:
            return searcher.get_search_qeuryset().none()

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.search_terms = self.get_search_terms(options)
        return super(BasePackageSearchListWidget, self)\
            .get_context(value=value,
                         options=options,
                         context=context,
                         pagination=pagination)


class BaseComplexPackageListWidget(base.FilterWidgetMixin,
                                   base.PaginatorPageMixin):

    ByCategoryFilterBackend = filters.CategorizedPackageFilterbackend

    class ByTopicFilterBackend(filters.ItemListByTopicFilterBackend):

        filter_ignore = False

        topic_param = 'current_topic'

    class OrderByFilterBackend(filters.PackageReleasedOrderFilterBackend):

        def filter_queryset(self, request, queryset, widget):
            setattr(widget, self.released_param,
                    getattr(widget, self.released_param, False) or bool(widget.current_topic))
            return super(BaseComplexPackageListWidget.OrderByFilterBackend, self)\
                .filter_queryset(request, queryset, widget)

    filter_backends = ()

    category = None

    current_topic = None

    topic_slugs = []

    per_page = 12

    TOPIC_NONE = 'NONE'

    max_paging_links = 10

    by_released = True

    def get_topic(self, topic_slug):
        from taxonomy.models import Topic
        return Topic.objects.get(slug=topic_slug)

    def get_category(self, cat_slug):
        from taxonomy.models import Category
        return Category.objects.get(slug=cat_slug)

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        qs = self.get_queryset().published()
        return self.filter_queryset(qs)

    def get_topic_slugs_from(self, options):
        _slugs_txt = options.get('topic_slugs')
        return [slug.strip() for slug in _slugs_txt.split(',') if slug]

    def get_context(self, value=None, options=dict(), context=None):
        from mezzanine.utils.views import paginate
        self.options = options
        self.product = options.get('product')
        self.per_page, cur_page = self.get_paginator_vars(self.options)
        self.request = context.get('request')
        cat_slug = options.get('cat_slug')
        self.topic_slugs = self.get_topic_slugs_from(options)

        # 过滤分类及其所有后代的列表
        self.category = self.get_category(cat_slug)
        self.filter_backends = (self.ByCategoryFilterBackend, )
        queryset = self.get_list()

        results = []
        # 过滤专区，当前专区为空，则以最新发布排序
        for topic_slug in self.topic_slugs:

            if topic_slug == self.TOPIC_NONE:
                self.current_topic = None
                grp_name = '最新发布'
                grp_more_url = self.get_more_url_by(self.category, None)
                self.by_released = True
                self.filter_backends = (self.OrderByFilterBackend, )
            else:
                self.filter_backends = (self.ByTopicFilterBackend,
                                        self.OrderByFilterBackend)
                self.by_released = False
                try:
                    self.current_topic = self.get_topic(topic_slug)
                except ObjectDoesNotExist:
                    self.current_topic = None
                    continue
                grp_name = self.current_topic.name
                grp_more_url =self.get_more_url_by(self.category, self.current_topic)

            qs = self.filter_queryset(queryset).all()
            items = paginate(qs,
                             page_num=cur_page,
                             per_page=self.per_page,
                             max_paging_links=self.max_paging_links)
            results.append(dict(
                name=grp_name,
                packages=items,
                paginator=items.paginator,
                more_url=grp_more_url,
            ))

        data = deepcopy(options)
        data.update(
            category=self.category,
            title=self.category.name,
            result=results,
            product=self.product
        )
        return data

    def get_more_url_by(self, category, topic):
        topic_param = 'topic'
        url = category.get_absolute_url_as(product=self.product, pagetype='special')
        if topic:
            urlp = list(urlparse(url))
            qp = parse_qsl(urlp[4])
            qp = list(filter(lambda nv: not(nv[0] == topic_param), qp))
            qp.append((topic_param, topic.pk,))
            urlp[4] = urlencode(qp, True)
            url = urlunparse(urlp)
        return url


class BaseTopicalPackageListWidget(BasePackageListWidget):

    class TopicalFilter(filters.ItemListByTopicFilterBackend):
        filter_ignore = False

    topic = None

    topic_ordering = False

    by_released = (not topic_ordering)

    filter_backends = (TopicalFilter,
                       filters.PackageReleasedOrderFilterBackend,
    )


    def get_more_url(self):
        if self.topic:
            return self.topic.get_absolute_url_as(product=self.product,
                                                  pagetype='special')
        return 'javascript:;'

    def get_title(self):
        if self.topic:
            return self.topic.name
        return self.title

    def get_topic(self, slug):
        from taxonomy.models import Topic
        return Topic.objects.get(slug=slug)

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        try:
            self.topic = self.get_topic(slug=options.get('slug'))
        except ObjectDoesNotExist:
            self.topic = None
        return super(BaseTopicalPackageListWidget, self).get_context(
            value=value,
            options=options,
            context=context,
            pagination=pagination)


class BaseRankingPackageListWidget(base.PaginatorPageMixin):

    template = None

    ranking_slug = 'main'

    cat_slug = None

    ranking = None

    title = None

    more_url = None

    def get_title(self):
        return self.title

    def get_more_url(self):
        return self.more_url

    def get_list(self):
        from warehouse.models import Package
        return Package.objects.filter(rankings__pk=self.ranking.pk).published()

    def get_ranking(self, cat_slug, ranking_slug, cycle_type=0):
        from ranking.models import PackageRanking
        return PackageRanking.objects.get(ranking_type__slug=ranking_slug,
                                          category__slug=cat_slug,
                                          cycle_type=cycle_type)

    def get_context(self, value, options, context=None):
        context = context if context else dict()
        self.options = options
        self.per_page, cur_page = self.get_paginator_vars(options)
        self.cat_slug = options.get('cat_slug')
        self.product = options.get('product')
        self.request = context.get('request')
        self.ranking_slug = options.get('ranking_slug', 'main')
        self.ranking = self.get_ranking(self.cat_slug, self.ranking_slug)
        qs = self.get_list()
        paginator = Paginator(qs, self.per_page)
        data = deepcopy(options)
        data.update(
            title=self.get_title(),
            more_url=self.get_more_url(),
            ranking=self.ranking,
            items=paginator.page(cur_page),
            product=self.product,
        )
        return data


class BaseCategoryComplexPackageList(BasePackageListWidget):

    class ByCategoryFilterBackend(filters.CategorizedPackageFilterbackend):

        filter_ignore = False

    class ByTopicFilterBackend(filters.ItemListByTopicFilterBackend):

        filter_ignore = True

        topic_param = 'current_topic'

    class OrderByFilterBackend(filters.PackageReleasedOrderFilterBackend):

        def filter_queryset(self, request, queryset, widget):
            setattr(widget, self.released_param, getattr(widget, self.released_param) or not bool(widget.current_topic))
            return super(BaseCategoryComplexPackageList.OrderByFilterBackend, self) \
                .filter_queryset(request, queryset, widget)

    filter_backends = (
        ByCategoryFilterBackend,
        ByTopicFilterBackend,
        OrderByFilterBackend,
    )

    current_topic = None

    category = None

    lang = None

    by_released = True

    def get_category(self, slug):
        from taxonomy.models import Category
        if isinstance(slug, six.string_types):
            return Category.objects.get(slug=slug)
        elif isinstance(slug, Category):
            return slug
        raise TypeError

    def get_topic(self, slug):
        from taxonomy.models import Topic
        if not slug:
            return None
        if isinstance(slug, six.string_types):
            return Topic.objects.get(slug=slug)
        elif isinstance(slug, Topic):
            return slug
        raise TypeError

    def get_lang(self, lang):
        from warehouse.models import SupportedLanguage
        return SupportedLanguage.objects.get(code=lang)

    def get_context(self, value=None, options=dict(), context=None, pagination=True):
        self.category = self.get_category(options.get('category'))
        try:
            self.current_topic = self.get_topic(options.get('topic'))
        except ObjectDoesNotExist:
            self.current_topic = None

        try:
            self.lang = self.get_lang(options.get('lang'))
        except ObjectDoesNotExist:
            self.lang = None

        data = super(BaseCategoryComplexPackageList, self).get_context(value=value,
                                                                     options=options,
                                                                     context=context,
                                                                     pagination=pagination)
        return data
