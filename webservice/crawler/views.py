# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import json
from crawler.models import *
from crawler.tasks import *


def aria2_linktag(text):
    url = 'http://aria2.ccplay.com.cn/'
    mask = '<a href="%(url)s" target="webui-aria2">%(text)s</a>'
    return mask % {'url': url, 'text': text}

@staff_member_required
def download_iosapp_resource(request, pk, **kwargs):
    app = get_object_or_404(IOSAppData, pk=pk)
    try:
        task = DownloadIOSAppResourceTask()
        gids = task.download_app_resource(app)
        del task
        output = dict(
            code=0,
            msg='%s downloading...' % aria2_linktag('status'),
            result=gids,
        )
    except Exception as e:
        output = dict(code=1, msg=e)
        return HttpResponse(json.dumps(output))
    return HttpResponse(json.dumps(output))


@staff_member_required
def sync_resource_to_version(request, pk, **kwargs):
    app = get_object_or_404(IOSAppData, pk=pk)
    try:
        task = SyncIOSPackageVersionResourceFromCrawlResourceTask()
        flag = task.sync_resourcefiles_to_version(app, status=False)
        if flag is None:
            raise Exception('没有对应的版本数据')
        del task
        output = dict(
            code=0,
            msg='ok',
            result=flag,
        )
        dw_task = DownloadIOSAppResourceTask()
        dw_task.checkout_app_resources(app)
        del dw_task
    except Exception as e:
        output = dict(code=1, msg=str(e))
        return HttpResponse(json.dumps(output))
    return HttpResponse(json.dumps(output))


@staff_member_required
def down_sync_to_version(request, pk, **kwargs):
    app = get_object_or_404(IOSAppData, pk=pk)
    try:
        dw_task = DownloadIOSAppResourceTask()
        gids = dw_task.download_app_resource(app)

        sync_task = SyncIOSPackageVersionResourceFromCrawlResourceTask()
        flag = sync_task.sync_resourcefiles_to_version(app, status=False)
        if flag is None:
            raise Exception('没有对应的版本数据')

        output = dict(
            code=0,
            msg='ok',
            data=gids,
            result=flag,
            )
        del dw_task
        del sync_task
    except Exception as e:
        output = dict(code=1, msg=str(e))
        return HttpResponse(json.dumps(output))
    return HttpResponse(json.dumps(output))


@staff_member_required
def chk_resource_dl_status(request, pk, **kwargs):
    app = get_object_or_404(IOSAppData, pk=pk)
    try:
        output = dict(
            code=0,
            msg='ok',
            result=True,
        )
        dw_task = DownloadIOSAppResourceTask()
        dw_task.checkout_app_resources(app)
        del dw_task
    except Exception as e:
        output = dict(code=1, msg=str(e))
        return HttpResponse(json.dumps(output))
    return HttpResponse(json.dumps(output))


# 替换
download_iosapp_resource = down_sync_to_version

chk_resource_dl_status = sync_resource_to_version
