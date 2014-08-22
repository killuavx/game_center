# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from taxonomy.models import Category, Topic, TopicalItem
from warehouse.models import Package, PackageVersion
from toolkit.helpers import get_global_site


class TemplateResponseNotFound(TemplateResponse,
                               HttpResponseNotFound):
    template = None

    def __init__(self, request, template=None, **kwargs):
        if template is None:
            template = self.template
        super(TemplateResponseNotFound, self).__init__(request, template, **kwargs)


def package_detail(request, pk,
                   template_name,
                   template_not_found_class=TemplateResponseNotFound,
                   *args, **kwargs):
    try:
        package = Package.objects.get_cache_by(pk)
        if not package or package.status != Package.STATUS.published:
            raise ObjectDoesNotExist
        version = package.get_cache_latest_version()
        if not version or version.status != PackageVersion.STATUS.published:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return template_not_found_class(request)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            package=package, version=version,
            product=kwargs.get('product'),
        )
    )


def packageversion_detail(request, pk,
                          template_name,
                          template_not_found_class=TemplateResponseNotFound,
                          *args, **kwargs):
    try:
        version = PackageVersion.objects.get_cache_by(pk=pk)
        if not version or version.status != PackageVersion.STATUS.published:
            raise ObjectDoesNotExist
        package = version.get_cache_package()
        if not package or package.status != Package.STATUS.published:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return template_not_found_class(request)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            package=package, version=version,
            product=kwargs.get('product'),
        )
    )


def category_page(request, slug,
                  template_name,
                  template_not_found_class=TemplateResponseNotFound,
                  *args, **kwargs):
    try:
        category = Category.objects.get_cache_by_slug(site_id=get_global_site().pk, slug=slug)
        if not category:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return TemplateResponseNotFound(request)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            category=category
        )
    )


def topic_detail(request, slug,
                 template_name,
                 product,
                 template_not_found_class=TemplateResponseNotFound,
                 *args, **kwargs):
    try:
        topic = Topic.objects.get_cache_by_slug(get_global_site().pk, slug=slug)
        if not topic or not topic.is_published():
            raise ObjectDoesNotExist
        topic.packages_count = lambda: TopicalItem.objects \
            .get_items_by_topic(topic, Package).published().count()
    except ObjectDoesNotExist:
        return template_not_found_class(request)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            topic=topic,
            product=product,
        )
    )

