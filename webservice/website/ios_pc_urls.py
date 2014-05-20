# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


slug_pattern = '[\w_.-]+'

urlpatterns = patterns('website.views',
    url(r'^package/(?P<package_name>%s)/$' % (slug_pattern),'iospc_package_detail_views', name='iospc_package_detail'),
    url(r'^collections/$', 'iospc_collectios_list_views', name='iospc_collections_list'),
    url(r'^topic/(?P<slug>%s)/$' % slug_pattern, 'iospc_collection_detail_views', name='iospc_masterpiece_packages'),
    url(r'^vendor/(?P<slug>%s)/(?:(?P<pk>\d+)/)?$' % slug_pattern, 'iospc_vendors_list_views', name='iospc_vendors_list'),
    url(r'^collection/(?P<slug>%s)/$' % slug_pattern, 'iospc_collection_detail_views', name='iospc_collection_detail'),
    url(r'^category/(?P<cat_slug>%s)/topic/(?P<other_slug>\w+)/$' % slug_pattern, 'iospc_packages_topic_list_views', name='iospc_packages_topic_list'),
    url(r'^category/(?P<slug>%s)/$' % slug_pattern, 'iospc_packages_cat_list_views', name='iospc_packages_cat_list'),
    url(r'^category/(?P<cat_slug>%s)/(?P<other_slug>\w+)/$' % slug_pattern, 'iospc_packages_topic_list_views', name='iospc_packages_other_list'),
)
