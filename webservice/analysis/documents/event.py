# -*- coding: utf-8 -*-
from django.utils.timezone import now
from mongoengine import DynamicDocument, fields, Document, DoesNotExist
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
        ('pc', _('PC')),
        ('wap', _('Wap')),
        ('game_loading', _('Game Loading')),
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

    meta = {
        #'allow_inheritance': True,
        'indexes': ['created_datetime',
                    'imei',
                    'eventtype',
                    'entrytype',
                    ('entrytype', 'eventtype', 'created_datetime'),
                    ('entrytype', 'eventtype'),
        ]

    }

    @property
    def domain(self):
        if hasattr(self, 'site_domain'):
            return self.site_domain

        return None

    @domain.setter
    def domain(self, domain):
        self.site_domain = domain
        bits = domain.split('.')
        if bits[0] in ('ios', 'android'):
            self.platform = bits[0]
        elif bits[0] == 'gc' or bits[0].isnumeric():
            self.platform = 'android'
        else:
            self.platform = 'undefined'

    referer = fields.StringField(required=False)

    def __str__(self):
        return str(self.id)


class CellTower(Document):

    mcc = fields.IntField()
    mnc = fields.IntField()
    lac = fields.IntField()
    cid = fields.IntField(unique_with=['mcc', 'mnc', 'lac'])

    lng = fields.FloatField()
    lat = fields.FloatField()

    point = fields.GeoPointField()

    samples = fields.IntField(default=0)
    changeable = fields.BooleanField(default=False)

    created = fields.DateTimeField(default=None)
    updated = fields.DateTimeField(default=None)

    averageSignalStrength = fields.FloatField(default=0)

    meta = {
        'collection': 'cell_tower',
        'indexes': [
            'mcc',
            ('mcc', 'mnc'),
            ('mcc', 'mnc', 'lac', 'cid'),
        ]
    }


