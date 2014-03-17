# -*- coding: utf-8 -*-
import hashlib
import os
from os.path import join
from urllib.parse import urlparse, urlunparse
from django.conf import settings
from django.utils.timezone import now
from . import feedback_signals as fb_signals
from .errors import FeedbackActionException
from .parsers import OperationResponse, OperationRequest, FeedbackContextParser
from website.documents.cdn import SyncQueue


class Processor(object):

    DATETIME_FORMAT = '%Y%m%d%H%M%S.%f'

    absolute_root_path = None

    relative_path = None

    source_path_prefix = None

    publish_path_prefix = None

    request_class = OperationRequest

    response_class = OperationResponse

    queue_class = SyncQueue

    content_type = None

    object_pk = None

    def __init__(self):
        self.source_path_prefix = self.get_source_path_prefix()
        self.publish_path_prefix = self.get_publish_path_prefix()
        self.absolute_root_path = self.get_absolute_root_path()

    def process(self, op_item, resource_path):
        queue = self.process_start_queue(op_item, resource_path)
        request_parser = self.request_class(op_item)
        response = request_parser.request()
        self.process_record_queue(response, op_item, queue)

        return response, op_item, queue

    def process_start_queue(self, op_item, resource_path):
        try:
            queue = self.queue_class.objects(content_type=self.content_type,
                                             object_pk=self.object_pk,
                                             resource_path=resource_path).get()
        except self.queue_class.DoesNotExist:
            queue = self.queue_class(content_type=self.content_type,
                                     object_pk=self.object_pk,
                                     resource_path=resource_path)
        queue.latest_op_name = op_item.op_name
        queue.save()
        return queue

    def process_record_queue(self, response, op_item, queue):
        op_item.op_result = response.result
        op_item.op_detail = response.detail
        queue.operations.insert(0, op_item)
        queue.latest_item_id = op_item.item_id
        queue.latest_op_result = op_item.op_result
        queue.latest_op_name = op_item.op_name
        queue.latest_op_status = None
        queue.latest_fb_result = None
        queue.save()
        queue.reload()
        return queue

    def get_source_path_prefix(self):
        source_host=self.get_source_host()
        ps = urlparse(settings.MEDIA_URL)
        result = list(tuple(ps))
        result[1] = source_host
        return urlunparse(result)

    def get_source_host(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().domain

    def get_publish_path_prefix(self):
        return settings.PUBLISH_MEDIA_URL
        #return settings.MEDIA_URL

    def get_absolute_root_path(self):
        return settings.MEDIA_ROOT

    @classmethod
    def get_all_file_relative_paths(cls, directory_rootpath, folder_pathname):
        """
            directory_rootpath: /data0/www/webservice/media/
            pathname: package/123/v1/

            return [
                package/123/v1/icon.png,
                package/123/v1/cover.png,
                ....
            ]
        """
        directory_pathname = join(directory_rootpath, folder_pathname)
        file_relative_paths = []
        for cur, folders, files in os.walk(join(directory_rootpath,
                                                directory_pathname)):
            cur_relative_path = cur.replace(directory_rootpath, '')\
                                                        .lstrip(os.path.sep)
            file_relative_paths += [join(cur_relative_path, file) for file in files]

        return file_relative_paths

    def generate_source_publish_paths(self, relative_filepath):
        """
            relative_filepath: package/123/v2/icon.png

            return (
                http://gc.ccplay.com.cn/media/package/123/v2/icon.png,
                http://meida.ccplay.com.cn/media/package/123/v2/icon.png
            )
        """
        source_path = join(self.source_path_prefix, relative_filepath)
        publish_path = join(self.publish_path_prefix, relative_filepath)
        return source_path, publish_path

    @classmethod
    def get_file_md5(cls, filepath):
        m = hashlib.md5()
        with open(filepath, 'rb') as f:
            m.update(f.read())
        return m.hexdigest()

    def get_sync_file_relative_paths(self):
        abs_file_path = join(self.absolute_root_path, self.relative_path)
        if os.path.isfile(abs_file_path):
            file_paths = [self.relative_path]
        else:
            file_paths = self.get_all_file_relative_paths(self.absolute_root_path,
                                                          self.relative_path)
        return file_paths


class Feedback(object):

    queue_class = SyncQueue

    context_parser = FeedbackContextParser

    response_class = OperationResponse

    def process(self, content=''):
        fb_items = self.context_parser.parse(content)
        result = self.fetch_actions(fb_items)
        return self.parse_response(result)

    def update_operation(self, fb_item, queue):
        operation = queue.fetch_operation(fb_item.item_id)
        operation.op_status = fb_item.op_status
        operation.fb_result = fb_item.fb_result
        operation.fb_datetime = now()
        operation.update_latest_to_queue()
        return operation

    def fetch_actions(self, fb_items):
        result = []
        for fb_item in fb_items:
            try:
                queue = self.queue_class.objects.get_by_item_id(fb_item.item_id)
            except self.queue_class.DoesNotExist as e:
                # skip queue DoesNotExist
                continue

            operation = self.update_operation(fb_item, queue)
            action_exception = None
            try:
                self.start_action(operation, queue)
                _result = True
            except FeedbackActionException as e:
                _result = False
                action_exception = e

            result.append((_result, operation, queue, action_exception))
        return result

    def start_action(self, operation, queue):
        fb_signals.start_action.send(sender=self.__class__,
                                     instance=self,
                                     operation=operation,
                                     queue=queue)
        if not queue.is_static():
            content_object = queue.content_object
            fb_signals.start_model_action.send(sender=content_object.__class__,
                                               instance=content_object,
                                               operation=operation,
                                               queue=queue
            )

    def parse_response(self, result):
        flag = all((r[0] for r in result))
        msgs = []
        if flag:
            code = self.response_class.STATUS_CODE_SUCCESS
        else:
            code = self.response_class.STATUS_CODE_FAILED
            for _flag, _op, _queue, _e in result:
                if not _flag:
                    msgs.append("%s,%s" %(_op.item_id, _e))
        return self.response_class(code, "\n".join(msgs))
