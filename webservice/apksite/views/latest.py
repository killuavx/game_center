# -*- coding: utf-8 -*-
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.timezone import now, make_aware, get_default_timezone
from datetime import datetime
from django.views.generic import TemplateView

from apksite.apis import ApiFactory, ApiResponseException
from apksite.views.base import PRODUCT


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


class TimeLineView(TemplateView):

    template_name = 'apksite/pages/latest/index.html'

    banner_slug = None

    product = PRODUCT

    title = None

    max_groups = 4

    def get_context_data(self, **kwargs):
        data = super(TimeLineView, self).get_context_data(**kwargs)
        data['banner_list'] = self.get_banner_list(slug=self.banner_slug)
        data['product'] = self.product
        data['title'] = self.title
        current_datetime = now().astimezone()
        pkgs = self.get_packages()
        data['result'] = self.packages_group_by_release(pkgs, current_datetime)
        self.fill_package_group_result(data['result'])
        return data

    def get_banner_list(self, slug):
        api = ApiFactory.factory('advList')
        response = api.request(slugs=slug)
        try:
            banner_list = api.get_response_data(response=response, name=api.name)[slug]
        except (ApiResponseException, IndexError) as e:
            banner_list = []

        return banner_list

    def get_packages(self):
        return []

    def packages_group_by_release(self, pkgs, current_datetime):
        groups = SortedDict()
        tz = get_default_timezone()
        for p in pkgs:
            dt = datetime.fromtimestamp(float(p['released_datetime']), tz=tz)
            d = dt.date()
            if d not in groups:
                if len(groups) >= self.max_groups:
                    break
                time_name=datesince(current_datetime, dt)
                groups[d] = dict(time_name=time_name,
                                 url=None,
                                 packages=[],
                                 )
            groups[d]['packages'].append(p)

        return list(groups.values())

    def fill_package_group_result(self, result):
        result[-1]['time_name'] = '以前'
        result[-1]['url'] = self.get_more_url()

    def get_more_url(self):
        return None


class CrackTimeLineView(TimeLineView):

    banner_slug = 'crack-a1'

    title = '首发破解'

    category_crack_id = 4

    max_request_page_size = 100

    def get_packages(self):
        api = ApiFactory.factory('latest.crackList')
        response = api.request(page_size=self.max_request_page_size)
        try:
            pkgs = api.get_response_data(response=response, name=api.name)
        except ApiResponseException:
            pkgs = []

        return pkgs

    def get_more_url(self):
        return "%s?category=%s" % (reverse(viewname='category-game'),
                                   self.category_crack_id)


class LatestTimeLineView(TimeLineView):

    banner_slug = 'latest-banner'

    title = '最新发布'

    max_request_page_size = 150

    def get_packages(self):
        api = ApiFactory.factory('latest.releaseList')
        response = api.request(page_size=self.max_request_page_size)
        try:
            pkgs = api.get_response_data(response=response, name=api.name)
        except ApiResponseException:
            pkgs = []

        return pkgs

    def get_more_url(self):
        return reverse(viewname='category-game')
