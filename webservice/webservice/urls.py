# -*- encoding=utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
#from djrill import DjrillAdminSite
#admin.site = DjrillAdminSite()
admin.autodiscover()

rest_framework_swagger_url = url(r'^api-docs/', include('rest_framework_swagger.urls'))
urlpatterns = staticfiles_urlpatterns()
urlpatterns += patterns('',
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),

    rest_framework_swagger_url,
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('mobapi.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mob/', include('webmob.urls')),
    url(r'^admin/toolkit/', include('toolkit.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
           {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
       url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)
