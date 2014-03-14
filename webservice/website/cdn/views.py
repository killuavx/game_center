# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from website.cdn.utils import get_content_object
from django.contrib.admin.views.decorators import staff_member_required
import json

@staff_member_required
def cdn_sync_file(request, content_type, object_pk, **kwargs):
    output = dict(code=1)
    content_object = get_content_object(content_type, object_pk)
    processor = content_object.sync_processor_class(content_object)

    op_name = request.GET.get('op_name')
    if not(op_name and hasattr(processor, op_name)):
        return HttpResponseBadRequest(json.dumps(output))

    flag, result, faileds = getattr(processor, op_name)()

    output = dict(code=0, process_all=flag, result=list())
    for res, op_item, queue in result:
        data = {
            'item_id': op_item.item_id,
            'conent_type': queue.content_type,
            'object_pk': queue.object_pk,
            'resource_path': queue.resource_path,
            'op_result': op_item.op_result,
            'op_detail': op_item.op_detail,
        }
        output['result'].append(data)

    return HttpResponse(json.dumps(output))
