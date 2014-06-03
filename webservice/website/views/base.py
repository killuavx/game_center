# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from taxonomy.models import Category, Topic, TopicalItem
from warehouse.models import Package, PackageVersion


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
        package = Package.objects.published().get(pk=pk)
        version = package.versions.latest_published()
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
        version = PackageVersion.objects.published().get(pk=pk)
        package = version.package
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
        category = Category.objects.published().get(slug=slug)
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
                 template_not_found_class=TemplateResponseNotFound,
                 *args, **kwargs):
    try:
        topic = Topic.objects.published().get(slug=slug)
        topic.packages_count = TopicalItem.objects \
            .get_items_by_topic(topic, Package).published().count()
    except ObjectDoesNotExist:
        return template_not_found_class(request)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            topic=topic
        )
    )

