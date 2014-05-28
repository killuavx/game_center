# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from taxonomy.models import Category, Topic, TopicalItem
from warehouse.models import Package, PackageVersion

template404 = 'pages/pc/errors/404.html'


class TemplateResponseNotFound(TemplateResponse,
                               HttpResponseNotFound):
    pass


def _package_categories(package):
    cats = [cat for cat in package.categories.all() if cat.is_leaf_node()]
    main_category = cats[0]
    return main_category, cats


def _breadcrumbs_instances_from(package, category):
    breadcrumb_insts = []
    for cat in category.get_ancestors(include_self=True):
        cat.bcname = cat.name
        breadcrumb_insts.append(cat)
    package.bcname = package.title
    breadcrumb_insts.append(package)
    return breadcrumb_insts


def package_detail(request, pk,
                   template_name='pages/pc/package/detail.haml',
                   *args, **kwargs):
    try:
        package = Package.objects.published().get(pk=pk)
        version = package.versions.latest_published()
    except ObjectDoesNotExist:
        return TemplateResponseNotFound(request, template=template404)

    main_category, all_categories = _package_categories(package)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            package=package, version=version,
            main_category=main_category, all_categories=all_categories,
            breadcrumbs=_breadcrumbs_instances_from(package, main_category)
        )
    )


def packageversion_detail(request, pk,
                          template_name='pages/pc/package/detail.haml',
                          *args, **kwargs):
    try:
        version = PackageVersion.objects.published().get(pk=pk)
        package = version.package
    except ObjectDoesNotExist:
        return TemplateResponseNotFound(request, template=template404)

    main_category, all_categories = _package_categories(package)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            package=package, version=version,
            main_category=main_category, all_categories=all_categories,
            breadcrumbs=_breadcrumbs_instances_from(package, main_category)
        )
    )


def category_page(request, slug,
                  template_name='pages/pc/category/detail.haml',
                  *args, **kwargs):
    try:
        category = Category.objects.published().get(slug=slug)
    except ObjectDoesNotExist:
        return TemplateResponseNotFound(request, template=template404)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            category=category
        )
    )


def topic_detail(request, slug,
                 template_name='pages/pc/collections/detail.haml',
                 *args, **kwargs):
    try:
        topic = Topic.objects.published().get(slug=slug)
        topic.packages_count = TopicalItem.objects\
            .get_items_by_topic(topic, Package).published().count()
    except ObjectDoesNotExist:
        return TemplateResponseNotFound(request, template=template404)

    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            topic=topic
        )
    )
