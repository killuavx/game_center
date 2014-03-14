# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
urlpatterns = patterns('website.cdn.views',
   url(r'^syncqueue/(?P<content_type>\w+)/(?P<object_pk>\w+)/$',
       'cdn_sync_file', name='cdn_sync_file'),
)
