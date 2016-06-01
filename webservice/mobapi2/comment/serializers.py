# -*- coding: utf-8 -*-
from rest_framework import serializers
from comment.models import Comment, Feedback
from toolkit.models import Star
from mobapi2.serializers import ModelSerializer
from comment.helpers import comment_forbidden_words
from comment.forms import ForbiddenWordValidator


class CommentStarSerializerMixin(object):

    def get_content_star(self, obj):
        try:
            return obj.content_star.get().value
        except:
            return None


class CommentSerializer(CommentStarSerializerMixin, ModelSerializer):

    user_icon = serializers.SerializerMethodField('get_user_icon_url')

    star = serializers.SerializerMethodField('get_content_star')

    def get_user_icon_url(self, obj):
        try:
            return obj.user.profile.icon.url
        except:
            from mezzanine.core.templatetags.mezzanine_tags import gravatar_url
            try:
                return "http:%s" % gravatar_url(obj.user.profile.email, size=120)
            except:
                return None

    class Meta:
        model = Comment
        fields = (
            'user_name',
            'user_icon',
            'comment',
            'submit_date',
            'star',
        )


class CommentCreateSerializer(ModelSerializer):

    comment = serializers.CharField(
        required=True,
        max_length=200,
        min_length=3,
        validators=[
            ForbiddenWordValidator(words=comment_forbidden_words,
                                   message='您的评论含有敏感词汇')
        ])

    def save_object(self, obj, **kwargs):
        super(CommentCreateSerializer, self).save_object(obj=obj, **kwargs)
        if 'star' in self.init_data:
            star_val = self.init_data['star']
            Star(value=int(star_val),
                 user=obj.user,
                 content_object=obj.content_object,
                 ip_address=obj.ip_address,
                 by_comment=obj).save()

    class Meta:
        model = Comment
        read_only_fields = ('site',)


class FeedbackSerializer(ModelSerializer):

    class Meta:
        model = Feedback
        read_only_fields = ('site',)
