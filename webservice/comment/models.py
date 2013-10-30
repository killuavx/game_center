# -*- coding: utf-8 -*-
from django.contrib.comments.moderation import CommentModerator, moderator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from warehouse.models import PackageVersion
from django_comments_xtd.models import XtdComment, XtdCommentManager
from django.contrib.comments.managers import CommentManager as BaseCommentManager
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from django.conf import settings


class CommentManager(PassThroughManager, BaseCommentManager, XtdCommentManager):
    pass


class CommentQuerySet(QuerySet):

    def published(self):
        return self.filter(is_removed=False, is_public=True)

    def by_submit_order(self, newest=None):
        field = 'submit_date'
        if newest is None:
            return self
        elif newest is True:
            return self.order_by('-%s' % field)
        else:
            return self.order_by('+%s' % field)

    def with_site(self, site_id=settings.SITE_ID):
        return self.filter(site_id=site_id)


class Comment(XtdComment):

    objects = CommentManager.for_queryset_class(CommentQuerySet)()

    class Meta:
        proxy = True
        ordering = ('-submit_date',)


class PackageVersionModerator(CommentModerator):

    email_notification = True

moderator.register(PackageVersion, PackageVersionModerator)

@receiver(pre_save, sender=Comment)
def comment_pre_save(sender, instance, **kwargs):
    """
    post new comment default `is_public` allway is False
    but it cannot create comment with is_public = True
    """
    if instance.pk is None:
        instance.is_public = getattr(settings, 'COMMENTS_POST_PUBLISHED', True)

