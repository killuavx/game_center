# -*- coding: utf-8 -*-
from django_comments_xtd.admin import XtdCommentsAdmin
from django_comments_xtd.models import XtdComment
from django.contrib.admin import site
from django.contrib.admin.sites import NotRegistered
from comment.models import Comment


class CommentAdmin(XtdCommentsAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.ip_address:
            obj.ip_address = request.get_client_ip()
        super(CommentAdmin, self).save_model(request, obj, form, change)

try:
    site.unregister(XtdComment)
except NotRegistered:
    pass

site.register(Comment, CommentAdmin)
