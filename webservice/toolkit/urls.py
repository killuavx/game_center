# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^restart/$', view='toolkit.views.sys_restart', name='sys.restart'),
)
