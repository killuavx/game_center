# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webservice.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webservice.cms_localserver_settings')

app = Celery('webservice')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

def my_on_failure(self, exc, task_id, args, kwargs, einfo):
    print('Oh no! Task failed: {0!r}'.format(exc))

app.conf.update(
    CELERY_ANNOTATIONS={'*': {'on_failure': my_on_failure}}
)
