from webservice.settings import *

HOST_URL = 'http://173.254.227.49:8000/'
MEDIA_URL = HOST_URL + MEDIA_URL

EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('django_jenkins')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

import os
DATABASES['default'].update(dict(
    ENGINE = os.getenv('DBA_SQL_DJANGO_ENGINE'),
    NAME = os.getenv('DBA_SQL_DB_NAME'),
    USER = os.getenv('DBA_SQL_ADMIN_USER'),
    PASSWORD = os.getenv('DBA_SQL_ADMIN_PASSWORD'),
    HOST = os.getenv('DBA_SQL_HOST'),
    PORT = os.getenv('DBA_SQL_PORT'),
    ))
