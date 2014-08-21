# -*- coding: utf-8 -*-
from copy import deepcopy
from django.http import Http404
from django.shortcuts import redirect
from toolkit.helpers import get_client_event_data
from clientapp.models import ClientPackageVersion
from warehouse.models import PackageVersion
from mezzanine.conf import settings
from analysis.documents.event import Event
from analysis.tasks import record_event, event_fields_datetime_format_to_isostring
from analysis.serializers import DownloadEventCreateSerializer


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

    event_data = get_client_event_data(request)
    entrytype = kwargs.get('entrytype', request.GET.get('entrytype', 'web'))
    imei = event_data.get('imei', request.GET.get('imei', ''))
    user = request.user

    # FIX client 2.2 bug
    if entrytype == 'client':
        event_data.setdefault('package_name', 'com.lion.market')

    event = Event(**event_data)
    event.imei = imei
    event.eventtype = 'download'
    event.entrytype = entrytype
    event.file_type = kwargs.get('filetype', None)
    event.domain = request.get_host()
    if hasattr(request, 'get_client_ip'):
        event.client_ip = request.get_client_ip()

    event.download_package_name = kwargs.get('download_package_name')
    event.download_version_name = kwargs.get('download_version_name')

    event.current_uri = request.build_absolute_uri()
    event.redirect_to = response.get('Location')
    event.referer = request.META.get('HTTP_REFERER')
    event.user = user
    #event.save()
    #_data = deepcopy(event._data)
    #event_fields_datetime_format_to_isostring(_data)
    #res = record_event.delay(**_data)
    return event


def _download_make_event_delay(request, response, **kwargs):
    if _is_breakpoint_continual_download(request):
        return None
    event_data = get_client_event_data(request)
    event_data['entrytype'] = kwargs.get('entrytype', request.GET.get('entrytype', 'web'))
    event_data['imei'] = event_data.get('imei', request.GET.get('imei', ''))
    event_data['file_type'] = kwargs.get('filetype', None)
    event_data['download_package_name'] = kwargs.get('download_package_name')
    event_data['download_version_name'] = kwargs.get('download_version_name')
    serializer = DownloadEventCreateSerializer\
        .factory_serializer(data=event_data,
                            request=request,
                            response=response)
    if serializer.is_valid():
        serializer.save(force_insert=True)
        return serializer, True
    else:
        return serializer, False


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

    response = _download_packageversion_response(packageversion, filetype=filetype)
    try:
        #event = _download_make_event(request, response,
        #                             download_package_name=packageversion.package.package_name,
        #                             download_version_name=packageversion.version_name,
        #                             filetype=filetype)
        r = _download_make_event_delay(request, response,
                                   download_package_name=packageversion.package.package_name,
                                   download_version_name=packageversion.version_name,
                                   filetype=filetype)
        try:
            serializer, created = r
        except:
            pass
    except Exception as e:
        pass
    return response


def download_packageversion(request, pk, filetype=None, *args, **kwargs):
    try:
        packageversion = PackageVersion.objects.get_cache_by(pk)
        if not packageversion:
            raise PackageVersion.DoesNotExist
    except PackageVersion.DoesNotExist:
        raise Http404()

    response = _download_packageversion_response(packageversion, filetype=filetype)
    #event = _download_make_event(request, response,
    #                             download_package_name=packageversion.package.package_name,
    #                             download_version_name=packageversion.version_name,
    #                             filetype=filetype)
    try:
        _download_make_event_delay(request, response,
                                   download_package_name=packageversion.package.package_name,
                                   download_version_name=packageversion.version_name,
                                   filetype=filetype)
    except Exception as e:
        print(e)
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
        #event = _download_make_event(request, response,
        #                             download_package_name=app.package_name,
        #                             download_version_name=app.version_name)
        _download_make_event_delay(request, response,
                                   download_package_name=app.package_name,
                                   download_version_name=app.version_name)
    except Exception as e:
        print(e)
        pass
    return response
