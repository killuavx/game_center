# -*- coding: utf-8 -*-
from activity.documents.actions.base import *

import logging
logger = logging.getLogger('console')

CODE = 'install'


class InstallAction(Action):

    CODE = CODE

    name = fields.StringField(default='安装')

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
        if version.has_award:
            self.coin = version.award_coin

    def build_summary(self):
        version = self.content
        if version.has_award:
            return "安装奖励%d金币" % version.award_coin
        return "无奖励"

    def execute(self):
        dt = self.created_datetime
        version = self.content
        if version.has_award:
            log = CreditLog.factory(exchangable=self,
                                    user=self.user,
                                    credit_datetime=dt)
            log.save()

    def can_execute(self):
        cls = self.__class__
        qs = cls.objects.with_user(user=self.user)\
            .in_date(self.created_datetime.astimezone())\
            .filter(version_id=self.version_id)
        if qs.count():
            return False
        return self.content.has_award

    def save(self, *args, **kwargs):
        version = self.content
        if version.has_award:
            self.credit_exchange_coin = version.award_coin
        return super(InstallAction, self).save(*args, **kwargs)


class InstallTaskRule(TaskRule):

    CODE = CODE

    name = fields.StringField(default='安装')

    install_count = fields.IntField(verbose_name='安装数量', default=3)

    experience = fields.IntField(verbose_name='成长经验值', default=10)

    def _action_duplicate_object(self, action1, action2):
        return action1.version_id == action2.version_id

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.install_count > len(task.actions):
            if any((self._action_duplicate_object(action, install_action)
                    for install_action in task.actions)):
                raise TaskConditionDoesNotMeet('安装不同的游戏/应用')
            return super(InstallTaskRule, self).pre_update_action_check(task=task, action=action, *args, **kwargs)
        else:
            return self.STATUS.done

    def post_update_action_check(self, task, action, *args, **kwargs):
        if self.install_count == len(task.actions):
            return self.STATUS.finish
        elif self.install_count < len(task.actions):
            return self.STATUS.done
        else:
            return self.STATUS.inprogress


class InstallTask(Task):

    CODE = CODE

    def build_summary(self):
        return "安装%d款应用获得经验%d" % (self.rule.install_count,
                                  self.rule.experience)

    @classmethod
    def get_rule_class(cls):
        return InstallTaskRule

    @classmethod
    def get_action_class(cls):
        return InstallAction

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
                                  ip_address=ip_address), task.rule

    @property
    def standard_count(self):
        return self.rule.install_count



