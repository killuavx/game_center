# -*- coding: utf-8 -*-
from django.utils.timezone import now
from mongoengine import DynamicDocument, fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class Event(DynamicDocument):

    imei = fields.StringField(max_length=25,
                              required=True)

    user_pk = fields.IntField(default=-1)

    def _set_user(self, user):
        User = get_user_model()
        if isinstance(user, User):
            return user.pk
        elif isinstance(user, AnonymousUser):
            return -1
        elif isinstance(user, int):
            return user

        raise TypeError('user type must be int type')

    def _get_user(self):
        return get_user_model().objects.get(pk=self.user_pk)

    user = property(_get_user, _set_user)

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

    package_name = fields.StringField(max_length=150, required=False)

    device = fields.StringField(max_length=100, required=False)

    manufacturer = fields.StringField(max_length=50, required=False)

    created_datetime = fields.DateTimeField(default=now)

    #fact = fields.ReferenceField('anaylsis.documents.facts.BaseFact')
    meta = {
        'indexes': ['created_datetime',
                    ('entrytype', 'eventtype', 'created_datetime'),
                    ('entrytype', 'eventtype'),
        ]
    }
