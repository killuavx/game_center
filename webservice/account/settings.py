# -*- coding: utf-8 -*-
from django.conf import settings


ACCOUNT_FORBIDDEN_USERNAMES = getattr(settings,
                                      'ACCOUNT_FORBIDDEN_USERNAMES',
                                      ('signup', 'signout', 'signin',
                                        'activate', 'me', 'password'))
