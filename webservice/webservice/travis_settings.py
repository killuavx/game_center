# -*- encoding: utf-8-*-
from webservice.settings import *
import os
HOST_URL = os.getenv('GC_HOST_URL', '')
MEDIA_URL = HOST_URL + MEDIA_URL

EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('fts')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

DATABASES['default'].update(dict(
    ENGINE=os.getenv('DBA_SQL_DJANGO_ENGINE'),
    NAME=os.getenv('DBA_SQL_DB_NAME'),
    USER=os.getenv('DBA_SQL_ADMIN_USER'),
    PASSWORD=os.getenv('DBA_SQL_ADMIN_PASSWORD'),
    HOST=os.getenv('DBA_SQL_HOST'),
    PORT=os.getenv('DBA_SQL_PORT'),
    ))

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.extend([
    'fts.middlewares.ThreadLocals'
])

CACHE = {
    'default':{
        'django.core.cache.backends.dummy.DummyCache',
        }

}

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fts/tests/fixtures'),
)

TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'
NOSE_ARGS = [
    '--tests=%s' %(",".join(EXTENDAL_APPS), ),
    '--exclude=%s' % (",".join(INTERNAL_APPS),),
    '--failed', '--stop',
    '--with-xunit',
    '--xunit-file=reports/junit.xml',
    '--with-cov',
    '--cov-report=term',
    '--cov-report=xml',
    '--cov-config=.coveragerc'
]

AAPT_CMD = None
