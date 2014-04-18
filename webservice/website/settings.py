# -*- coding: utf-8 -*-
from django.conf import settings

MOGOENGINE_CONNECTS = getattr(settings, 'MOGOENGINE_CONNECTS', dict(
    systemresource=dict(
        host='localhost',
        port=27017,
        name='systemresource'
    )
))
