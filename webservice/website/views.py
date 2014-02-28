# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render, redirect
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
    return redirect(download_url)


def category_package_list(request, slug,
                          template='pages/categories.html',
                          extra_context=dict(), *args, **kwargs):
    return TemplateResponse(request=request, template=template, context=dict(
        category_slug=slug,
        extra_context=extra_context
    ))
