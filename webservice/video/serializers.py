# -*- coding: utf-8 -*-
from video.models import Video
from rest_framework import serializers
from rest_framework.reverse import reverse


class VideoSerializer(serializers.ModelSerializer):


    preview_url = serializers.SerializerMethodField('get_preview_url')

    def get_preview_url(self, obj):
        if obj.preview:
            return obj.preview.url
        return None

    play_url = serializers.SerializerMethodField('get_play_url')

    def get_play_url(self, obj):
        return reverse('video-play',
                       kwargs=dict(pk=obj.pk),
                       request=self.context.get('request'))

    username = serializers.CharField(source='user.username')

    created_date = serializers.SerializerMethodField('get_created_date')

    def get_created_date(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    play_src = serializers.SerializerMethodField('get_play_src')

    def get_play_src(self, obj):
        if obj.file:
            return obj.file.url
        return None

    file_time = serializers.CharField(source='file_time')

    class Meta:
        model = Video
        fields = (
            'title',
            'preview_url',
            'play_url',
            'play_src',
            'flip',
            'username',
            'file_size',
            'created_date',
            'file_time',
        )


class VideoUploadSerializer(serializers.ModelSerializer):

    video = serializers.FileField(source='file')

    play_url = serializers.SerializerMethodField('get_play_url')

    def get_play_url(self, obj):
        return reverse('video-play',
                       kwargs=dict(pk=obj.pk),
                       request=self.context.get('request')) + "?src=wap"


    preview_url = serializers.SerializerMethodField('get_preview_url')

    def get_preview_url(self, obj):
        if obj.preview:
            return obj.preview.url
        return None

    class Meta:
        model = Video
        fields = (
            'title',
            'video',
            'play_url',
            'flip',
            'preview_url',
        )

