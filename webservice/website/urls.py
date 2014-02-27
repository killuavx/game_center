# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from warehouse.models import PackageVersion

urlpatterns = patterns('website.views',
        #url(r'^packages/?', views.list_view, name='website_package_list'),
        #url(r'^packages/(?P<pk>\d+)/?', views.detail_view, name='website_package_detail'),
        #url(r'^packages/(?P<pk>\d+)/(?P<vpk>\d+)/?', views.version_view, name='website_package_version'),
        url(r'^download/packageversion/(?P<pk>\d+)(/(?P<filetype>\w+)?)?', 'download_packageversion', name='download_packageversion'),
        url(r'^categories/(?P<slug>[^/]+)/?', 'category_package_list', name='category_package_list')
)

