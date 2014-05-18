# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


slug_pattern = '[\w_.-]+'

urlpatterns = patterns('website.views',
    url(r'package/(?P<package_name>%s)/$' % (slug_pattern),'iospc_package_detail_views', name='iospc_package_detail'),
    url(r'packages/collections/$', 'iospc_packages_collectios_list_views', name='iospc_packages_collections_list'),
    url(r'packages/collection/(?P<slug>%s)/' % slug_pattern, 'iospc_collection_detail_views', name='iospc_collection_detail'),
    url(r'packages/(?P<cat_slug>%s)/(?P<other_slug>\w+)/' % slug_pattern, 'iospc_packages_topic_list_views', name='iospc_packages_topic_list'),
    url(r'packages/(?P<slug>%s)/' % slug_pattern, 'iospc_packages_cat_list_views', name='iospc_packages_cat_list'),
)
