# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView
from apksite.apis import ApiFactory, ApiException
from apksite.views.base import PRODUCT


class PackageSEORedirect(Exception):

    to_url = None

    def __init__(self, to_url):
        self.to_url = to_url


class PackageDetail(DetailView):

    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'package_name'
    context_object_name = 'package'

    template_name = 'apksite/pages/package/%s.html'
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

        try:
            related_pkgs = detail_api.get_response_data(response=res, name=detail_api.related_name)
        except ApiException:
            related_pkgs = []

        category_slug = pkg.get('root_category_slug', 'game')
        ranking_api = ApiFactory.factory('ranking')
        res = ranking_api.request(category_slug=category_slug)
        try:
            ranking = ranking_api.get_response_data(response=res,
                                                    name=ranking_api.ranking_name)[0]
        except (ApiException, IndexError):
            ranking = None
        return pkg, related_pkgs, ranking

    def get_context_data(self, **kwargs):
        data = super(PackageDetail, self).get_context_data(**kwargs)
        data['product'] = self.product
        return data

    def get(self, request, *args, **kwargs):
        try:
            self.object, related_packages, ranking = self.get_object()
        except PackageSEORedirect as e:
            return redirect(to=e.to_url, permanent=True)

        context = self.get_context_data(object=self.object,
                                        related_packages=related_packages,
                                        ranking=ranking,
                                        )
        return self.render_to_response(context)


