# -*- coding: utf-8 -*-
from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.managers import CommentManager as ThreadedCommentManager
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from django.conf import settings


class CommentManager(PassThroughManager, ThreadedCommentManager):
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


class Comment(ThreadedComment):

    objects = CommentManager.for_queryset_class(CommentQuerySet)()

    def avatar_link(self):
        if self.user and not self.user.is_anonymous():
            try:
                icon = self.user.profile.icon
                vars = (self.user_email, icon.url, self.user_name)
                return ("<a href='mailto:%s'><img style='vertical-align:middle; "
                        "margin-right:3px;' src='%s' />%s</a>" % vars)
            except:pass

        return super(Comment, self).avatar_link()

    class Meta:
        proxy = True
        ordering = ('-submit_date',)


from warehouse.models import PackageVersion
from django.contrib.comments.moderation import CommentModerator, moderator


class PackageVersionModerator(CommentModerator):

    email_notification = True

moderator.register(PackageVersion, PackageVersionModerator)
