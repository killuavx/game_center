# -*- coding: utf-8 -*-
from django.utils.timezone import now, get_default_timezone, make_aware
from datetime import datetime, timedelta
from dateutil import rrule
from django_widgets import Widget
from dateutil.relativedelta import relativedelta
from website.widgets.common.promotion import BaseMultiAdvWidget
from website.widgets.common.filters import SearchByCategoryFilterBackend, SearchOrderByFilterBackend
from website.widgets.common.package import BasePackageBySearchListWidget
from website.widgets.common.base import FilterWidgetMixin, BaseWidgetFilterBackend
from website.widgets.common.filters import (
    CategorizedPackageFilterbackend,
    PackageReleasedOrderFilterBackend
    )
from . import base
from toolkit.helpers import get_global_site


__all__ = ['WebCrackTopBannersWidget', 'WebCrackTimeLinePanelWidget', 'WebCrackTimeLineBySearchPanelWidget']

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
        # compat django 1.6
        if hasattr(queryset, 'datetimes'):
            days = queryset.datetimes('released_datetime', 'day',
                                      order='DESC',
                                      tzinfo=get_default_timezone())[0:self.latest_day_count]
        else:
            days = queryset \
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


class SearchReleasedInDateFilterbackend(BaseWidgetFilterBackend):

    def filter_queryset(self, request, queryset, widget):
        dt = getattr(widget, 'in_date')
        if not dt:
            return queryset

        start_dt = datetime(year=dt.year,
                            month=dt.month,
                            day=dt.day)
        start_dt = make_aware(start_dt, get_default_timezone())
        end_dt = start_dt + timedelta(days=1)
        return queryset.filter(released_datetime__gte=start_dt,
                               released_datetime__lt=end_dt)


from haystack.query import EmptySearchQuerySet


class BaseTimeLineBySearchPanelWidget(base.ProductPropertyWidgetMixin,
                                      BasePackageBySearchListWidget,
                                      Widget):

    title = None

    filter_backends = ()

    first_filter_backends = ()
    second_filter_backends = (SearchReleasedInDateFilterbackend,
                              SearchOrderByFilterBackend,)
    search_ordering = ('-released_datetime', )

    in_date = None

    latest_day_count = 4

    max_timedelta_days = 30

    def get_title(self):
        return self.title

    def get_latest_days_by(self, queryset, now_dt):
        try:
            item = queryset.latest('released_datetime')
            et = item.released_datetime
        except:
            et = now_dt
        end_dt = datetime(year=et.year,
                          month=et.month,
                          day=et.day)
        start_dt = end_dt - timedelta(days=self.max_timedelta_days)
        dts = rrule.rrule(rrule.DAILY, dtstart=start_dt, until=end_dt)
        days = sorted(dts, reverse=True)
        _days = []
        tzinfo=get_default_timezone()
        for d in days:
            dt = make_aware(d, tzinfo)
            _days.append(dict(
                time_name=datesince(now_dt, dt),
                dt=dt,
                url=None))
        return _days

    def setup_options(self, context, options):
        self.options = options
        self.product = options.get('product')
        if context:
            self.request = context.get('request')
        self.current_datetime = now().astimezone()

    def fill_latest_one(self, result, grp):
        result[-1]['time_name'] = '以前'

    def query_group_packages(self, queryset, grp, result):
        self.in_date = grp['dt']
        packages = list(self.filter_queryset(queryset))
        if not packages:
            return False
        result.append(dict(time_name=grp['time_name'],
                           url=grp['url'],
                           packages=packages))
        return True

    def get_context(self, value=None, options=dict(), context=None, **kwargs):
        self.setup_options(context, options)

        result = list()
        queryset = self.get_list()
        self.filter_backends = self.first_filter_backends
        queryset = self.filter_queryset(queryset)

        if not isinstance(queryset, EmptySearchQuerySet):
            self.filter_backends = self.second_filter_backends
            grp_count = 0
            for grp in self.get_latest_days_by(queryset,
                                               now_dt=self.current_datetime):
                if not self.query_group_packages(queryset, grp, result):
                    continue
                grp_count += 1
                if grp_count >= self.latest_day_count:
                    self.fill_latest_one(result, grp)
                    break

        self.filter_backends = ()
        return dict(
            title=self.get_title(),
            result=result,
            product=self.product
        )


class WebCrackTimeLineBySearchPanelWidget(BaseTimeLineBySearchPanelWidget):

    title = '首发破解'

    first_filter_backends = (SearchByCategoryFilterBackend, )

    category_slug = None

    category = None

    def setup_options(self, context, options):
        super(WebCrackTimeLineBySearchPanelWidget, self).setup_options(context, options)
        from taxonomy.models import Category
        self.category_slug = _default_slug()
        self.category = Category.objects.get_cache_by_slug(get_global_site().pk,
                                                           self.category_slug)

    def fill_latest_one(self, result, grp):
        super(WebCrackTimeLineBySearchPanelWidget, self)\
            .fill_latest_one(result, grp)
        result[-1]['url'] = self.category\
            .get_absolute_url_as(product=self.product)


class WebLatestTopBannersWidget(BaseMultiAdvWidget,
                                base.ProductPropertyWidgetMixin,
                                Widget):

    template='pages/widgets/home/banner.haml'

    def get_context(self, value=None, options=dict(), context=None):
        self.slug = 'banner-web-latest'
        return super(WebLatestTopBannersWidget, self).get_context(value=value,
                                                                  options=options,
                                                                  context=context)


class WebLatestTimeLineBySearchPanelWidget(BaseTimeLineBySearchPanelWidget):

    title = '最新发布'

    first_filter_backends = ()


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
        # compat django 1.6
        if hasattr(queryset, 'datetimes'):
            days = queryset.datetimes(self.filter_date_field, 'day',
                                      order='DESC',
                                      tzinfo=get_default_timezone())[0:self.latest_day_count]
        else:
            days = queryset \
                       .dates(self.filter_date_field, 'day', 'DESC')[0:self.latest_day_count]
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
