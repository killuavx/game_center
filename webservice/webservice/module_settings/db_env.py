# -*- coding: utf-8 -*-
import os

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DBA_SQL_DJANGO_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DBA_SQL_DB_NAME', 'webservice-database.sqlite'),
        'USER': os.getenv('DBA_SQL_ADMIN_USER'),
        'PASSWORD': os.getenv('DBA_SQL_ADMIN_PASSWORD'),
        'HOST': os.getenv('DBA_SQL_HOST'),
        'PORT': os.getenv('DBA_SQL_PORT'),
    }
}
