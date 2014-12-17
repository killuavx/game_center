# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from apksite.views import (
    package as package_view,
    category as category_view,
    topic as topic_view,
    ranking as ranking_view,
    vender as vender_view,
    latest as latest_view,
    #home as home_view
)

pkgview = package_view.PackageDetail.as_view()
catview = category_view.CategoryView.as_view()
searchview = category_view.SearchView.as_view()
masterpieceview = topic_view.MasterpieceView.as_view()
collectionsview = topic_view.CollectionView.as_view()
collectionsdetail = topic_view.CollectionDetailView.as_view()
rankingview = ranking_view.RankingView.as_view()
crackview = latest_view.CrackTimeLineView.as_view()
latestview = latest_view.LatestTimeLineView.as_view()
#homeview = home_view.HomeView.as_view()
venderview = vender_view.VenderView.as_view()

urlpatterns = patterns('apksite.web.views',
                       #url(r'^/?$', homeview, name='home'),
                       url(r'^venders/?$', venderview, name='vender'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/detail\.html$', pkgview, name='package_detail_default'),
                       url(r'^package/(?P<pk>\d+)/(?P<package_name>[\d\w_.-]+)/(?P<template>[\w\d_]+)\.html$', pkgview, name='package_detail_template'),
                       url(r'^package/(?P<pk>\d+)(/(?P<package_name>[\d\w_.-]+))?', pkgview, name='package_detail'),
                       url(r'^game/?', catview, kwargs=dict(root_slug='game'), name='category-game'),
                       url(r'^application/?', catview, kwargs=dict(root_slug='application'), name='category-application'),
                       url(r'^search/?', searchview, name='search'),
                       url(r'^masterpiece/?$', masterpieceview, name='masterpiece'),
                       url(r'^collections/?$', collectionsview, name='collection-list'),
                       url(r'^collections/(?P<slug>[\d\w_.-]+)/?$', collectionsdetail, name='collection-detail'),
                       url(r'^ranking/?$', rankingview, name='ranking-default'),
                       url(r'^ranking/(?P<category_slug>[\d\w_.-]+)/?$', rankingview, name='ranking-list'),
                       url(r'^crack/?$', crackview, name='crack'),
                       url(r'^latest/?$', latestview, name='latest'),
                   )
