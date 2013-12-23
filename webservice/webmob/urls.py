# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from webmob import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='webmob-home'),
        url(r'^packages/?$', views.packages, name='webmob-package-list'),
        url(r'^packages/(?P<pk>\d+)/?$', views.packagedetail, name='webmob-package-detail'),
        url(r'^searches/', views.searches, name='webmob-search-list'),
)
