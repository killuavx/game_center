# -*- coding: utf-8 -*-
from django.conf import settings

STARS_MIN = getattr(settings, "STARS_MIN", 1)

STARS_MAX = getattr(settings, "STARS_MAX", 5)

STARS_RANGE = list(range(STARS_MIN, STARS_MAX + 1))

