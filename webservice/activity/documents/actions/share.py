# -*- coding: utf-8 -*-
from django.utils.timezone import get_default_timezone
from datetime import datetime, timedelta
from activity.documents.actions.base import *


CODE = 'share'


class ShareAction(Action):

    CODE = CODE

    name = fields.StringField(default='分享')

    package_id = fields.IntField()

    version_id = fields.IntField()

    packageversion_class = None

    def get_packageversion_class(self):
        if not self.packageversion_class:
            from warehouse.models import PackageVersion
            self.packageversion_class = PackageVersion
        return self.packageversion_class

    @property
    def content(self):
        if not hasattr(self, '_version'):
            try:
                self._version = self.get_packageversion_class().objects.get(pk=self.version_id)
            except:
                self._version = None
        return self._version

    @content.setter
    def content(self, version):
        self.version_id = version.pk
        self.package_id = version.package_id
        self._version = version


class ShareTaskRule(TaskRule):

    CODE = CODE

    name = fields.StringField(default='分享')

    share_count = fields.IntField(verbose_name='分享数量', default=5)

    experience = fields.IntField(verbose_name='成长经验值', default=10)

    def _action_duplicate_object(self, action1, action2):
        return action1.version_id == action2.version_id

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.share_count > len(task.actions):
            if any((self._action_duplicate_object(action, share_action)
                    for share_action in task.actions)):
                raise TaskConditionDoesNotMeet('分享不同的游戏/应用')
            return super(ShareTaskRule, self).pre_update_action_check(task=task, action=action, *args, **kwargs)
        else:
            return self.STATUS.done

    def post_update_action_check(self, task, action, *args, **kwargs):
        if self.share_count == len(task.actions):
            return self.STATUS.finish
        elif self.share_count < len(task.actions):
            return self.STATUS.done
        else:
            return self.STATUS.inprogress


import logging
logger = logging.getLogger('console')


class ShareTask(Task):

    CODE = CODE

    def build_summary(self):
        return "分享%d款应用获得经验%d" % (self.rule.share_count,
                                        self.rule.experience)

    @classmethod
    def get_rule_class(cls):
        return ShareTaskRule

    @classmethod
    def get_action_class(cls):
        return ShareAction

    @classmethod
    def factory_action(cls, user, version, ip_address, *args, **kwargs):
        return cls.get_action_class()(content=version, user=user, ip_address=ip_address)

    @classmethod
    def factory(cls, user, version, action_datetime=None, ip_address=None, *args, **kwargs):
        dt = action_datetime.astimezone() if action_datetime else now().astimezone()

        task = cls.factory_task(user, dt)
        task.rule = cls.factory_rule()
        task.user = user
        return task, task.user, \
               cls.factory_action(user=user,
                                  version=version,
                                  ip_address=ip_address), \
               task.rule

    @property
    def standard_count(self):
        return self.rule.share_count
