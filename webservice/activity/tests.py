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


class CommentTestCase(TestCase):

    rule = None

    def tearDown(self):
        CommentTask.objects.delete()
        CommentTaskRule.objects.delete()
        CommentAction.objects.delete()

    def get_rule(self):
        try:
            return CommentTaskRule.objects.get(code=CommentTaskRule.CODE)
        except:
            rule = CommentTaskRule(name='post comment', comment_count=3)
            rule.save()
            return rule

    def test_add_duplicate_action(self):
        self.rule = self.get_rule().comment_count |should| equal_to(3)

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
        self.rule = self.get_rule().comment_count |should| equal_to(3)

        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task
        task.make_done = Mock(return_value=None)
        self.rule.comment_count |should| equal_to(3)

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

        cmt3 = user.comment_comments.all()[3]
        action = CommentAction(content=cmt3)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(CommentTask.STATUS.done)
        task.actions |should| have(3).items


        cmt3 = user.comment_comments.all()[4]
        action = CommentAction(content=cmt3)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)

    def test_factory(self):
        self.rule = self.get_rule().comment_count |should| equal_to(3)
        user = User.objects.get(username='killuavx')
        cmt1 = user.comment_comments.all()[1]
        cmt2 = user.comment_comments.all()[2]
        cmt3 = user.comment_comments.all()[3]
        cmt4 = user.comment_comments.all()[4]
        CommentTask.make_done = Mock(return_value=None)

        action_datetime = now().astimezone()

        task1, user, action, rule = CommentTask.factory(comment=cmt1, action_datetime=action_datetime)
        task1.process(user=user, action=action, rule=rule)
        task1.make_done.called |should| be(False)
        task1.status |should| equal_to(CommentTask.STATUS.inprogress)
        task1.actions |should| have(1).items

        task2, user, action, rule = CommentTask.factory(comment=cmt2, action_datetime=action_datetime)
        task2.id |should| equal_to(task1.id)

        task2.process(user=user, action=action, rule=rule)
        task2.make_done.called |should| be(False)
        task2.status |should| equal_to(CommentTask.STATUS.inprogress)
        task2.actions |should| have(2).items

        task3, user, action, rule = CommentTask.factory(comment=cmt3, action_datetime=action_datetime)
        task3.process(user=user, action=action, rule=rule)
        task3.make_done.called |should| be(True)
        task3.status |should| equal_to(CommentTask.STATUS.done)
        task3.actions |should| have(3).items

        cmt4 = user.comment_comments.all()[4]
        task4, user, action, rule = CommentTask.factory(comment=cmt4, action_datetime=action_datetime)
        (task4.process, user, action, task4.rule) |should| throw(TaskAlreadyDone)
        task4.make_done.call_count |should| equal_to(1)


from activity.documents.actions.signin import *


class SigninTestCase(TestCase):

    rule = None

    def get_rule(self):
        try:
            rule = SigninTaskRule.objects.get(code=SigninTaskRule.CODE)
        except:
            rule = SigninTaskRule()
            rule.save()
        return rule

    @classmethod
    def tearDownClass(cls):
        SigninTaskRule.objects.delete()
        SigninAction.objects.delete()
        SigninTask.objects.delete()

    def tearDown(self):
        if hasattr(self, 'task'):
            self.task.delete()

    def test_signin_task(self):
        user = User.objects.get(username='killuavx')
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
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=rule)
        task.make_done.called |should| be(True)

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

