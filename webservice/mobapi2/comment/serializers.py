# -*- coding: utf-8 -*-
from rest_framework import serializers
from comment.models import Comment
from toolkit.models import Star


class CommentSerializer(serializers.ModelSerializer):
    user_icon = serializers.SerializerMethodField('get_user_icon_url')

    star = serializers.SerializerMethodField('get_comment_star_value')

    def get_comment_star_value(self, obj):
        try:
            return obj.content_star.value
        except:
            return None

    def get_user_icon_url(self, obj):
        try:
            return obj.user.profile.icon['small'].url
        except:
            return None

    class Meta:
        model = Comment
        fields = (
            'user_name',
            'user_icon',
            'comment',
            'star',
            'submit_date',
        )


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

    def save_object(self, obj, **kwargs):
        if 'star' in self.init_data:
            star = Star(
                content_object=obj.content_object,
                user=obj.user,
                value=self.init_data['star']
            )
            obj.content_star = star
        super(CommentCreateSerializer, self).save_object(obj, **kwargs)

