from webservice.settings import *

import os
HOST_URL = os.getenv('GC_HOST_URL', '')
MEDIA_URL = HOST_URL + MEDIA_URL

EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('django_jenkins')
EXTENDAL_APPS.append('fts')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

DATABASES['default'].update(dict(
    ENGINE = os.getenv('DBA_SQL_DJANGO_ENGINE'),
    NAME = os.getenv('DBA_SQL_DB_NAME'),
    USER = os.getenv('DBA_SQL_ADMIN_USER'),
    PASSWORD = os.getenv('DBA_SQL_ADMIN_PASSWORD'),
    HOST = os.getenv('DBA_SQL_HOST'),
    PORT = os.getenv('DBA_SQL_PORT'),
    ))

COVERAGE_EXCLUDES = EXTENDAL_APPS
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.extend([
    'fts.middlewares.ThreadLocals'
])

CACHE = {
    'default':{
        'django.core.cache.backends.dummy.DummyCache',
    }

}

OUTPUT_DIR = 'reports'
COVERAGE_RCFILE = '.coveragerc'
