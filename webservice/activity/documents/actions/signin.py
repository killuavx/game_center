# -*- coding: utf-8 -*-
from activity.documents.actions.base import *


class SigninAction(Action):

    CODE = 'signin'

    name = fields.StringField(default='签到')


class SigninTaskRule(TaskRule):

    CODE = 'signin'

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if len(task.actions):
            return self.STATUS.done
        else:
            return super(SigninTaskRule, self).pre_update_action_check(task=task, action=action, *args, **kwargs)

    def post_update_action_check(self, task, action, *args, **kwargs):
        if len(task.actions):
            return self.STATUS.finish
        else:
            return self.STATUS.posted


import logging
logger = logging.getLogger('console')


class SigninTask(Task):

    def make_done(self):
        logger.info('signin task done')
        #self.uesr.profile.save()
