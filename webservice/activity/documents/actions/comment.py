# -*- coding: utf-8 -*-
from activity.documents.actions.base import *


class CommentAction(Action):

    CODE = 'comment'

    comment_class = None

    comment_id = fields.IntField()

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
        self.name = '评论'


class CommentTaskRule(TaskRule):

    CODE = 'comment'

    comment_count = fields.IntField(default=3)

    experience = fields.IntField(default=10)

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.comment_count > len(task.actions):
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

    def make_done(self):
        logger.info('task done')
        #self.uesr.profile.save()

