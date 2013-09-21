from webservice.settings import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database_dev.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('django_jenkins')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

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
