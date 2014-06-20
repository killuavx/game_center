# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import redirect
from toolkit.helpers import get_client_event_data
from clientapp.models import ClientPackageVersion
from warehouse.models import PackageVersion
from analysis.documents.event import Event
from mezzanine.conf import settings


def _download_packageversion_response(packageversion, filetype):
    try:
        download_url = packageversion.get_download_static_url(filetype=filetype)
    except (AttributeError, ValueError):
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
    # 重命名会导致重定向失败，使得cdn地址失效
    """
    new_filename = "%s-%s%s" % (packageversion.package.package_name,
                                packageversion.version_name,
                                splitext(download_url)[-1])
    response['Content-Disposition'] = 'attachment; filename=%s' % new_filename
    bits = urlsplit(download_url)
    path = bits[2]
    response['X-Accel-Redirect'] = "%s?renameto=%s" %(path, new_filename)
    """
    return response


def _is_breakpoint_continual_download(request):
    """
        是否断点续传
    """
    request_range = request.META.get('HTTP_RANGE', None)
    if request_range is None:
        return False

    bytes_bits = request_range.strip('bytes=').split('-')
    if str(bytes_bits[0]).isnumeric() and int(bytes_bits[0]) == 0:
        return False

    return True


def _download_make_event(request, response, **kwargs):
    """
        下载事件的日志记录
    """
    if _is_breakpoint_continual_download(request):
        return None

    kwargs = get_client_event_data(request)
    entrytype = kwargs.get('entrytype', request.GET.get('entrytype', 'web'))
    imei = kwargs.get('imei', request.GET.get('imei', ''))
    user = request.user

    event = Event(**kwargs)
    event.imei = imei
    event.eventtype = 'download'
    event.entrytype = entrytype
    event.file_type = kwargs.get('filetype', None)
    event.domain = request.get_host()
    if hasattr(request, 'get_client_ip'):
        event.client_ip = request.get_client_ip()

    event.download_package_name = kwargs.get('package_name')
    event.download_version_name = kwargs.get('version_name')

    event.current_uri = request.build_absolute_uri()
    event.redirect_to = response.get('Location')
    event.referer = request.META.get('HTTP_REFERER')
    event.user = user
    event.save()
    return event


def download_package(request, package_name, version_name=None,
                     filetype=None, *args, **kwargs):
    try:
        qs = PackageVersion.objects \
            .filter(package__package_name=package_name).published()
        if version_name:
            qs = qs.filter(version_name=version_name)
        packageversion = qs.get()
    except (PackageVersion.DoesNotExist, PackageVersion.MultipleObjectsReturned):
        raise Http404()

    response = _download_packageversion_response(packageversion, filetype)
    try:
        event = _download_make_event(request, response,
                                     package_name=packageversion.package.package_name,
                                     version_name=packageversion.version_name,
                                     filetype=filetype)
    except Exception as e:
        pass
    return response


def download_packageversion(request, pk, filetype=None, *args, **kwargs):
    try:
        packageversion = PackageVersion.objects.published().get(pk=pk)
    except PackageVersion.DoesNotExist:
        raise Http404()

    response = _download_packageversion_response(packageversion, filetype)
    try:
        event = _download_make_event(request, response,
                                     package_name=packageversion.package.package_name,
                                     version_name=packageversion.version_name,
                                     filetype=filetype)
    except Exception as e:
        pass
    return response


def clientapp_latest_download(request, package_name=None,
                              *args, **kwargs):
    if not package_name:
        package_name = getattr(settings,
                               'GC_FOOTER_CLIENT_DOWNLOAD_PACKAGE_NAME', None)
    if not package_name:
        raise Http404

    try:
        app = ClientPackageVersion.objects\
            .filter(package_name=package_name)\
            .published().latest_version()
    except ClientPackageVersion.DoesNotExist:
        raise Http404

    response = redirect(app.download.url)
    try:
        event = _download_make_event(request, response,
                                     package_name=app.package_name,
                                     version_name=app.version_name)
    except Exception as e:
        pass
    return response
