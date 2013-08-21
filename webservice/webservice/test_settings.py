from webservice.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database_test.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
EXTENDAL_APPS.append('django_nose')
EXTENDAL_APPS.append('django_jenkins')
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

