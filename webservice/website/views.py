# -*- coding: utf-8 -*-
from os.path import splitext
from urllib.parse import urlsplit
from django.conf import settings
from mezzanine.conf import settings
from django.core.paginator import EmptyPage

from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.vary import vary_on_headers

from .response import WidgetHttpResponse
from warehouse.models import PackageVersion


def _download_packageversion_response(packageversion, filetype):
    try:
        download_url = packageversion.get_download_static_url(filetype=filetype)
    except ValueError:
        raise Http404()
    # counter plus one
    # from website.tasks import packageversion_download_counter
    #### website/tasks.py
    # from analysis.documents.fields import DownloadCounter
    # pv.download_counter\
    #                 .add(DownloadCounter(user=request.user,
    #                                      packageversion=pv.pk,
    #                                      filetype=filetype))
    response = redirect(download_url)
    new_filename = "%s%s" % (packageversion.package.package_name, splitext(download_url)[-1])
    response['Content-Disposition'] = 'attachment; filename=%s' % new_filename
    bits = urlsplit(download_url)
    path = bits[2]
    response['X-Accel-Redirect'] = "%s?renameto=%s" %(path, new_filename)
    return response


def download_package(request, package_name, version_name=None,
                     filetype=None, *args, **kwargs):
    try:
        qs = PackageVersion.objects\
            .filter(package__package_name=package_name).published()
        if version_name:
            qs = qs.filter(version_name=version_name)
        packageversion = qs.get()
    except (PackageVersion.DoesNotExist, PackageVersion.MultipleObjectsReturned):
        raise Http404()

    return _download_packageversion_response(packageversion, filetype)


def download_packageversion(request, pk, filetype=None, *args, **kwargs):
    try:
        packageversion = PackageVersion.objects.published().get(pk=pk)
    except PackageVersion.DoesNotExist:
        raise Http404()

    return _download_packageversion_response(packageversion, filetype)


def packageversion_detail(request, package_name, version_name,
                          template='pages/package/version-detail.html',
                          *args, **kwargs):
    return TemplateResponse(request=request, template=template, context=dict(
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


def cdn_feedback(request, slug, *args, **kwargs):
    from website.cdn.core import Feedback
    ctx1 = request.GET.get('context')
    ctx2 = request.POST.get('context')
    if not(ctx1 or ctx2) or slug != 'cscc':
        return HttpResponseBadRequest()
    context = ctx1 or ctx2
    feedback = Feedback()
    response = feedback.process(content=context)
    return HttpResponse(response.render(), mimetype='text/xml; charset=utf-8')

