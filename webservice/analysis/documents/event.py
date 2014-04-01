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
            self.user_pk = user.pk
        elif isinstance(user, AnonymousUser):
            self.user_pk = -1
        elif isinstance(user, int):
            self.user_pk = user
        else:
            raise TypeError('user type must be int type')

    def _get_user(self):
        return get_user_model().objects.get(pk=self.user_pk)

    user = property(_get_user, _set_user)

    ENTRY_TYPES = (
        ('client', _('GC Client')),
        ('game', _('Game')),
        ('sdk', _('SDK')),
        ('web', _('Web')),
        ('wap', _('Wap')),
    )

    entrytype = fields.StringField(max_length=25,
                                   required=True,
                                   choices=ENTRY_TYPES,
                                   )

    EVENT_TYPES = (
        ('activate', _('Activate')),
        ('open', _('Open')),
        ('close', _('Close')),
        ('click', _('Click')),
        ('download', _('Download')),
        ('downloaded', _('Download finish')),
    )

    eventtype = fields.StringField(max_length=15,
                                   required=True,
                                   choices=EVENT_TYPES,
                                   )

    tags = fields.ListField(fields.StringField(max_length=100), required=False)

    package_name = fields.StringField(max_length=150, required=False)

    created_datetime = fields.DateTimeField(default=now)

    #fact = fields.ReferenceField('anaylsis.documents.facts.BaseFact')
    meta = {
        #'allow_inheritance': True,
        'indexes': ['created_datetime',
                    ('entrytype', 'eventtype', 'created_datetime'),
                    ('entrytype', 'eventtype'),
        ]

    }

    referer = fields.StringField(required=False)

    def __str__(self):
        return str(self.id)

