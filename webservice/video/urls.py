# -*- coding: utf-8 -*-
from django.conf.urls import url, include, patterns
from video.views import VideoViewSet

video_upload = VideoViewSet.as_view({'post':'create'})
video_play = VideoViewSet.as_view({'get':'play'})
video_index = VideoViewSet.as_view({'get': 'list'})

urlpatterns = patterns('',
   #url('^$', video_index, name="video-index"),
   url('^upload/?$', video_upload, name="video-upload"),
   url('^play/(?P<pk>\d+)/?$', video_play, name="video-play"),
)
