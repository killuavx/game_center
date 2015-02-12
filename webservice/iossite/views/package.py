# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView
from iossite.apis import ApiFactory, ApiException
from iossite.views.base import PRODUCT, CACHE_IOSSITE_TIMEOUT, CACHE_IOSSITE_ALIAS, method_cache_page
from iossite.views.common import page_not_found


class PackageSEORedirect(Exception):

    to_url = None

    def __init__(self, to_url):
        self.to_url = to_url


class PackageDetail(DetailView):

    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'package_name'
    context_object_name = 'package'

    template_name = 'iossite/pages/package/%s.html'
    template_url_kwarg = 'template'

    product = PRODUCT

    def get_template_names(self):
        return [self.template_name % self.kwargs.get(self.template_url_kwarg, 'detail')]

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        detail_api = ApiFactory.factory('detail')
        res = detail_api.request(pk=pk)
        try:
            pkg = detail_api.get_response_data(response=res, name=detail_api.detail_name)
        except ApiException:
            raise Http404()

        if not pkg:
            raise Http404()

        package_name = self.kwargs.get(self.slug_url_kwarg)
        if not package_name:
            package_name = pkg.get('package_name')
            raise PackageSEORedirect(to_url=reverse(viewname='package_detail_default',
                                                    kwargs=dict(pk=pk, package_name=package_name)))

        if package_name and pkg['package_name'] != package_name:
            raise Http404()

        self.fill_package_category_objects(pkg)
        self.fill_package_support_devices(pkg)
        self.fill_package_support_languages(pkg)

        try:
            related_pkgs = detail_api.get_response_data(response=res, name=detail_api.related_name)
        except ApiException:
            related_pkgs = []

        category_slug = pkg['root_category']['slug']
        ranking_api = ApiFactory.factory('ranking')
        res = ranking_api.request(category_slug=category_slug)
        try:
            ranking = ranking_api.get_response_data(response=res,
                                                    name=ranking_api.ranking_name)[0]
        except (ApiException, IndexError):
            ranking = None

        return pkg, related_pkgs, ranking

    LANG_NAMES = {
        'zh': '中文',
        'en': '英文',
        'other': '其他',
    }

    def fill_package_support_languages(self, pkg):
        pkg['supported_languages'] = [self.LANG_NAMES[lang['code'].lower()]
                                      for lang in pkg['languages']
                                      if lang['code'].lower() in self.LANG_NAMES]

    def fill_package_support_devices(self, pkg):
        pass

    def fill_package_category_objects(self, pkg):
        root_category = dict(id=pkg['root_category_id'],
                             slug=pkg['root_category_slug'],
                             name=pkg['root_category_name'])
        cat_url = reverse(viewname='category-%s' %root_category['slug'])
        root_category['url'] = cat_url
        main_category = dict(id=pkg['primary_category_id'],
                             url="%s?category=%s" %(cat_url, pkg['primary_category_id']),
                             slug=pkg['primary_category_slug'],
                             name=pkg['primary_category_name'])
        pkg['root_category'] = root_category
        pkg['main_category'] = main_category
        main_categories = []
        for cat in pkg['category_leafs']:
            cat['url'] = "%s?category=%s" %(cat_url, cat['id'])
            main_categories.append(cat)
        pkg['main_categories'] = main_categories

    def get_context_data(self, **kwargs):
        data = super(PackageDetail, self).get_context_data(**kwargs)
        data['product'] = self.product
        data['product_url'] = 'http://ccplay.com.cn' + reverse('product')
        return data

    @method_cache_page(CACHE_IOSSITE_TIMEOUT,
                       cache=CACHE_IOSSITE_ALIAS,
                       key_prefix='package-detail')
    def get(self, request, *args, **kwargs):
        try:
            return self._get(request, *args, **kwargs)
        except Http404 as e:
            return page_not_found(request)

    def _get(self, reqeust, *args, **kwargs):
        try:
            self.object, related_packages, ranking = self.get_object()
        except PackageSEORedirect as e:
            return redirect(to=e.to_url, permanent=True)

        context = self.get_context_data(object=self.object,
                                        related_packages=related_packages,
                                        ranking=ranking,
                                        )
        return self.render_to_response(context)
