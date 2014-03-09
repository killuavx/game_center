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
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api/', include('mobapi.urls')),
                       rest_framework_swagger_url,
                       url(r'^admin/toolkit/', include('toolkit.urls')),
                       url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
                       )
if "mezzanine.boot" in settings.INSTALLED_APPS:
    from mezzanine.core.views import direct_to_template
    urlpatterns += patterns('',
                            url("^$", direct_to_template, {"template": "pages/comingsoon.html"}, name="comingsoon"),
                            url("^$", "mezzanine.blog.views.blog_post_list", name="home"),
                            #url("^$", "mezzanine.blog.views.blog_post_list", name="commingsoon"),
                            url("^", include('website.urls')),
                            ("^", include("mezzanine.urls")),
                            )

    handler404 = "mezzanine.core.views.page_not_found"
    handler500 = "mezzanine.core.views.server_error"

from django.http import HttpResponse
urlpatterns += patterns("",
                        ("^robots.txt$", lambda r: HttpResponse("User-agent: *\nDisallow: /",
                                                                mimetype="text/plain")),
                        )
if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
                           ) + urlpatterns

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

saved_file.connect(generate_aliases_global)
