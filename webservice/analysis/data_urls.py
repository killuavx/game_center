# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from analysis.views import data_views

urlpatterns = patterns('analysis.views.data_views',
   url(r'^product/?$',
       data_views.ProductActivateListView.as_view(),
       name='analysis_product_activate_list'),
   url(r'^product/(?P<entrytype>[\w_.-]+)/$',
       data_views.ProductChannelActivateListView.as_view(),
       name='analysis_product_channel_activate_list'),
   url(r'^product/(?P<entrytype>[\w_.-]+)/(?P<channel>[\w_.-]+)/$',
       data_views.ProductChannelCycleActivateListView.as_view(),
       name='analysis_product_channel_activate_detail'),
   url(r'^download/?$',
       data_views.PackageDownloadListView.as_view(),
       name='analysis_package_download_list'),
   url(r'^download/(?P<package_name>[\w_.]+)/$',
       data_views.ProductPackageDownloadListView.as_view(),
       name='analysis_package_download_detail'),


   url(r'^crack/$',
       data_views.CrackPackageListView.as_view(),
       name='analysis_package_crack_list'),

   url(r'^crack/(?P<package_name>[\w_.]+)/download/$',
       data_views.CrackPackageDownloadListView.as_view(),
       name='analysis_package_crack_download_detail'),

   url(r'^crack/(?P<package_name>[\w_.]+)/activate/$',
       data_views.CrackPackageActivateListView.as_view(),
       name='analysis_package_crack_activate_list'),

   url(r'^crack/(?P<package_name>[\w_.]+)/activate/(?P<entrytype>[\w_.-]+)/(?P<channel>[\w_.-]+)/$',
       data_views.CrackPackageChannelActivateListView.as_view(),
       name='analysis_package_crack_activate_detail'),
)
