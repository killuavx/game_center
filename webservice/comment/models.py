# -*- coding: utf-8 -*-
from django.contrib.comments.moderation import CommentModerator, moderator
from warehouse.models import PackageVersion
from django_comments_xtd.models import XtdComment, XtdCommentManager
from django.contrib.comments.managers import CommentManager as BaseCommentManager


class CommentManager(BaseCommentManager, XtdCommentManager):
    pass


class Comment(XtdComment):

    objects = CommentManager()

    class Meta:
        proxy = True


class PackageVersionModerator(CommentModerator):

    email_notification = True

moderator.register(PackageVersion, PackageVersionModerator)
