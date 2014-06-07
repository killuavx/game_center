# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django_widgets import Widget
from dateutil.relativedelta import relativedelta
from website.widgets.common.promotion import BaseMultiAdvWidget
from website.widgets.common.base import FilterWidgetMixin, BaseWidgetFilterBackend
from website.widgets.common.filters import (
    CategorizedPackageFilterbackend,
    PackageReleasedOrderFilterBackend
    )
from . import base


__all__ = ['WebCrackTopBannersWidget', 'WebCrackTimeLinePanelWidget']

def _default_slug():
    return 'crack-game'


class WebCrackTopBannersWidget(BaseMultiAdvWidget,
                               base.ProductPropertyWidgetMixin,
                               Widget):

    template='pages/widgets/home/banner.haml'

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = _default_slug()
        return super(WebCrackTopBannersWidget, self).get_context(value=value,
                                                          options=options,
                                                          context=context)


class InDateFilterBackend(BaseWidgetFilterBackend):

    filter_date_param = 'filter_date_field'

    date_param = 'in_date'

    def filter_queryset(self, request, queryset, widget):
        d = getattr(widget, self.date_param)
        field = getattr(widget, self.filter_date_param)
        if not d or not field:
            queryset
        return queryset.filter(**{
            "%s__year" % field : d.year,
            "%s__month" % field: d.month,
            "%s__day" % field: d.day,
        })


def datesince(cur_dt, comp_dt):
    comp = relativedelta(comp_dt, cur_dt)
    dmap = {
        'before': '%d天前',
        -2: '前天',
        -1: '昨天',
        0: '今天',
        'after': '%d天后',
    }
    if comp.days in dmap:
        return dmap[comp.days]
    elif comp.days < 0:
        return dmap['before'] % abs(comp.days)
    else:
        return dmap['after'] % comp.days


class WebCrackTimeLinePanelWidget(base.ProductPropertyWidgetMixin,
                                  FilterWidgetMixin,
                                  Widget):

    filter_backends = ()

    first_filter_backends = (CategorizedPackageFilterbackend, )
    second_filter_backends = (InDateFilterBackend,
                              PackageReleasedOrderFilterBackend,)

    by_released = True

    category = None

    in_date = None

    filter_date_field = 'released_datetime'

    latest_day_count = 4

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        return self.get_queryset().published()

    def _get_default_slug(self):
        return 'crack-game'

    def get_category(self):
        from taxonomy.models import Category
        return Category.objects.get(slug=self.slug)

    def get_latest_days_by(self, queryset, now=None):
        days = queryset\
                   .dates('released_datetime', 'day', 'DESC')[0:self.latest_day_count]
        cur_dt = now.astimezone()
        _days = []
        for d in days:
            dt = d.astimezone()
            _days.append(dict(
                time_name=datesince(cur_dt, dt),
                dt=dt,
                url=None,
                ))
        _days[-1]['time_name'] = '以前'
        _days[-1]['url'] = self.category.get_absolute_url_as(product=self.product)
        return _days

    def get_context(self, value, options, context=None):
        self.options = options
        self.product = options.get('product')
        if context:
            self.request = context.get('request')
        self.slug = _default_slug()
        self.category = self.get_category()
        self.current_datetime = now()

        result = list()
        queryset = self.get_list()
        self.filter_backends = self.first_filter_backends
        queryset = self.filter_queryset(queryset)

        self.filter_backends = self.second_filter_backends
        for grp in self.get_latest_days_by(queryset, now=self.current_datetime):
            self.in_date = grp['dt']
            result.append(dict(time_name=grp['time_name'],
                               url=grp['url'],
                               packages=self.filter_queryset(queryset)))

        self.filter_backends = ()
        return dict(
            category=self.category,
            result=result,
            product=self.product
        )


class WebLatestTopBannersWidget(BaseMultiAdvWidget,
                                base.ProductPropertyWidgetMixin,
                                Widget):

    template='pages/widgets/home/banner.haml'

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = 'banner-web-latest'
        return super(WebLatestTopBannersWidget, self).get_context(value=value,
                                                                  options=options,
                                                                  context=context)


class WebLatestTimeLinePanelWidget(base.ProductPropertyWidgetMixin,
                                   FilterWidgetMixin,
                                   Widget):
    filter_backends = ()

    second_filter_backends = (InDateFilterBackend,
                              PackageReleasedOrderFilterBackend,)

    by_released = True

    in_date = None

    filter_date_field = 'released_datetime'

    latest_day_count = 4

    def get_title(self):
        return '最新发布'

    def get_queryset(self):
        from warehouse.models import Package
        return Package.objects.all()

    def get_list(self):
        return self.get_queryset().published()

    def get_latest_days_by(self, queryset, now=None):
        days = queryset \
                   .dates(self.filter_date_field,
                          'day', 'DESC')[0:self.latest_day_count]
        _days = []
        cur_dt = now.astimezone()
        for d in days:
            dt = d.astimezone()
            _days.append(dict(
                time_name=datesince(cur_dt, dt),
                dt=dt,
                url=None,
                ))

        from taxonomy.models import Category
        _days[-1]['time_name'] = '以前'
        _days[-1]['url'] = Category.absolute_url_as(slug=Category.ROOT_SLUG_GAME,
                                                    product=self.product)
        return _days

    def get_context(self, value, options, context=None):
        self.options = options
        self.product = options.get('product')
        if context:
            self.request = context.get('request')
        self.slug = _default_slug()
        self.current_datetime = now()

        result = list()
        queryset = self.get_list()
        self.filter_backends = ()
        queryset = self.filter_queryset(queryset)

        self.filter_backends = self.second_filter_backends
        for grp in self.get_latest_days_by(queryset, now=self.current_datetime):
            self.in_date = grp['dt']
            result.append(dict(time_name=grp['time_name'],
                               url=grp['url'],
                               packages=self.filter_queryset(queryset)))

        self.filter_backends = ()
        return dict(
            title=self.get_title(),
            result=result,
            product=self.product,
        )
