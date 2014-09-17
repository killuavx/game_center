# -*- encoding=utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
#from djrill import DjrillAdminSite
#admin.site = DjrillAdminSite()
admin.autodiscover()

rest_framework_swagger_url = url(r'^api-docs/', include('rest_framework_swagger.urls'))
urlpatterns = patterns("",
                       url(r'^mob/', include('webmob.urls')),
                       url("^admin/", include(admin.site.urls)),
                       url("^admin/analysis/", include('analysis.data_urls')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api/', include('mobapi.urls')),
                       url(r'^api/v2/', include('mobapi2.urls')),
                       #rest_framework_swagger_url,
                       url(r'^admin/cdn/', include('website.cdn.urls')),
                       url(r'^admin/toolkit/', include('toolkit.urls')),
                       url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
                       url(r'^', include('website.web.urls')),
                       url(r'^', include('website.urls')),
                       url(r'^pc/', include('website.urls_pc')),
                       )
if "mezzanine.boot" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
                            #url("^$", "mezzanine.blog.views.blog_post_list", name="home"),
                            ("^", include("mezzanine.urls")),
                            )

    handler404 = "mezzanine.core.views.page_not_found"
handler500 = "website.views.common.server_error"

from django.http import HttpResponse
# urlpatterns += patterns("", ("^robots.txt$", lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")), )
if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
                           ) + urlpatterns


#urlpatterns += patterns("",
#   url(r'^iospc/', include('website.ios_pc_urls')),
#)

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)

try:
    from mezzanine.conf import settings as mz_settings
    mz_settings._load()
except:
    pass
