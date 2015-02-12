# -*- coding: utf-8 -*-


class BaseParamFilterBackend(object):

    def filter_params(self, request, *args, **kwargs):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_queryset() must be overridden.")


class LanguageParamFilterBackend(BaseParamFilterBackend):

    language_param = 'lang'

    choices = [
        {'code': 'ZH', 'name': '中文'},
        {'code': 'EN', 'name': '英文'},
        {'code': 'OTHER', 'name': '其他'},
        ]

    lang_choices = {}
    for c in choices:
        lang_choices[c['code']] = c['code']

    def filter_params(self, request, *args, **kwargs):
        lang = request.GET.get(self.language_param)
        lang = lang.upper() if lang is not None else None
        if lang not in self.lang_choices:
            return dict()
        return dict(language=lang)


class PkgSizeParamFilterBackend(BaseParamFilterBackend):

    M = 1024 * 1024

    G = M * 1024

    size_param = 'size'

    choices = [
        {'code': '0-10m', 'name': '10M以内', 'value': (0, 10*M)},
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

    def filter_params(self, request, *args, **kwargs):
        size = request.GET.get(self.size_param)
        size = size.lower() if size is not None else None
        if size not in self.size_choices:
            return None
        min_size, max_size = self.size_choices[size]

        size_range = []
        if min_size is not None:
            size_range.append(str(min_size))
        if max_size is not None:
            size_range.append(str(max_size))

        return dict(download_size="-".join(size_range))


class PkgReportsParamFilterBackend(BaseParamFilterBackend):

    reports_param = 'reps'

    choices = [
        {'code': 'no-network', 'name': '无需网络'},
        {'code': 'no-adv', 'name': '无广告'},
        {'code': 'no-gplay', 'name': '无需谷歌市场'},
        {'code': 'no-root', 'name': '无需root权限'},
        ]

    report_choices = {}
    for c in choices:
        report_choices[c['code']] = c['code']

    def filter_params(self, request, *args, **kwargs):
        reps = request.GET.getlist(self.reports_param)
        lookups = {}
        for r in reps:
            r = r.lower()
            if r in self.report_choices:
                name = r.replace('no-', '')
                lookups['reported_%s' % name] = 'false'

        return lookups


class PaginatorParamFilterBackend(BaseParamFilterBackend):

    page_param = 'page'

    def filter_params(self, request, *args, **kwargs):
        page = request.GET.get(self.page_param)
        return dict(page=page)