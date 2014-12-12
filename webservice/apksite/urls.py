# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from apksite.views import package as package_view, category as category_view

pkgview = package_view.PackageDetail.as_view()
catview = category_view.CategoryView.as_view()

urlpatterns = patterns('apksite.web.views',
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/detail\.html$', pkgview, name='package_detail_default'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/(?P<template>[\w\d_]+)\.html$', pkgview, name='package_detail_template'),
                       url(r'^package/(?P<pk>\d+)(/(?P<package_name>[\d\w_.-]+))?', pkgview, name='package_detail'),
                       url(r'^game/?', catview, kwargs=dict(root_slug='game'), name='category-game'),
                       url(r'^application/?', catview, kwargs=dict(root_slug='application'), name='category-application'),
                   )
