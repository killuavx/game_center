from webservice.settings import *

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
