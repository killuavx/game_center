# -*- coding: utf-8 -*-
from django.utils.timezone import now
from mongoengine import DynamicDocument, fields
from django.utils.translation import ugettext_lazy as _


class Event(DynamicDocument):

    imei = fields.StringField(max_length=25,
                              required=True)

    user_pk = fields.IntField(default=-1)

    ENTRY_TYPES = (
        ('client', _('CCPlay Client')),
        ('game', _('Game')),
    )

    entrytype = fields.StringField(max_length=25,
                                   required=True,
                                   choices=ENTRY_TYPES,
                                   )

    EVENT_TYPES = (
        ('activate', _('Activate')),
    )

    eventtype = fields.StringField(max_length=15,
                                   required=True,
                                   choices=EVENT_TYPES,
                                   )

    tags = fields.ListField(fields.StringField(max_length=30), required=False)

    created_datetime = fields.DateTimeField(default=now)

    #fact = fields.ReferenceField('anaylsis.documents.facts.BaseFact')
    meta = {
        'indexes': ['created_datetime',
                    ('entrytype', 'eventtype', 'created_datetime'),
                    ('entrytype', 'eventtype'),
        ]
    }
