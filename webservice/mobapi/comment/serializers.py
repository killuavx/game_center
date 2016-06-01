# -*- coding: utf-8 -*-
from rest_framework import serializers
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_icon = serializers.SerializerMethodField('get_user_icon_url')

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
            'submit_date',
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = ('site',)

