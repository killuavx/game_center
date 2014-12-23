# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from apksite.views import (
    package as package_view,
    category as category_view,
    topic as topic_view,
    ranking as ranking_view,
    vendor as vendor_view,
    latest as latest_view,
    home as home_view,
    product as product_view,
    auth as auth_view
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
homeview = home_view.HomeView.as_view()
vendorview = vendor_view.VendorView.as_view()
productview = product_view.ProductView.as_view()

authpanel = auth_view.UserAuthenticatedPanelView.as_view()



account_urlpatterns = patterns('apksite.views.auth',
                               url(r'^authpanel/?', authpanel, name='authpanel'),
                               url(r'^login/?', 'login', name='login'),
                               url(r'^logout/?', 'logout', name='logout'),
                               url(r'^signup/?', 'signup', name='signup'),
                               )

comment_urlpatterns = patterns('apksite.views.comment',
                               url(r'^comments/$', 'comment_list', name='comment_list'),
                               url(r'^form_comment/$', 'comment_form', name='comment_form'),
                               url(r'^comment/$', 'comment', name='comment'),
                               url(r'^comment/remove/(?P<pk>\d+)/?$', 'comment_remove', name='comment_remove'),
                               )

urlpatterns = patterns('',
                       url(r'^/?$', homeview, name='home'),
                       url(r'^vendors/?$', vendorview, name='vendor'),
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
                       url(r'^product/?$', productview, name='product'),

                       url(r'^captcha/?', 'apksite.views.auth.captcha', name='captcha'),
                       url(r'^accounts/', include(account_urlpatterns)),
                       url(r'^', include(comment_urlpatterns)),
                   )





handler404 = "apksite.views.common.page_not_found"
handler500 = "apksite.views.common.server_error"
