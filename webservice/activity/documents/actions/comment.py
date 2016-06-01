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

    def _action_duplicate_object(self, action1, action2):
        cmt1, cmt2 = action1.content, action2.content
        return (cmt1.content_type_id, cmt1.object_pk) == (cmt2.content_type_id, cmt2.object_pk)

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.comment_count > len(task.actions):
            if any((self._action_duplicate_object(action, cmt_action)
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

    def build_summary(self):
        return "评论%d条获得经验%d" %(self.rule.comment_count,
                                     self.rule.experience)

    @classmethod
    def get_rule_class(cls):
        return CommentTaskRule

    @classmethod
    def get_action_class(cls):
        return CommentAction

    @classmethod
    def factory_action(cls, comment, *args, **kwargs):
        return cls.get_action_class()(content=comment)

    @classmethod
    def factory(cls, comment, action_datetime=None, *args, **kwargs):
        dt = action_datetime.astimezone() if action_datetime else comment.submit_date.astimezone()
        task = cls.factory_task(comment.user, dt)
        task.rule = cls.factory_rule()
        task.user = comment.user
        return task, task.user, cls.factory_action(comment=comment), task.rule

    @property
    def standard_count(self):
        return self.rule.comment_count

