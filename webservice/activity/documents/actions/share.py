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
                self._version = self.get_packageversion_class()(pk=self.version_id)
            except:
                self._version = None
        return self._version

    @content.setter
    def content(self, version):
        self.version_id = version.pk
        self.package_id = version.package.pk
        self._version = version


class ShareTaskRule(TaskRule):

    CODE = CODE

    name = fields.StringField(default='分享')

    share_count = fields.IntField(verbose_name='分享数量', default=5)

    experience = fields.IntField(verbose_name='成长经验值', default=10)

    def _share_duplicate_object(self, version1, version2):
        return version1.pk == version2.pk

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if self.share_count > len(task.actions):
            if any((self._share_duplicate_object(action.content, share_action.content)
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

    def make_done(self):
        logger.info('share task done')
        #self.uesr.profile.save()

    @classmethod
    def get_rule_class(cls):
        return ShareTaskRule

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
        return ShareAction

    @classmethod
    def get_action(cls, user, version, ip_address, *args, **kwargs):
        return cls.get_action_class()(content=version, user=user, ip_address=ip_address)

    @classmethod
    def factory(cls, user, version, action_datetime=None, ip_address=None, *args, **kwargs):
        dt = action_datetime.astimezone() if action_datetime else now().astimezone()
        action = cls.get_action(user=user, version=version, ip_address=ip_address)
        rule = cls.get_rule()
        try:
            begin_dt = datetime(year=dt.year, month=dt.month, day=dt.day,
                                tzinfo=get_default_timezone())
            finish_dt = begin_dt + timedelta(days=1)
            qs = cls.objects.filter(user_id=user.pk,
                                    created_datetime__gte=begin_dt,
                                    created_datetime__lt=finish_dt) \
                .order_by('-created_datetime')
            task = qs[0]
            return task, user, action, rule
        except IndexError:
            return cls(), user, action, rule
