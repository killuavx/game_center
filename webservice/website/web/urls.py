# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from website.web.views import UserAuthenticatedPanelView


account_urlpatterns = patterns('website.web.views',
                               url(r'^authpanel/?', UserAuthenticatedPanelView.as_view(), name='authpanel'),
                               url(r'^login/?', 'login', name='login'),
                               url(r'^logout/?', 'logout', name='logout'),
                               url(r'^signup/?', 'signup', name='signup'),
                               )

slug_pattern = '[\w_.-]+'
urlpatterns = patterns('website.web.views',
                       url(r'^search/?', 'search', name='search'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.]+)/detail\.html$', 'package_detail', name='package_detail_default'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.]+)/(?P<template>[\w\d_]+)\.html$', 'package_detail', name='package_detail_template'),
                       url(r'^package/(?P<pk>\d+)(/(?P<package_name>[\d\w_.]+))?', 'package_detail', name='package_detail'),
                       url(r'^packageversion/(?P<pk>\d+)/?', 'packageversion_detail'),
                       url(r'^collections/(?P<slug>%s)/?' % slug_pattern, 'topic_detail'),
                       url(r'^qrcode/?', 'qrcode_gen'),
                       url(r'^captcha/?', 'captcha', name='captcha'),
                       url(r'^accounts/', include(account_urlpatterns)),
                       url(r'^comments/$', 'comment_list', name='comment_list'),
                       url(r'^form_comment/$', 'comment_form', name='comment_form'),
                       url(r'^comment/$', 'comment', name='comment'),
                       )

