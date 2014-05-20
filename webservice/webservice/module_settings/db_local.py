# -*- coding: utf-8 -*-
#import os
#
#DATABASES = {
#    'default': {
#        'ENGINE': os.getenv('DBA_SQL_DJANGO_ENGINE', 'django.db.backends.postgresql_psycopg2'),
#        'NAME': os.getenv('DBA_SQL_DB_NAME', 'webservice'),
#        'USER': os.getenv('DBA_SQL_ADMIN_USER', 'postgres'),
#        'PASSWORD': os.getenv('DBA_SQL_ADMIN_PASSWORD', '123456'),
#        'HOST': os.getenv('DBA_SQL_HOST', '127.0.0.1'),
#        'PORT': os.getenv('DBA_SQL_PORT', '5432'),
#    },
#    'datawarehouse': {
#        'ENGINE': os.getenv('DBA_SQL_DJANGO_ENGINE_DW', 'django.db.backends.postgresql_psycopg2'),
#        'NAME': os.getenv('DBA_SQL_DB_NAME_DW', 'datawarehouse'),
#        'USER': os.getenv('DBA_SQL_ADMIN_USER_DW', 'datawarehouse'),
#        'PASSWORD': os.getenv('DBA_SQL_ADMIN_PASSWORD_DW', ''),
#        'HOST': os.getenv('DBA_SQL_HOST_DW', '127.0.0.1'),
#        'PORT': os.getenv('DBA_SQL_PORT_DW', '5432'),
#        'OPTIONS': {'autocommit': True,}
#    }
#}
#
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
