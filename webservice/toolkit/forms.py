# -*- coding: utf-8 -*-
from mezzanine.generic.forms import ThreadedCommentForm
from django import forms
from toolkit.models import Star
from comment.models import Comment
from django.utils.translation import ugettext as _

COMMENT_MAX_LENGTH = 300


class CommentWithStarForm(ThreadedCommentForm):

    name = forms.CharField(label=_("Name"),
                           required=False,
                           max_length=50)
    email = forms.EmailField(label=_("Email"),
                             required=False)
    url = forms.URLField(label=_("Website"), required=False)

    star = forms.IntegerField(label="评星",
                              widget=forms.HiddenInput(attrs={'id': 'rating_output', 'value': 3}))
    comment = forms.CharField(label=_('Comment'), widget=forms.Textarea,
                              max_length=COMMENT_MAX_LENGTH)

    def __init__(self, request, *args, **kwargs):
        super(CommentWithStarForm, self).__init__(request, *args, **kwargs)
        self.request = request

    def get_comment_model(self):
        return Comment

    def clean_star(self):
        from mezzanine.conf import settings
        if self.cleaned_data['star'] not in settings.RATINGS_RANGE:
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
        value = self.cleaned_data["star"]
        name = self.target_object.get_starsfield_name()
        manager = getattr(self.target_object, name)
        if user.is_authenticated():
            try:
                instance = manager.get(user=user)
            except Star.DoesNotExist:
                instance = Star(user=user,
                                value=value,
                                content_object=self.target_object,
                                ip_address=comment.ip_address,
                                by_comment=comment)
                manager.add(instance)
            else:
                # do something
                pass
        else:
            instance = Star(value=value,
                            content_object=self.target_object,
                            by_comment=comment,
                            ip_address=comment.ip_address,
                            user_id=None)
            manager.add(instance)
        return instance
