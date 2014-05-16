# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
urlpatterns = patterns('website.cdn.views',
   url(r'^syncqueue/(?P<content_type>\w+)/(?P<object_pk>\w+)/$',
       'cdn_sync_file', name='cdn_sync_file'),
)

urlpatterns += patterns('',
    url(r'^down_ios_resource/(?P<pk>\d+)/',
        'crawler.views.download_iosapp_resource',
        name='crawler-down-iosresource'),
    url(r'^sync_resource_to_version/(?P<pk>\d+)/',
        'crawler.views.sync_resource_to_version',
        name='crawler-sync-iosversion'),
)
