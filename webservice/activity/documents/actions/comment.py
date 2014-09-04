# -*- coding: utf-8 -*-
from activity.documents.actions.base import *
from datetime import datetime, timedelta
from django.utils.timezone import get_default_timezone

CODE = 'comment'


class CommentAction(Action):

    CODE = CODE

    comment_class = None

    name = fields.StringField(default='评论')

    comment_id = fields.IntField()

    content_type_id = fields.IntField()

    object_pk = fields.StringField()

    def get_comment_class(self):
        if not self.comment_class:
            from comment.models import Comment
            self.comment_class = Comment
        return self.comment_class

    @property
    def content(self):
        if not hasattr(self, '_comment'):
            try:
                self._comment = self.get_comment_class()(pk=self.comment_id)
            except:
                self._comment = None
        return self._comment

    @content.setter
    def content(self, content):
        self.comment_id = content.pk
        self._comment = content
        self.user_id = content.user_id
        self.ip_address = content.ip_address
        self.content_type_id = content.content_type_id
        self.object_pk = str(content.object_pk)


class CommentTaskRule(TaskRule):

    CODE = CODE

    name = fields.StringField(default='评论')

    comment_count = fields.IntField(verbose_name='评论数额', default=5)

    experience = fields.IntField(verbose_name='成长经验值', default=10)

    def _comment_same_object(self, cmt1, cmt2):
        return (cmt1.content_type_id, cmt1.object_pk) == (cmt2.content_type_id, cmt2.object_pk)

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.comment_count > len(task.actions):
            if any((self._comment_same_object(action.content, cmt_action.content)
                    for cmt_action in task.actions)):
                raise TaskConditionDoesNotMeet('需要评论不同得游戏/应用')

            return super(CommentTaskRule, self).pre_update_action_check(task=task, action=action, *args, **kwargs)
        else:
            return self.STATUS.done

    def post_update_action_check(self, task, action, *args, **kwargs):
        if self.comment_count == len(task.actions):
            return self.STATUS.finish
        elif self.comment_count < len(task.actions):
            return self.STATUS.done
        else:
            return self.STATUS.inprogress


import logging
logger = logging.getLogger('console')


class CommentTask(Task):

    CODE = CODE

    def make_done(self):
        logger.info('task done')
        #self.uesr.profile.save()

    @classmethod
    def get_rule_class(cls):
        return CommentTaskRule

    @classmethod
    def get_rule(cls, *args, **kwargs):
        rule_cls = cls.get_rule_class()
        try:
            return rule_cls.objects.get(code=rule_cls.CODE)
        except:
            rule = rule_cls()
            rule.save()
            return rule

    @classmethod
    def get_action_class(cls):
        return CommentAction

    @classmethod
    def get_action(cls, comment, *args, **kwargs):
        return cls.get_action_class()(content=comment)

    @classmethod
    def factory(cls, comment, action_datetime=None, *args, **kwargs):
        dt = action_datetime.astimezone() if action_datetime else comment.submit_date.astimezone()
        action = cls.get_action(comment)
        rule = cls.get_rule()
        user = comment.user
        try:
            begin_dt = datetime(year=dt.year, month=dt.month, day=dt.day,
                                tzinfo=get_default_timezone())
            finish_dt = begin_dt + timedelta(days=1)
            qs = cls.objects.filter(user_id=user.pk,
                                    created_datetime__gte=begin_dt,
                                    created_datetime__lt=finish_dt)\
                .order_by('-created_datetime')
            task = qs[0]
            return task, user, action, rule
        except IndexError:
            return cls(), user, action, rule
