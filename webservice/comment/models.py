# -*- coding: utf-8 -*-
from django.db.models import Q
from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.managers import CommentManager as ThreadedCommentManager
from django.db.models.query import QuerySet
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.managers import PassThroughManager
from django.db import models
from django.conf import settings
from tagging.fields import TagField


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


# feedback
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from toolkit.models import SiteRelated
from toolkit.managers import CurrentSitePassThroughManager
from mezzanine.core.models import TimeStamped
from django.contrib.auth import get_user_model


class BaseLetter(SiteRelated, TimeStamped):

    user = models.ForeignKey(get_user_model(),
                             verbose_name=_('user'),
                             blank=True, null=True)

    comment = models.TextField(_('comment'), max_length=300)

    class Meta:
        abstract = True


class FeedbackType(SiteRelated):

    title = models.CharField(_("Title"), max_length=300)

    slug = models.CharField(_("Slug"), max_length=300)

    level = models.IntegerField(_("Level"), max_length=5)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '反馈类型'
        verbose_name_plural = '反馈类型列表'
        unique_together = (
            ('site', 'slug'),
            ('site', 'title'),
        )
        ordering = ('-level', )


class FeedbackQuerySet(QuerySet):

    def visible(self, for_user=None):
        done = self.model.STATUS.done
        confirmed = self.model.STATUS.confirmed
        deleted = self.model.STATUS.deleted
        if for_user is not None:
            return self.filter(user=for_user)\
                .exclude(Q(status=deleted)| Q(is_owner_ignored=True))
        else:
            return self.filter(status__in=(done, confirmed))


class Feedback(BaseLetter):

    objects = CurrentSitePassThroughManager.for_queryset_class(FeedbackQuerySet)()

    kind = models.ForeignKey(FeedbackType, related_name='feedbacks')

    object_pk = models.IntegerField(_('object ID'))
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    content_object = generic.GenericForeignKey(ct_field="content_type",
                                               fk_field="object_pk")

    STATUS = Choices(
        ('posted', 'posted', '已提交'), # _('Posted')),
        ('confirmed', 'confirmed', '已确认'), #_('Confirmed')),
        ('done', 'done', '已处理'), # _('Done')),
        ('rejected', 'rejected', '已拒绝'), #_('Rejected')),
        ('deleted', 'deleted', '已删除'),#  _('Deleted')),
    )

    status = StatusField(default=STATUS.posted, blank=True)

    is_owner_ignored = models.BooleanField(default=False)

    replies = generic.GenericRelation(Comment)

    def get_absolute_url(self):
        return ''

    def __str__(self):
        return "%s, %s" %(self.content_object, self.comment)

    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = '反馈列表'
        index_together = (
            ('site', 'kind'),
            ('site', 'kind', 'created'),
            ('site', 'kind', 'status'),
            ('site', 'kind', 'status', 'created'),
            ('site', 'user'),
            ('site', 'user', 'created'),
            ('site', 'user', 'status'),
            ('site', 'user', 'status', 'created'),
        )
        ordering = ('site', 'created')

