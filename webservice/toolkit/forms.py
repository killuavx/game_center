# -*- coding: utf-8 -*-
from mezzanine.generic.forms import ThreadedCommentForm
from django import forms
from toolkit.models import Star
from comment.models import Comment
from django.utils.translation import ugettext as _

COMMENT_MAX_LENGTH = 300


class CommentWithStarForm(ThreadedCommentForm):

    star = forms.IntegerField(label="评星",
                              widget=forms.HiddenInput(attrs={'id': 'rating_output', 'value': 3}))
    comment = forms.CharField(label=_('Comment'), widget=forms.Textarea,
                              max_length=COMMENT_MAX_LENGTH)

    def get_comment_model(self):
        return Comment

    def clean_star(self):
        from mezzanine.conf import settings
        choices = list(zip(*(settings.RATINGS_RANGE,) * 2))
        if self.cleaned_data['star'] not in choices:
            raise forms.ValidationError('评星错误', code=1)

        bits = (self.data["content_type"], self.data["object_pk"])
        self.current = "%s.%s" % bits
        request = self.request
        self.previous = request.COOKIES.get("comment-star", "").split(",")
        already_rated = self.current in self.previous
        if already_rated and not self.request.user.is_authenticated():
            raise forms.ValidationError('已经过评星 ', code=10)
        return self.cleaned_data['star']

    def save(self, request):
        comment = super(CommentWithStarForm, self).save(request=request)
        self.save_star(request, comment)
        return comment

    def save_star(self, request, comment=None):
        user = request.user
        value = self.cleaned_data["value"]
        name = self.target_object.get_starfield_name()
        manager = getattr(self.target_object, name)
        if user.is_authenticated():
            try:
                instance = manager.get(user=user)
            except Star.DoesNotExist:
                instance = Star(user=user,
                                value=value,
                                by_comment=comment)
                manager.add(instance)
            else:
                # do something
                pass
        else:
            instance = Star(value=value,
                            by_comment=comment,
                            user_id=None)
            manager.add(instance)
        return instance
