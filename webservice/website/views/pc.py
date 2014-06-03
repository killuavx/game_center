# -*- coding: utf-8 -*-
from . import base
from django.conf import settings

template404 = 'pages/pc/errors/404.html'


class NotFound(base.TemplateResponseNotFound):

    template = template404


def package_detail(request, pk,
                   template_name='pages/pc/package/detail.haml', *args, **kwargs):

    ETS = settings.ENTRY_TYPES()
    return base.package_detail(request=request, pk=pk,
                               template_name=template_name,
                               template_not_found_class=NotFound,
                               product=ETS.pc,
                               *args, **kwargs)


def packageversion_detail(request, pk,
                          template_name='pages/pc/package/detail.haml',
                          *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.packageversion_detail(request=request, pk=pk,
                                      template_name=template_name,
                                      template_not_found_class=NotFound,
                                      product=ETS.pc,
                                      *args, **kwargs)


def category_page(request, slug,
                  template_name='pages/pc/category/detail.haml',
                  *args, **kwargs):
    return base.category_page(request=request, slug=slug, template_name=template_name,
                              template_not_found_class=NotFound,
                              *args, **kwargs)


def topic_detail(request, slug,
                 template_name='pages/pc/collections/detail.haml',
                 *args, **kwargs):
    return base.topic_detail(request, slug, template_name=template_name,
                             template_not_found_class=NotFound, *args, **kwargs)
