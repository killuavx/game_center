# -*- coding: utf-8 -*-
from django.conf import settings

COLLECTIONS = getattr(settings, 'HAYSTACK_COLLECTIONS', {
    'package': None,
})
