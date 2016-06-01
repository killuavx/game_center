# -*- coding: utf-8 -*-
from django.db.models import Model
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from mongoengine import (DynamicDocument,
                         DynamicEmbeddedDocument, fields, QuerySet)
from website.cdn.utils import get_content_object


class BaseOperation(DynamicEmbeddedDocument):

    item_id = fields.StringField(max_length=100, required=True, unique=True)

    op_name = fields.StringField(max_length=20, required=True)

    publish_path = fields.URLField(required=True)

    source_path = fields.URLField()

    op_result = fields.StringField(max_length=10)

    op_detail = fields.StringField(default='post finish')

    op_datetime = fields.DateTimeField(default=now)

    # feedback
    op_status = fields.StringField()

    fb_result = fields.StringField(default='NOFEEDBACK', max_length=20)

    fb_datetime = fields.DateTimeField()

    meta = {'allow_inheritance': True}

    def update_latest_to_queue(self):
        queue = self._instance
        queue.latest_item_id = self.item_id
        queue.latest_op_name = self.op_name
        queue.latest_op_result = self.op_result
        queue.latest_op_datetime = self.op_datetime
        queue.latest_fb_datetime = self.fb_datetime
        queue.latest_fb_result = self.fb_result
        queue.latest_op_status = self.op_status
        queue.save()


class UpdateOperation(BaseOperation):

    op_name = fields.StringField(default='update')

    md5 = fields.StringField(max_length=40)

    file_size = fields.LongField()

    meta = {'allow_inheritance': True}


class PublishOperation(UpdateOperation):

    op_name = fields.StringField(default='publish')

    FILE_LEVEL_NONE = 0
    FILE_LEVEL_REFRESH = 1
    FILE_LEVEL_PRELOAD = 2
    FILE_LEVELS = (
        (FILE_LEVEL_NONE, 'None'),
        (FILE_LEVEL_REFRESH, 'Refresh'),
        (FILE_LEVEL_PRELOAD, 'Preload'),
    )

    filelevel = fields.IntField(default=0,
                                min_value=0, max_value=5,
                                choices=FILE_LEVELS)

    unzip = fields.BooleanField(default=False)


    meta = {'allow_inheritance': True}


class RenameOperation(BaseOperation):

    op_name = fields.StringField(default='rename')


class DeleteOperation(BaseOperation):

    op_name = fields.StringField(default='delete')


class UnzipOperation(BaseOperation):

    op_name = fields.StringField(default='unzip')


class CheckOperation(UpdateOperation):

    op_name = fields.StringField(default='check')


class ContentTypeDocumentQuerySet(QuerySet):

    def by_content_object(self, content_object):
        if not isinstance(content_object, Model):
            raise TypeError()
        ct = ContentType.objects.get_for_model(content_object.__class__)
        return self.filter(content_type=str(ct.pk),
                           object_pk=str(content_object.pk))

    def by_raw_content_object(self, content_type, object_pk):
        return self.filter(content_type=str(content_type),
                           object_pk=str(object_pk))


class SyncQueueQuerySet(ContentTypeDocumentQuerySet):

    def get_by_item_id(self, item_id):
        return self.filter(operations__match=dict(item_id=item_id)).get()

    def get_by_latest_item_id(self, item_id):
        return self.filter(**{'operations.0.item_id': item_id}).get()


class SyncQueue(DynamicDocument):

    content_type = fields.StringField(max_length=30, required=True)

    object_pk = fields.StringField(max_length=15, required=True)

    def _get_content_object(self):
        return get_content_object(content_type=self.content_type,
                                    object_pk=self.object_pk)

    def _set_content_object(self, content_object):
        ct = ContentType.objects.get_for_model(content_object.__class__)
        self.content_type = str(ct.pk)
        self.object_pk = str(content_object.pk)

    content_object = property(_get_content_object, _set_content_object)

    resource_path = fields.StringField(required=True,
                                       unique=True,
                                       unique_with=('content_type', 'object_pk')
                                       )

    latest_item_id = fields.StringField(max_length=100)

    latest_op_name = fields.StringField()

    latest_op_result = fields.StringField(default='POST')

    latest_op_datetime = fields.DateTimeField()

    latest_op_status = fields.StringField()

    latest_fb_result = fields.StringField(default='NOFEEDBACK')

    latest_fb_datetime = fields.DateTimeField()

    operations = fields.ListField(fields.EmbeddedDocumentField(BaseOperation))

    meta = {
        'db_alias': 'systemresource',
        'collection': 'syncqueue',
        'indexes': [('content_type', 'object_pk'), 'resource_path'],
        'queryset_class': SyncQueueQuerySet,
    }

    def is_static(self):
        if self.content_type == 'static':
            return True
        return False

    def fetch_operation(self, item_id):
        for op in self.operations:
            if op.item_id == item_id:
                # small hack without wrapper_proxy
                op._instance = self
                return op
        return None


class RefreshQueueQuerySet(ContentTypeDocumentQuerySet):
    pass


class RefreshQueue(DynamicDocument):

    content_type = fields.StringField(max_length=30, required=True)

    object_pk = fields.StringField(max_length=15, required=True)

    resource_path = fields.StringField(required=True)

    publish_uri = fields.StringField(required=True)

    r_id = fields.StringField(required=True, unique=True)

    posted_datetime = fields.DateTimeField(default=now)

    fb_datetime = fields.DateTimeField()

    status = fields.StringField(default='POSTED')

    created_datetime = fields.DateTimeField()

    finished_datetime = fields.DateTimeField()

    total_second = fields.IntField()

    success_rate = fields.FloatField()

    url_status = fields.ListField(fields.DictField())

    meta = {
        'db_alias': 'systemresource',
        'collection': 'refreshqueue',
        'indexes': [
            ('content_type', 'object_pk', '-posted_datetime'),
            ('content_type', 'object_pk'),
            '-posted_datetime',
            'resource_path',
        ],
        'queryset_class': RefreshQueueQuerySet,
    }

    @property
    def content_object(self):
        return get_content_object(content_type=self.content_type,
                                  object_pk=self.object_pk)

    @content_object.setter
    def content_object(self, content_object):
        ct = ContentType.objects.get_for_model(content_object.__class__)
        self.content_type = str(ct.pk)
        self.object_pk = str(content_object.pk)
