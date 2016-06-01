# -*- coding: utf-8 -*-
from django.conf import settings
from os.path import dirname, join, abspath


ACCOUNT_FORBIDDEN_USERNAMES = getattr(settings,
                                      'ACCOUNT_FORBIDDEN_USERNAMES',
                                      ('signup', 'signout', 'signin',
                                        'activate', 'me', 'password'))

UC_CLIENT_CMD = join(dirname(abspath(__file__)), 'uc_client/uc_client_api.php')
