# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.template.response import TemplateResponse

slug_pattern = '[\w_.-]+'
urlpatterns = patterns('website.views.download',
                        url(r'^download/packageversion/(?P<pk>\d+)(/(?P<filetype>\w+)?)?',
                            'download_packageversion', name='download_packageversion'),
                        url(r'^download/package/(?P<package_name>%s)'
                            '(/(?P<version_name>%s)?)?(/(?P<filetype>\w+)?)?' % (slug_pattern, slug_pattern),
                            'download_package', name='download_package'),
                        url(r'download/client/(?P<package_name>[\w_.-]*)',
                            'clientapp_latest_download',
                            name='clientapp-latest_download')
                        )


urlpatterns += patterns('website.views.common',
                        url(r'^feedbacks/cdn/(?P<slug>%s)' % slug_pattern, 'cdn_feedback', name='cdn_feedback'),
                        url("^social/redirect\.html$", lambda r: TemplateResponse(request=r, template='bd_frontia_jump.html')),
                        )

