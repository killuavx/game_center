# -*- encoding=utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import warehouse.views_rest
import taxonomy.views_rest
from rest_framework import routers
rest_router = routers.DefaultRouter()
rest_router.register('authors', warehouse.views_rest.AuthorViewSet)
rest_router.register('packages', warehouse.views_rest.PackageViewSet)
rest_router.register('categories', taxonomy.views_rest.CategoryViewSet)

from django.contrib import admin
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()
admin.autodiscover()
#admin.site.disable_action('delete_selected')


urlpatterns = staticfiles_urlpatterns()
urlpatterns += patterns('',
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(rest_router.urls)),

    url(r'^grappelli/', include('grappelli.urls') ),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns = patterns('',
       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
           {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
       url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns