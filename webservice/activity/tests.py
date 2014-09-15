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


from should_dsl import should
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
        self.user.profile.coin |should| equal_to(10)
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
