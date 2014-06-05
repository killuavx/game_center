# -*- coding: utf-8 -*-
import os
from os.path import join
from urllib.parse import urlparse, urlunparse
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from website.cdn.utils import publish_path_to_content_type, relative_path_to_object_pk
from website.cdn.errors import StaticContentTypeError
from website.cdn.core import Processor
from website.documents import cdn


class BaseProcessor(Processor):

    operation_publish_class = cdn.PublishOperation

    operation_update_class = cdn.UpdateOperation

    operation_delete_class = cdn.DeleteOperation

    operation_check_class = cdn.CheckOperation

    operation_unzip_class = cdn.UnzipOperation

    def _package_many_operations_result(self, result):
        STATIC_CODE_SUCCESS = self.response_class.STATUS_CODE_SUCCESS
        STATIC_CODE_FAILED = self.response_class.STATUS_CODE_FAILED

        faileds = list(filter(lambda r: r[0].code == STATIC_CODE_FAILED, result))
        flag = all((res.code == STATIC_CODE_SUCCESS for res, item, queue in result))
        return flag, result, faileds

    def publish_one(self, fpath=None, filelevel=None):
        if filelevel is None:
            filelevel = self.operation_publish_class.FILE_LEVEL_REFRESH

        if fpath is None:
            fpath = self.relative_path
        abs_filepath = join(self.absolute_root_path, fpath)
        file_size = os.path.getsize(abs_filepath)
        md5 = self.get_file_md5(abs_filepath)
        item = self.operation_publish_class(
            source_path=join(self.source_path_prefix, fpath),
            publish_path=join(self.publish_path_prefix, fpath),
            file_size=file_size,
            filelevel=filelevel,
            md5=md5)
        return self.process(op_item=item, resource_path=fpath)

    def publish(self, filelevel=None):
        file_paths = self.get_sync_file_relative_paths()
        result = []
        for fpath in file_paths:
            response = self.publish_one(fpath, filelevel)
            result.append(response)

        return self._package_many_operations_result(result)

    def update_one(self, fpath=None):
        if fpath is None:
            fpath = self.relative_path
        abs_filepath = join(self.absolute_root_path, fpath)
        file_size = os.path.getsize(abs_filepath)
        md5 = self.get_file_md5(abs_filepath)
        item = self.operation_update_class(
                    source_path=join(self.source_path_prefix, fpath),
                    publish_path=join(self.publish_path_prefix, fpath),
                    file_size=file_size,
                    md5=md5)
        return self.process(op_item=item, resource_path=fpath)

    def update(self):
        file_paths = self.get_sync_file_relative_paths()
        result = []
        for fpath in file_paths:
            response = self.update_one(fpath)
            result.append(response)

        return self._package_many_operations_result(result)

    def delete_one(self, fpath=None):
        if fpath is None:
            fpath = self.relative_path
        source_path = publish_path = join(self.publish_path_prefix, fpath)
        item = self.operation_delete_class(
            source_path=source_path,
            publish_path=publish_path,
        )
        return self.process(op_item=item, resource_path=fpath)

    def delete(self):
        file_paths = self.get_sync_file_relative_paths()
        result = []
        for fpath in file_paths:
            response = self.delete_one(fpath)
            result.append(response)

        return self._package_many_operations_result(result)

    def check_one(self, fpath=None):
        if fpath is None:
            fpath = self.relative_path
        abs_filepath = join(self.absolute_root_path, fpath)
        file_size = os.path.getsize(abs_filepath)
        md5 = self.get_file_md5(abs_filepath)
        source_path = publish_path = join(self.publish_path_prefix, fpath)
        item = self.operation_check_class(
            source_path=source_path,
            publish_path=publish_path,
            file_size=file_size,
            md5=md5
        )
        return self.process(op_item=item, resource_path=fpath)

    def check(self):
        file_paths = self.get_sync_file_relative_paths()
        result = []
        for fpath in file_paths:
            response = self.check_one(fpath)
            result.append(response)

        return self._package_many_operations_result(result)

    def unzip_one(self, fpath):
        if fpath is None:
            fpath = self.relative_path
        item = self.operation_unzip_class(
            publish_path=join(self.publish_path_prefix, fpath),
        )
        return self.process(op_item=item, resource_path=fpath)

    def unzip(self):
        file_paths = self.get_sync_file_relative_paths()
        result = []
        for fpath in file_paths:
            response = self.unzip_one(fpath)
            result.append(response)

        return self._package_many_operations_result(result)


class StaticProcessor(BaseProcessor):

    CONTENT_TYPE_PATHS = None

    CONTENT_TYPE_STATIC = 'static'

    CONTENT_TYPE_MEDIA = 'media'

    def _content_type_paths(self):
        from django.conf import settings
        return {
            self.CONTENT_TYPE_MEDIA: {'url': settings.PUBLISH_MEDIA_URL,
                      'abs_path': settings.MEDIA_ROOT},
            self.CONTENT_TYPE_STATIC: {'url': settings.PUBLISH_STATIC_URL,
                       'abs_path': settings.STATIC_ROOT}
        }

    def __init__(self, relative_path, content_type=CONTENT_TYPE_STATIC):
        self.CONTENT_TYPE_PATHS = self._content_type_paths()
        self.relative_path = relative_path
        self.content_type = content_type
        if self.content_type not in self.CONTENT_TYPE_PATHS:
            raise StaticContentTypeError(
                "'%s' must in %s" %(content_type,
                                    self.CONTENT_TYPE_PATHS.keys()))

        super(StaticProcessor, self).__init__()
        self.object_pk = relative_path_to_object_pk(self.absolute_root_path,
                                                    self.relative_path)

    def get_absolute_root_path(self):
        return self.CONTENT_TYPE_PATHS[self.content_type]['abs_path']

    def get_source_path_prefix(self):
        source_host = self.get_source_host()
        url = self.get_publish_path_prefix()
        ps = urlparse(url)
        result = list(tuple(ps))
        result[1] = source_host
        if not result[0]:
            result[0] = 'http'
        return urlunparse(result)

    def get_publish_path_prefix(self):
        return self.CONTENT_TYPE_PATHS[self.content_type]['url']

    def generate_item_id(self):
        sequeue_num = now().strftime(self.DATETIME_FORMAT)
        return ":".join([self.content_type,
                         self.object_pk,
                         str(sequeue_num)])

    def process(self, op_item, resource_path):
        if not op_item.item_id:
            op_item.item_id = self.generate_item_id()
        return super(StaticProcessor, self).process(op_item, resource_path)


class ModelProcessor(BaseProcessor):

    def __init__(self, instance):
        super(ModelProcessor, self).__init__()
        self.instance = instance
        self.content_type = str(self.content_type_to_db(instance))
        self.object_pk = str(self.instance.pk)

    @classmethod
    def content_type_to_db(cls, obj):
        ct = ContentType.objects.get_for_model(obj.__class__)
        return ct.pk

    def generate_item_id(self, obj):
        ct = self.content_type_to_db(obj)
        sequeue_num = now().strftime(self.DATETIME_FORMAT)
        return ":".join([str(ct), str(obj.pk), str(sequeue_num)])

    def process(self, op_item, resource_path):
        if not op_item.item_id:
            op_item.item_id = self.generate_item_id(self.instance)
        return super(ModelProcessor, self).process(op_item, resource_path)


