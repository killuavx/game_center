# -*- coding: utf-8 -*-
from django.utils.timezone import now
from mongoengine import Document, fields


class Event(Document):

    imei = fields.StringField(max_length=25, required=True)

    user_pk = fields.IntField(default=-1)

    entrytype = fields.StringField(max_length=25, required=True)

    eventtype = fields.StringField(max_length=15, required=True)

    tags = fields.ListField(fields.StringField(max_length=30), required=False)

    created_datetime = fields.DateTimeField(default=now)

    #fact = fields.ReferenceField('anaylsis.documents.facts.BaseFact')
