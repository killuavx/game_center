# -*- coding: utf-8 -*-
from django.db.models import Q
from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.managers import CommentManager as ThreadedCommentManager
from django.db.models.query import QuerySet
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField
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

    ip_address = models.IPAddressField(default=None, null=True, blank=True)

    class Meta:
        abstract = True


class FeedbackType(SiteRelated):

    objects = CurrentSitePassThroughManager()

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
        finished = self.model.STATUS.finished
        confirmed = self.model.STATUS.confirmed
        deleted = self.model.STATUS.deleted
        if for_user is not None:
            return self.filter(user=for_user)\
                .exclude(Q(status=deleted)| Q(is_owner_ignored=True))
        else:
            return self.filter(status__in=(finished, confirmed))


class Feedback(BaseLetter):

    objects = CurrentSitePassThroughManager.for_queryset_class(FeedbackQuerySet)()

    kind = models.ForeignKey(FeedbackType,
                             related_name='feedbacks')

    object_pk = models.IntegerField(_('object ID'))
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    content_object = generic.GenericForeignKey(ct_field="content_type",
                                               fk_field="object_pk")

    STATUS = Choices(
        ('posted', 'posted', '已提交'),
        ('confirmed', 'confirmed', '已确认'),
        ('finished', 'finished', '已处理'),
        ('rejected', 'rejected', '已拒绝'),
        ('deleted', 'deleted', '已删除'),
    )

    status = StatusField(default=STATUS.posted, blank=True)

    is_owner_ignored = models.BooleanField(default=False)

    replies = generic.GenericRelation(Comment)

    contact_email = models.EmailField(verbose_name=_('Contact Email'),
                                      default=None,
                                      null=True,
                                      blank=True,
                                      )

    contact_phone = models.CharField(verbose_name=_('Contact Phone'),
                                     default=None,
                                     null=True,
                                     blank=True,
                                     max_length=50)

    contact_im_qq = models.CharField(verbose_name=_('Contact IM QQ'),
                                     max_length=50,
                                     default=None,
                                     blank=True,
                                     null=True)

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


class PetitionPackageVersion(SiteRelated, models.Model):
    """
        请愿包
    """

    objects = CurrentSitePassThroughManager()

    url = models.URLField(blank=True,
                          null=True)

    title = models.CharField(max_length=300,
                             null=True,
                             blank=True)

    package_name = models.CharField(max_length=300,
                                    blank=True,
                                    null=True)

    version_name = models.CharField(max_length=300,
                                    blank=True,
                                    null=True)

    class Meta:
        verbose_name = '请愿软件'
        verbose_name_plural = '请愿软件清单'
        unique_together = (
            ('site', 'url', 'title',
             'package_name',
             'version_name'),
        )

    def get_admin_url(self):
        from mezzanine.utils.urls import admin_url
        return admin_url(self, "change", self.id)

    def __str__(self):
        if self.title:
            return self.title
        if self.package_name:
            return "%s:%s" % (self.package_name, self.version_name)
        if self.url:
            return self.url
        return None


class PetitionQuerySet(QuerySet):

    def visible(self):
        finished = self.model.STATUS.finished
        confirmed = self.model.STATUS.confirmed
        return self.filter(status__in=(finished, confirmed))


class Petition(BaseLetter):
    """
        请愿内容
    """

    objects = CurrentSitePassThroughManager.for_queryset_class(PetitionQuerySet)()

    petition_for = models.ForeignKey(PetitionPackageVersion)

    packageversion = models.ForeignKey('warehouse.PackageVersion',
                                       blank=True,
                                       null=True)

    STATUS = Choices(
        ('posted', 'posted', '已提交'),
        ('confirmed', 'confirmed', '已确认'),
        ('rejected', 'rejected', '已拒绝'),
        ('finished', 'finished', '已完成'),
        ('deleted', 'deleted', '已删除'),
    )

    status = StatusField(default=STATUS.posted, blank=True)

    verifier = models.ForeignKey(get_user_model(),
                                 verbose_name='审核人',
                                 related_name='confirm_petitions',
                                 editable=False,
                                 blank=True,
                                 null=True)

    confirmed_at = MonitorField(monitor='status',
                                editable=False,
                                when=['confirmed'])
    finished_at = MonitorField(monitor='status',
                               editable=False,
                               when=['finished'])
    rejected_at = MonitorField(monitor='status',
                               editable=False,
                               when=['rejected'])
    deleted_at = MonitorField(monitor='status',
                              editable=False,
                              when=['deleted'])

    replies = generic.GenericRelation(Comment)

    def get_absolute_url(self):
        return '#'

    def get_admin_url(self):
        from mezzanine.utils.urls import admin_url
        return admin_url(self, "change", self.id)

    class Meta:
        verbose_name = '请愿'
        verbose_name_plural = '请愿列表'
        index_together = (
            ('site', 'user', 'created',),
            ('site', 'user', 'petition_for', 'packageversion',),
            ('site', 'user', 'petition_for', 'packageversion', 'status', ),
            ('site', 'user', 'packageversion', ),
            ('site', 'user', 'packageversion', 'status', ),
            ('site', 'user', 'packageversion', 'status', 'finished_at'),
        )
        ordering = ('created', )
