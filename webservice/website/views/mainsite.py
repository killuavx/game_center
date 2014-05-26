# -*- coding: utf-8 -*-
from mezzanine.conf import settings
from django.core.paginator import EmptyPage, Paginator

from django.http import Http404
from django.template.response import TemplateResponse
from website.response import WidgetHttpResponse
from warehouse.models import PackageVersion, Package


def packageversion_detail(request, package_name, version_name=False,
                          template='pages/packages/version-detail.html',
                          *args, **kwargs):
    if version_name is False:
        try:
            package = Package.objects.published().get(package_name=package_name)
        except Package.DoesNotExist:
            raise Http404
        version = package.versions.latest_publish()
    else:
        try:
            version = PackageVersion.objects.published() \
                .get(package__package_name=package_name, version_name=version_name)
        except PackageVersion.DoesNotExist:
            raise Http404()
        package = version.package

    return TemplateResponse(request=request, template=template, context=dict(
        package=package,
        version=version,
        package_name=package_name,
        version_name=version_name,
        ))


def category_package_list(request, slug=settings.GC_CATEGORIES_DEFAULT_SLUG,
                          template='pages/categories.html', *args, **kwargs):
    context = dict(
        slug=slug,
        ordering=request.GET.get('ordering'),
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='CategoryPackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def masterpiece_view(request, template='pages/masterpiece.html', *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='MasterpiecePackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def topics_view(request, template='pages/topics.html',
                *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsTopicListWidget')
            return response
        except Exception as e:
            raise Http404()
    return TemplateResponse(request=request, template=template, context=context)


def topic_package_list(request, slug, template='pages/topics/detail.html',
                       *args, **kwargs):
    context = dict(
        slug=slug,
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsPackageListWidget')
        except EmptyPage:
            raise Http404()
        return response

    return TemplateResponse(request=request, template=template, context=context)

