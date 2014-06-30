# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mezzanine.core.views import server_error as mz_server_error
import json


@csrf_exempt
def cdn_feedback(request, slug, *args, **kwargs):
    from website.cdn.core import Feedback
    from website.cdn.parsers import OperationResponse
    ctx1 = request.GET.get('context')
    ctx2 = request.POST.get('context')
    if not(ctx1 or ctx2) or slug != 'ccsc':
        response = OperationResponse(OperationResponse.STATUS_CODE_FAILED,
                                     'Bad Requeset')
        return HttpResponseBadRequest(response.render(),
                                      mimetype='text/xml; charset=utf-8')
    context = ctx1 or ctx2
    feedback = Feedback()
    response = feedback.process(content=context)
    return HttpResponse(response.render(),
                        mimetype='text/xml; charset=utf-8')


@csrf_exempt
def cdn_refresh_feedback(request, r_id, *args, **kwargs):
    from website.cdn.core import Feedback
    try:
        result = json.dumps(request.body)
    except Exception:
        result = None
        pass
    feedback = Feedback()
    try:
        response = feedback.process_refresh(r_id, result)
    except feedback.refresh_queue_class.DoesNotExist:
        return HttpResponse(dict(code=404),
                            mimetype='text/json; charset=utf-8')

    _publish_refresh_content_object(response.content_object)
    return HttpResponse(response.render(),
                        mimetype='text/json; charset=utf-8')


def _publish_refresh_content_object(content_object):
    from warehouse.models import PackageVersion
    if isinstance(content_object, PackageVersion):
        content_object.status = content_object.STATUS.published
        content_object.clean()
        p = content_object.package
        p.status = p.STATUS.published
        content_object.save()
        p.save()


def server_error(request, template_name='errors/custom/500.html'):
    return mz_server_error(request, template_name=template_name)
