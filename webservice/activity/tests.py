# -*- coding: utf-8 -*-
from unittest.mock import Mock
from django.test import TestCase


class WarehouseDSL(object):
    pass


class ActivityDSL(object):

    def giftbag_already_exists_for(self, package, version=None,
                                   published_datetime=None,
                                   expire_datetime=None,
                                   ):
        pass

    def gitbag_already_has_many_gitcard(self, gitbag, card_code):
        pass


class GitBagTest(TestCase):

    def _test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


from should_dsl import should, should_not
from account.models import User
from activity.documents.actions.comment import *


from mongoengine import register_connection
from django.conf import settings
con_key = 'data_center'
con_opts = settings.MOGOENGINE_CONNECTS[con_key]
register_connection(alias=con_key,
                    name=con_opts.get('name'),
                    host=con_opts.get('host'),
                    port=con_opts.get('port'))

import logging
logger = logging.getLogger('console')


class TaskTestCase(TestCase):

    action_class = None

    task_class = None

    rule_class = None

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class()
            rule.save()
        return rule

    def setUp(self):
        CreditLog.objects.delete()
        self.user = User.objects.get(username='killuavx')
        self.user.profile.experience = 0
        self.user.profile.coin = 0
        self.user.profile.level = 0
        self.user.save()

    def tearDown(self):
        self.task_class.objects.delete()
        self.action_class.objects.delete()
        self.rule_class.objects.delete()
        CreditLog.objects.delete()
        if hasattr(self, 'user'):
            self.user.profile.experience = 0
            self.user.profile.coin = 0
            self.user.profile.level = 0
            self.user.save()


class CommentTestCase(TaskTestCase):

    action_class = CommentAction

    task_class = CommentTask

    rule_class = CommentTaskRule

    rule = None

    def get_rule(self):
        try:
            rule = CommentTaskRule.objects.get(code=CommentTaskRule.CODE)
        except:
            rule = CommentTaskRule(name='post comment', comment_count=3)
            rule.save()
        return rule

    def test_add_duplicate_action(self):
        self.rule = self.get_rule()
        self.rule.comment_count |should| equal_to(3)

        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task

        same_cmt = user.comment_comments.all()[1]
        action = CommentAction(content=same_cmt)
        task.process(user=user, action=action, rule=self.rule)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(1).items

        action = CommentAction(content=same_cmt)
        (task.process, user, action, task.rule) |should| throw(TaskConditionDoesNotMeet)
        task.actions |should| have(1).items

    def test_finish_comment_task(self):
        self.rule = self.get_rule()
        self.rule.comment_count |should| equal_to(3)

        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task
        task.make_done = Mock(return_value=None)

        cmt1 = user.comment_comments.all()[1]
        action = CommentAction(content=cmt1)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(False)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(1).items

        cmt2 = user.comment_comments.all()[2]
        action = CommentAction(content=cmt2)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(False)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(2).items

        cmt3 = user.comment_comments.all()[10]
        action = CommentAction(content=cmt3)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(CommentTask.STATUS.done)
        task.actions |should| have(3).items

        cmt3 = user.comment_comments.all()[8]
        action = CommentAction(content=cmt3)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)

    def test_factory(self):
        self.rule = self.get_rule().comment_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        cmt1 = user.comment_comments.all()[1]
        cmt2 = user.comment_comments.all()[2]
        cmt3 = user.comment_comments.all()[10]
        cmt4 = user.comment_comments.all()[11]
        CommentTask.make_done = Mock(return_value=None)

        action_datetime = now().astimezone()

        task1, user, action, rule = CommentTask.factory(comment=cmt1, action_datetime=action_datetime)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.status |should| equal_to(CommentTask.STATUS.inprogress)
        task1.actions |should| have(1).items
        task1.progress |should| equal_to(dict(current=1, standard=3))

        task2, user, action, rule = CommentTask.factory(comment=cmt2, action_datetime=action_datetime)
        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.status |should| equal_to(CommentTask.STATUS.inprogress)
        task2.actions |should| have(2).items
        task2.progress |should| equal_to(dict(current=2, standard=3))

        task3, user, action, rule = CommentTask.factory(comment=cmt3, action_datetime=action_datetime)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.status |should| equal_to(CommentTask.STATUS.done)
        task3.actions |should| have(3).items
        task3.progress |should| equal_to(dict(standard=3, current=3))

        task4, user, action, rule = CommentTask.factory(comment=cmt4, action_datetime=action_datetime)
        (task4.process, user, action, task4.rule) |should| throw(TaskAlreadyDone)
        task4.make_done.call_count |should| equal_to(1)

    def test_task_exchange_user_experience(self):
        self.user.profile.experience |should| equal_to(0)

        rule = self.rule = self.get_rule()
        rule.experience |should| equal_to(10)
        rule.comment_count |should| equal_to(3)
        user = self.user
        cmt1 = user.comment_comments.all()[1]
        cmt2 = user.comment_comments.all()[2]
        cmt3 = user.comment_comments.all()[10]

        action_datetime = now().astimezone()
        task1, user, action, rule = commenttask.factory(comment=cmt1, action_datetime=action_datetime)
        rule.id |should| equal_to(self.rule.id)

        task1.process(user=user, action=action, rule=rule)
        task1.status |should| equal_to(commenttask.status.inprogress)
        task1.actions |should| have(1).items
        task1.progress |should| equal_to(dict(standard=3, current=1))

        task2, user, action, rule = commenttask.factory(comment=cmt2, action_datetime=action_datetime)
        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.status |should| equal_to(commenttask.status.inprogress)
        task2.actions |should| have(2).items
        task2.progress |should| equal_to(dict(standard=3, current=2))

        task3, user, action, rule = commenttask.factory(comment=cmt3, action_datetime=action_datetime)
        task3.process(user=user, action=action, rule=rule)
        task3.status |should| equal_to(commenttask.status.done)
        task3.actions |should| have(3).items
        task3.progress |should| equal_to(dict(standard=3, current=3))

        user.profile.experience |should| equal_to(10)
        self.user = user


from activity.documents.actions.signin import *


class SigninTestCase(TaskTestCase):

    action_class = SigninAction

    task_class = SigninTask

    rule_class = SigninTaskRule

    rule = None

    def test_signin_task(self):
        user = User.objects.get(username='killuavx')
        self.user = user
        task = SigninTask()
        self.task = task
        self.rule = self.get_rule()

        action = SigninAction(user=user)
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(SigninTaskRule.STATUS.done)
        task.actions |should| have(1).items

        action = SigninAction(user=user)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)

    def test_factory(self):
        user = User.objects.get(username='killuavx')
        task, user, action, rule = SigninTask.factory(user=user,
                                                      ip_address='127.0.0.1')
        self.user = user
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=rule)
        task.make_done.called |should| be(True)
        list(task.progress.values()) |should| equal_to((1, 1))

        action.ip_address |should| equal_to('127.0.0.1')
        task.ip_address |should| equal_to('127.0.0.1')

        task.status |should| equal_to(SigninTaskRule.STATUS.done)
        task.actions |should| have(1).items

        sec_task, user, sec_action, rule = SigninTask.factory(user=user,
                                                              ip_address='127.0.0.2')

        sec_task.id |should| equal_to(task.id)
        sec_action.ip_address |should| equal_to('127.0.0.2')

        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)
        sec_task.ip_address |should| equal_to('127.0.0.1')

    def test_signin_task_exchange_user_experience(self):
        task, user, action, rule = SigninTask.factory(user=self.user,
                                                      ip_address='127.0.0.1')
        rule.experience |should| equal_to(5)
        self.user.profile.experience |should| equal_to(0)
        task.process(user=user, action=action, rule=rule)
        self.user.profile.experience |should| equal_to(5)


from activity.documents.actions.share import *
from warehouse.models import PackageVersion


class ShareTestCase(TaskTestCase):

    task_class = ShareTask

    action_class = ShareAction

    rule_class = ShareTaskRule

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class(share_count=3)
            rule.save()
        return rule

    def test_factory(self):
        self.rule = self.get_rule()
        self.rule.share_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()
        ShareTask.make_done = Mock(return_value=None)

        version1 = queryset[0]
        task1, user, action, rule = ShareTask.factory(user=user,
                                                      version=version1,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTask.STATUS.inprogress)
        task1.progress |should| equal_to(dict(current=1, standard=3))

        version2 = queryset[1]
        task2, user, action, rule = ShareTask.factory(user=user,
                                                      version=version2,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.actions |should| have(2).items
        task2.status |should| equal_to(ShareTask.STATUS.inprogress)
        task2.progress |should| equal_to(dict(current=2, standard=3))

        version3 = queryset[2]
        task3, user, action, rule = ShareTask.factory(user=user,
                                                      version=version3,
                                                      ip_address=ip_address)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.actions |should| have(3).items
        task3.status |should| equal_to(ShareTask.STATUS.done)
        task3.progress |should| equal_to(dict(standard=3, current=3))


        version4 = queryset[3]
        task4, user, action, rule = ShareTask.factory(user=user,
                                                      version=version4,
                                                      ip_address=ip_address)
        (task4.process, user, action, rule) |should| throw(TaskAlreadyDone)
        task4.actions |should| have(3).items
        task4.progress |should| equal_to(dict(current=3, standard=3))

    def test_factory_duplicate(self):
        self.rule = self.get_rule()
        self.rule.share_count |should| equal_to(3)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()
        ShareTask.make_done = Mock(return_value=None)

        same_version = version = queryset[0]
        task1, user, action, rule = ShareTask.factory(user=user,
                                                      version=version,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTask.STATUS.inprogress)

        task2, user, action, rule = ShareTask.factory(user=user,
                                                      version=same_version,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        (task2.process, user, action, rule) |should| throw(TaskConditionDoesNotMeet)
        task2.actions |should| have(1).items

    def test_task_exchange_user_experience(self):
        self.user.profile.experience |should| equal_to(0)
        user = self.user

        rule = self.rule = self.get_rule()
        rule.experience |should| equal_to(10)
        rule.share_count |should| equal_to(3)
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        version1 = queryset[0]
        task1, user, action, rule = ShareTask.factory(user=user,
                                                      version=version1,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTask.STATUS.inprogress)
        task1.progress |should| equal_to(dict(current=1, standard=3))

        version2 = queryset[1]
        task2, user, action, rule = ShareTask.factory(user=user,
                                                      version=version2,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.actions |should| have(2).items
        task2.status |should| equal_to(ShareTask.STATUS.inprogress)
        task2.progress |should| equal_to(dict(current=2, standard=3))

        version3 = queryset[2]
        task3, user, action, rule = ShareTask.factory(user=user,
                                                      version=version3,
                                                      ip_address=ip_address)
        task3.process(user=user, action=action, rule=rule)
        task3.actions |should| have(3).items
        task3.status |should| equal_to(ShareTask.STATUS.done)
        task3.progress |should| equal_to(dict(standard=3, current=3))

        user.profile.experience |should| equal_to(10)
        self.user = user


from activity.documents.actions.install import *


class InstallTestCase(TaskTestCase):

    task_class = InstallTask

    action_class = InstallAction

    rule_class = InstallTaskRule

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class(install_count=3)
            rule.save()
        return rule

    def test_factory(self):
        self.rule = self.get_rule()
        self.rule.install_count |should| equal_to(3)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()
        InstallTask.make_done = Mock(return_value=None)

        version1 = queryset[0]
        version2 = queryset[1]
        version3 = queryset[2]
        version4 = queryset[3]

        task1, user, action, rule = InstallTask.factory(user=user,
                                                        version=version1,
                                                        ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(InstallTask.STATUS.inprogress)
        task1.progress |should| equal_to(dict(current=1, standard=3))

        task2, user, action, rule = InstallTask.factory(user=user,
                                                        version=version2,
                                                        ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.actions |should| have(2).items
        task2.status |should| equal_to(InstallTask.STATUS.inprogress)
        task2.progress |should| equal_to(dict(current=2, standard=3))

        task3, user, action, rule = InstallTask.factory(user=user,
                                                      version=version3,
                                                      ip_address=ip_address)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.actions |should| have(3).items
        task3.status |should| equal_to(InstallTask.STATUS.done)
        task3.progress |should| equal_to(dict(current=3, standard=3))


        task4, user, action, rule = InstallTask.factory(user=user,
                                                        version=version4,
                                                        ip_address=ip_address)
        (task4.process, user, action, rule) |should| throw(TaskAlreadyDone)
        task4.actions |should| have(3).items
        task4.progress |should| equal_to(dict(current=3, standard=3))

    def test_factory_duplicate(self):
        self.rule = self.get_rule()
        self.rule.install_count |should| equal_to(3)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        same_version = version = queryset[0]
        task1, user, action, rule = InstallTask.factory(user=user,
                                                        version=version,
                                                        ip_address=ip_address)
        task1.make_done = Mock(return_value=None)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(InstallTask.STATUS.inprogress)

        task2, user, action, rule = InstallTask.factory(user=user,
                                                        version=same_version,
                                                        ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        (task2.process, user, action, rule) |should| throw(TaskConditionDoesNotMeet)
        task2.actions |should| have(1).items

    def test_task_exchange_user_credit(self):
        self.user.profile.experience |should| equal_to(0)
        self.user.profile.coin |should| equal_to(0)
        user = self.user

        rule = self.rule = self.get_rule()
        rule.experience |should| equal_to(10)
        rule.install_count |should| equal_to(3)
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        version1 = queryset[0]
        task1, user, action, rule = InstallTask.factory(user=user,
                                                      version=version1,
                                                      ip_address=ip_address)
        task1.process(user=user, action=action, rule=rule)
        task1.actions |should| have(1).items
        task1.status |should| equal_to(ShareTask.STATUS.inprogress)
        task1.progress |should| equal_to(dict(current=1, standard=3))

        version2 = queryset[1]
        task2, user, action, rule = InstallTask.factory(user=user,
                                                      version=version2,
                                                      ip_address=ip_address)

        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.actions |should| have(2).items
        task2.status |should| equal_to(InstallTask.STATUS.inprogress)
        task2.progress |should| equal_to(dict(current=2, standard=3))

        version3 = queryset[2]
        task3, user, action, rule = InstallTask.factory(user=user,
                                                      version=version3,
                                                      ip_address=ip_address)
        task3.process(user=user, action=action, rule=rule)
        task3.actions |should| have(3).items
        task3.status |should| equal_to(InstallTask.STATUS.done)
        task3.progress |should| equal_to(dict(standard=3, current=3))

        user.profile.experience |should| equal_to(10)
        self.user.profile.coin |should| equal_to(30)
        self.user = user


class InstallAwardCoinTestCase(TestCase):

    task_class = InstallTask

    action_class = InstallAction

    rule_class = InstallTaskRule

    def get_rule(self):
        try:
            rule = self.rule_class.objects.get(code=self.rule_class.CODE)
        except:
            rule = self.rule_class(install_count=3)
            rule.save()
        return rule

    def setUp(self):
        self.rule = self.get_rule()
        self.user = User.objects.get(username='killuavx')
        self.user.profile.experience = 0
        self.user.profile.coin = 0
        self.user.profile.level = 0
        self.user.save()

    def tearDown(self):
        self.task_class.objects.delete()
        self.action_class.objects.delete()
        self.rule_class.objects.delete()
        CreditLog.objects.delete()
        if hasattr(self, 'user'):
            self.user.profile.experience = 0
            self.user.profile.coin = 0
            self.user.profile.level = 0
            self.user.save()

    def test_install_award_coin(self):
        self.user.profile.experience |should| equal_to(0)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        # package version with award coin
        same_version = version = queryset[0]
        version.has_award = True
        version.award_coin = 20
        version.save()

        # first install
        action = InstallTask.factory_action(user=user, version=version, ip_address=ip_address)
        action.can_execute() |should| be(True)
        if action.can_execute():
            action.save()
            action.execute()
        user.profile.coin |should| equal_to(20)

        # install duplicate
        action = InstallTask.factory_action(user=user, version=same_version, ip_address=ip_address)
        action.save()
        action.can_execute() |should| be(False)

        user.profile.coin |should| equal_to(20)

    def test_install_award_outof_300max(self):
        self.user.profile.experience |should| equal_to(0)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        # package version with award coin
        version = queryset[0]
        version.has_award = True
        version.award_coin = 200
        version.save()

        # first install coin
        action = InstallTask.factory_action(user=user, version=version, ip_address=ip_address)
        action.can_execute() |should| be(True)
        if action.can_execute():
            action.save()
            action.execute()
        user.profile.coin |should| equal_to(200)

        # second install
        version2 = queryset[3]
        version2.has_award = True
        version2.award_coin = 110
        version2.save()

        action = InstallTask.factory_action(user=user, version=version2, ip_address=ip_address)
        action.can_execute() |should| be(True)
        if action.can_execute():
            action.save()
            action.execute()
        user.profile.coin |should| equal_to(310)


        # install 3
        version3 = queryset[5]
        version3.has_award = True
        version3.award_coin = 20
        version3.save()

        action = InstallTask.factory_action(user=user, version=version3, ip_address=ip_address)
        action.can_execute() |should| be(False)

        user.profile.coin |should| equal_to(310)

    def test_install_award_outof_300max_2(self):
        self.user.profile.experience |should| equal_to(0)
        user = self.user
        ip_address = '127.0.0.1'
        queryset = PackageVersion.objects.published()

        # package version with award coin
        version = queryset[0]
        version.has_award = True
        version.award_coin = 400
        version.save()

        # first install coin
        action = InstallTask.factory_action(user=user, version=version, ip_address=ip_address)
        action.can_execute() |should| be(True)
        if action.can_execute():
            action.save()
            action.execute()
        user.profile.coin |should| equal_to(400)

        # second install
        version2 = queryset[3]
        version2.has_award = True
        version2.award_coin = 110
        version2.save()

        action = InstallTask.factory_action(user=user, version=version2, ip_address=ip_address)
        action.can_execute() |should| be(False)
        user.profile.coin |should| equal_to(400)


from activity.documents.actions.lottery import *
from activity import models
from activity.models import LotteryLuckyDraw
from activity import models as am
from datetime import timedelta
from django.utils.timezone import now


class LotteryTestCase(TestCase):

    task_class = LotteryTask

    rule_class = LotteryRule

    def get_rule(self):
        rule = self.task_class.factory_rule()
        return rule

    def setUp(self):
        self.rule = self.get_rule()
        self.user = User.objects.get(username='killuavx')
        self.user.profile.experience = 0
        self.user.profile.coin = 0
        self.user.profile.level = 0
        self.user.save()

    def _prepare_lottery(self, **kwargs):
        n = now().astimezone()
        e = n + timedelta(days=10)
        lottery = models.Lottery(title=kwargs.get('title', '抽奖'),
                                 description="",
                                 publish_date=n,
                                 expiry_date=e)
        lottery.save()

        # prize 1
        prize = models.LotteryPrize(
            group=models.LOTTERY_PRIZE_GROUP.real,
            level=models.LOTTERY_PRIZE_LEVEL.top,
            title='小米手机4',
            total_count=1,
            award_coin=0,
            win_prompt='你经常扶老奶奶过马路的事情已经被我们知道了，这是奖励。',
            rate=1,
        )
        lottery.prizes.add(prize)

        # prize 2
        prize = models.LotteryPrize(
            group=models.LOTTERY_PRIZE_GROUP.real,
            level=models.LOTTERY_PRIZE_LEVEL.lucky,
            title='小米平板',
            total_count=2,
            award_coin=0,
            win_prompt='你是在山东蓝翔技校学习的抽奖技术吗？',
            rate=2,
        )
        lottery.prizes.add(prize)

        # prize 3
        prize = models.LotteryPrize(
            group=models.LOTTERY_PRIZE_GROUP.real,
            level=models.LOTTERY_PRIZE_LEVEL.well,
            title='小米电源',
            total_count=3,
            award_coin=0,
            win_prompt='传说中的神抽手就是你吗？',
            rate=3,
            )
        lottery.prizes.add(prize)

        # prize 4
        prize = models.LotteryPrize(
            group=models.LOTTERY_PRIZE_GROUP.virtual,
            level=models.LOTTERY_PRIZE_LEVEL.good,
            title='100金币',
            total_count=0,
            award_coin=100,
            win_prompt='传说中的神抽手就是你吗？',
            rate=300,
        )
        lottery.prizes.add(prize)

        # prize 5
        prize = models.LotteryPrize(
            group=models.LOTTERY_PRIZE_GROUP.virtual,
            level=models.LOTTERY_PRIZE_LEVEL.again,
            title='再来一次',
            total_count=0,
            award_coin=50,
            win_prompt='传说中的神抽手就是你吗？',
            rate=600,
        )
        lottery.prizes.add(prize)

        return lottery

    def test_play(self):
        lottery = self._prepare_lottery(title='万圣节抽奖')
        lottery.title |should| equal_to('万圣节抽奖')
        task = LotteryTask.factory_task(lottery=lottery)
        task.cost_coin |should| equal_to(100)
        task.title |should| equal_to('万圣节抽奖')

        p1 = task.prizes[0]
        p1.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p1.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.top)

        p2 = task.prizes[1]
        p2.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p2.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.lucky)

        p3 = task.prizes[2]
        p3.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p3.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.well)

        p4 = task.prizes[3]
        p4.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.virtual)
        p4.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.good)

        p5 = task.prizes[4]
        p5.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.virtual)
        p5.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.again)

        expect_task = LotteryTask.factory_task()
        expect_task.id |should| equal_to(task.id)

    def test_play_with_orm(self):
        lottery = self._prepare_lottery(title='万圣节抽奖')
        lottery.title |should| equal_to('万圣节抽奖')
        task = LotteryTask.factory_task(lottery=lottery)
        task.cost_coin |should| equal_to(100)
        task.title |should| equal_to('万圣节抽奖')

        prizes = lottery.prizes.all()
        p1 = prizes[0]
        p1.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p1.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.top)

        p2 = prizes[1]
        p2.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p2.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.lucky)

        p3 = prizes[2]
        p3.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.real)
        p3.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.well)

        p4 = prizes[3]
        p4.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.virtual)
        p4.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.good)

        p5 = prizes[4]
        p5.group |should| equal_to(models.LOTTERY_PRIZE_GROUP.virtual)
        p5.level |should| equal_to(models.LOTTERY_PRIZE_LEVEL.again)

        luckydraw = LotteryLuckyDraw(lottery)
        rt = luckydraw.draw(user=self.user)
        rt |should_not| be(None)

        prize, winning = rt
        if prize.group == models.LOTTERY_PRIZE_GROUP.real:
            winning |should_not| be(None)
            winning.user |should| equal_to(self.user)
            prize.win_count |should| equal_to(1)
            if prize.total_count == prize.win_count:
                prize.status |should| equal_to(LotteryPrize.STATUS.notover)
        else:
            winning |should| be(None)
            prize.award_coin |should| be_greater_than_or_equal_to(50)

    def test_prize_status(self):
        # 测试内定奖项后，prize状态变化
        lottery = self._prepare_lottery(title='万圣节抽奖')

        prize1 = lottery.prizes.get(level=am.LotteryPrize.LEVEL.top)
        prize1.status |should| equal_to(am.LotteryPrize.STATUS.notover)
        prize1.total_count |should| equal_to(1)
        prize1.win_count |should| equal_to(0)

        win_date = now().astimezone()
        winning = am.LotteryWinning.objects.create(prize=prize1,
                                                   lottery=lottery,
                                                   user=self.user,
                                                   status=am.LotteryWinning.STATUS.unofficial,
                                                   win_date=win_date)
        expect_prize = am.LotteryPrize.objects.get(pk=winning.prize_id)
        expect_prize.win_count |should| equal_to(0)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.over)

        #删除内定名单，over -> notover
        winning.delete()
        expect_prize = am.LotteryPrize.objects.get(pk=winning.prize_id)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)


        #新增内定名的, notover -> over
        winning.save()
        expect_prize = am.LotteryPrize.objects.get(pk=winning.prize_id)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.over)

        # 新增发奖数据, over -> notover
        expect_prize.total_count += 1
        expect_prize.save()
        expect_prize = am.LotteryPrize.objects.get(pk=winning.prize_id)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)

        # notover -> over -> finish
        winning2 = am.LotteryWinning.objects.create(prize=expect_prize,
                                                    lottery=lottery,
                                                    user=self.user,
                                                    status=am.LotteryWinning.STATUS.win,
                                                    win_date=win_date)
        expect_prize = am.LotteryPrize.objects.get(pk=winning2.prize_id)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.over)

        # hack
        winning = am.LotteryWinning.objects.get(pk=winning.pk)
        winning.status = am.LotteryWinning.STATUS.win
        winning.save()
        expect_prize = am.LotteryPrize.objects.get(pk=winning2.prize_id)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.finish)

        #luckydraw = LotteryLuckyDraw(lottery=lottery)

    def test_prize_status_2(self):
        # 测试内定奖项后，prize状态变化
        lottery = self._prepare_lottery(title='万圣节抽奖')

        prize1 = lottery.prizes.get(level=am.LotteryPrize.LEVEL.lucky)
        prize1.status |should| equal_to(am.LotteryPrize.STATUS.notover)
        prize1.total_count |should| equal_to(2)
        prize1.win_count |should| equal_to(0)

        win_date = now().astimezone()
        winning1 = am.LotteryWinning.objects.create(prize=prize1,
                                                    lottery=lottery,
                                                    user=self.user,
                                                    status=am.LotteryWinning.STATUS.unofficial,
                                                    win_date=win_date)
        expect_prize = am.LotteryPrize.objects.get(pk=winning1.prize_id)
        expect_prize.win_count |should| equal_to(0)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)

        winning2 = am.LotteryWinning.objects.create(prize=expect_prize,
                                                    lottery=lottery,
                                                    user=self.user,
                                                    status=am.LotteryWinning.STATUS.unofficial,
                                                    win_date=win_date)
        expect_prize = am.LotteryPrize.objects.get(pk=winning2.prize_id)
        expect_prize.win_count |should| equal_to(0)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.over)

        for w in expect_prize.winnings.all():
            w.status = am.LotteryWinning.STATUS.win
            w.save()

        expect_prize = am.LotteryPrize.objects.get(pk=winning2.prize_id)
        expect_prize.win_count |should| equal_to(2)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.finish)


        w = expect_prize.winnings.all()[0]
        w.delete()
        expect_prize = am.LotteryPrize.objects.get(pk=winning2.prize_id)
        expect_prize.win_count |should| equal_to(1)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)

        w = expect_prize.winnings.all()[0]
        w.status = am.LotteryWinning.STATUS.unofficial
        w.save()
        expect_prize.win_count |should| equal_to(0)
        expect_prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)

    def test_prize_draw_manually(self):
        lottery = self._prepare_lottery(title='万圣节抽奖')


        prize = lottery.prizes.get(level=am.LotteryPrize.LEVEL.top)
        luckydraw = LotteryLuckyDraw(lottery=lottery)


        prize.total_count |should| equal_to(1)
        prize.win_count |should| equal_to(0)
        prize.status |should| equal_to(am.LotteryPrize.STATUS.notover)

        lottery.cost_coin |should| equal_to(100)
        self.user.profile.coin = 1000
        self.user.profile.save()
        res = luckydraw.draw_manually(user=self.user, prize=prize)
        res |should_not| be(None)

        self.user.profile.coin |should| equal_to(900)


        expect_prize, expect_winning = res
        (prize.pk, prize.group, prize.level) |should| equal_to((expect_prize.pk, prize.group, expect_prize.level))

        expect_winning.user.pk |should| equal_to(self.user.pk)
        expect_winning.prize_id |should| equal_to(prize.pk)


    def tearDown(self):
        if hasattr(self, 'lottery'):
            self.lottery.delete()

        self.task_class.objects.delete()
        LotteryPlayAction.objects.delete()
        LotteryWinningAction.objects.delete()
        self.rule_class.objects.delete()
        CreditLog.objects.delete()
        if hasattr(self, 'user'):
            self.user.profile.experience = 0
            self.user.profile.coin = 0
            self.user.profile.level = 0
            self.user.save()

