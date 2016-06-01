# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from analysis.views.web_views import EventCreateView

urlpatterns = patterns('',
   url(r'^event/$', view=EventCreateView.as_view(), name='web-analysis-eidt'),
)
