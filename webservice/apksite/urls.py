# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from apksite.views import package as package_view

pkgview = package_view.PackageDetail.as_view()

urlpatterns = patterns('apksite.web.views',
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/detail\.html$', pkgview, name='package_detail_default'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/(?P<template>[\w\d_]+)\.html$', pkgview, name='package_detail_template'),
                       url(r'^package/(?P<pk>\d+)(/(?P<package_name>[\d\w_.-]+))?', pkgview, name='package_detail'),
                   )
