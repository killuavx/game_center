# -*- coding: utf-8 -*-
import os

#DATABASES = {
#    'default': {
#        'ENGINE': os.getenv('DBA_SQL_DJANGO_ENGINE', 'django.db.backends.postgresql_psycopg2'),
#        'NAME': os.getenv('DBA_SQL_DB_NAME', 'webservice_test'),
#        'USER': os.getenv('DBA_SQL_ADMIN_USER', 'postgres'),
#        'PASSWORD': os.getenv('DBA_SQL_ADMIN_PASSWORD', ''),
#        'HOST': os.getenv('DBA_SQL_HOST', ''),
#        'PORT': os.getenv('DBA_SQL_PORT', ''),
#    },
#    'datawarehouse': {
#        'ENGINE': os.getenv('DBA_SQL_DJANGO_ENGINE_DW', 'django.db.backends.postgresql_psycopg2'),
#        'NAME': os.getenv('DBA_SQL_DB_NAME_DW', 'datawarehouse'),
#        'USER': os.getenv('DBA_SQL_ADMIN_USER_DW', 'datawarehouse'),
#        'PASSWORD': os.getenv('DBA_SQL_ADMIN_PASSWORD_DW', ''),
#        'HOST': os.getenv('DBA_SQL_HOST_DW', ''),
#        'PORT': os.getenv('DBA_SQL_PORT_DW', '5432'),
#        'OPTIONS': {'autocommit': True,}
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'webservice-database.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        },
    'datawarehouse': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'webservice-database.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
