# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from mongoengine import document, QuerySet
from mongoengine import fields
from django.utils.timezone import now


class CrawlResourceQuerySet(QuerySet):

    def by_content_object(self, content_object):
        if not isinstance(content_object, Model):
            raise TypeError()
        ct = ContentType.objects.get_for_model(content_object.__class__)
        return self.filter(content_type=str(ct.pk),
                           object_pk=str(content_object.pk))

    def by_raw_content_object(self, content_type, object_pk):
        return self.filter(content_type=str(content_type),
                           object_pk=str(object_pk))


class CrawlResource(document.DynamicDocument):

    gid = fields.StringField()

    content_type = fields.StringField()
    object_pk = fields.StringField()

    url = fields.StringField()

    file_dir = fields.StringField()

    file_path = fields.StringField()

    file_size = fields.IntField(default=0)

    file_alias = fields.StringField(required=False)

    resource_type = fields.StringField(default='default')

    relative_path = fields.StringField(required=True,
                                       unique_with=('content_type', 'object_pk')
    )

    status = fields.StringField(default='posted')

    error_code = fields.StringField(default='0')

    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)

    meta = {
        'db_alias': 'systemresource',
        'collection': 'crawl_resource',
        'indexes': [
            'created',
            'updated',
            'relative_path',
            ('content_type', 'object_pk'),
            ('content_type', 'object_pk', 'status'),
            ('content_type', 'object_pk', 'resource_type', 'status'),
            ('content_type', 'object_pk', 'resource_type'),
        ],
        'queryset_class': CrawlResourceQuerySet,
    }

