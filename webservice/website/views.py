# -*- coding: utf-8 -*-
from django.http import Http404
from os.path import splitext
from urllib.parse import urlsplit
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from warehouse.models import Package, PackageVersion


def download_package(request, package_name, version_name, *args, **kwargs):
    try:
        pv = PackageVersion.objects\
            .filter(package__package_name=package_name,
                    version_name=version_name).get()
    except PackageVersion.DoesNotExist:
        raise Http404()

    download = pv.get_download()
    if not download:
        raise Http404()

    return redirect(download.url)


def download_packageversion(request, pk, filetype=None, *args, **kwargs):
    try:
        pv = PackageVersion.objects.published().get(pk=pk)
    except PackageVersion.DoesNotExist:
        raise Http404()

    download_url = pv.get_download_static_url(filetype=filetype)
    # counter plus one
    # from website.tasks import packageversion_download_counter
    #### website/tasks.py
    # from analysis.documents.fields import DownloadCounter
    # pv.download_counter\
    #                 .add(DownloadCounter(user=request.user,
    #                                      packageversion=pv.pk,
    #                                      filetype=filetype))
    response = redirect(download_url)
    new_filename = "%s%s" % (pv.package.package_name, splitext(download_url)[-1])
    response['Content-Disposition'] = 'attachment; filename=%s' % new_filename
    bits = urlsplit(download_url)
    path = bits[2]
    response['X-Accel-Redirect'] = "%s?renameto=%s" %(path, new_filename)
    return response


def category_package_list(request, slug,
                          template='pages/categories.html',
                          extra_context=dict(), *args, **kwargs):
    return TemplateResponse(request=request, template=template, context=dict(
        category_slug=slug,
        extra_context=extra_context
    ))


def topic_package_list(request, slug, template='pages/topics/detail.html',
                        extra_context=dict(), *args, **kwargs):
    return TemplateResponse(request=request, template=template, context=dict(
        topic_slug=slug,
        extra_context=extra_context
    ))
