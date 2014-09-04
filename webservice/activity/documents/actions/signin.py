# -*- coding: utf-8 -*-
from activity.documents.actions.base import *
from django.utils.timezone import get_default_timezone
from datetime import datetime, timedelta

CODE = 'signin'

class SigninAction(Action):

    CODE = CODE

    name = fields.StringField(default='签到')


class SigninTaskRule(TaskRule):

    CODE = CODE

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

    CODE = CODE

    def make_done(self):
        logger.info('signin task done')
        #self.uesr.profile.save()

    @classmethod
    def get_rule_class(cls):
        return SigninTaskRule

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
        return SigninAction

    @classmethod
    def get_action(cls, user, ip_address=None, *args, **kwargs):
        return cls.get_action_class()(user=user, ip_address=ip_address)

    @classmethod
    def factory(cls, user, action_datetime=None, ip_address=None, *args, **kwargs):
        dt = action_datetime.astimezone() if action_datetime else now().astimezone()
        action = cls.get_action(user=user, ip_address=ip_address)
        rule = cls.get_rule()
        try:
            begin_dt = datetime(year=dt.year, month=dt.month, day=dt.day,
                                tzinfo=get_default_timezone())
            finish_dt = begin_dt + timedelta(days=1)
            task = cls.objects.filter(user_id=user.pk,
                                      created_datetime__gte=begin_dt,
                                      created_datetime__lt=finish_dt) \
                .order_by('-created_datetime')[0]
            return task, user, action, rule
        except IndexError:
            return cls(), user, action, rule

    def __str__(self):
        return "%s, %s" %(self.user, self.created_datetime)
