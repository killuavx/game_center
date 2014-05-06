# -*- coding: utf-8 -*-
from django.conf import settings


ACCOUNT_FORBIDDEN_USERNAMES = getattr(settings,
                                      'ACCOUNT_FORBIDDEN_USERNAMES',
                                      ('signup', 'signout', 'signin',
                                        'activate', 'me', 'password'))

UC_CLIENT_CMD = '/data0/www/bbs/uc_client/uc_client_api.php'