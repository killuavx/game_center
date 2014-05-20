# -*- coding: utf-8 -*-
from webservice.cms_settings import *
from webservice.module_settings.db_local import *
from webservice.module_settings.logging_test import *
from webservice.module_settings.script_local import *

DEBUG = TEMPLATE_DEBUG = True

import os

#HOST_URL = os.getenv('GC_HOST_URL', '')
#MEDIA_URL = 'http://media.ccplay.com.cn/%s/' % MEDIA_URL.strip('/')
#STATIC_URL = 'http://static.ccplay.com.cn/%s/'% STATIC_URL.strip('/')
#PUBLISH_MEDIA_URL = MEDIA_URL
#PUBLISH_STATIC_URL = STATIC_URL

HOST_URL = os.getenv('GC_HOST_URL', 'http://gc.ccplay.com.cn')
MEDIA_URL = HOST_URL + MEDIA_URL
STATIC_URL = HOST_URL + STATIC_URL
PUBLISH_MEDIA_URL= MEDIA_URL
PUBLISH_STATIC_URL = STATIC_URL

EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('django_jenkins')
EXTENDAL_APPS.append('fts')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

LOGGING.get('handlers').get('default').update(filename=join(STATIC_ROOT+'/logs/','all.log'))
LOGGING.get('handlers').get('request_handler').update(filename=join(STATIC_ROOT+'/logs/','request.log'))
LOGGING.get('handlers').get('scripts_handler').update(filename=join(STATIC_ROOT+'/logs/','scripts.log'))

# for test
TEMPLATE_LOADERS = (
    #('django.template.loaders.cached.Loader', (
    'djaml.loaders.DjamlFilesystemLoader',
    'djaml.loaders.DjamlAppDirectoriesLoader',
    #)),

    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.eggs.Loader',
)

del SESSION_ENGINE

COVERAGE_EXCLUDES = EXTENDAL_APPS
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fts/tests/fixtures'),
)

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.extend([
    'toolkit.middleware.ThreadLocals'
])

CACHE = {
    'default':{
        'django.core.cache.backends.dummy.DummyCache',
        }

}


OUTPUT_DIR = 'reports'
COVERAGE_RCFILE = '.coveragerc'

LESS_EXECUTABLE = 'lessc'

COFFEESCRIPT_EXECUTABLE = 'coffee'

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
