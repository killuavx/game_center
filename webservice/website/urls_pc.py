# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
slug_pattern = '[\w_.-]+'
urlpatterns = patterns('website.views.pc',
                       url(r'^package/(?P<pk>\d+)/?', 'package_detail'),
                       url(r'^packageversion/(?P<pk>\d+)/?', 'packageversion_detail'),
)
