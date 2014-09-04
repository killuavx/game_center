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

    @classmethod
    def setUpClass(cls):
        try:
            cls.rule = CommentTaskRule.objects.get(code=CommentTaskRule.CODE)
        except:
            cls.rule = CommentTaskRule(name='post comment', comment_count=3)
            cls.rule.save()

    @classmethod
    def tearDownClass(cls):
        CommentTask.objects.delete()
        CommentTaskRule.objects.delete()
        CommentAction.objects.delete()
        pass

    def tearDown(self):
        if hasattr(self, 'task'):
            self.task.delete()
        pass

    def test_add_duplicate_action(self):
        user = User.objects.get(username='killuavx')
        task = CommentTask()
        self.task = task
        task.make_done = Mock(return_value=None)
        self.rule.comment_count |should| equal_to(3)

        same_cmt = user.comment_comments.all()[1]
        action = CommentAction(content=same_cmt)
        task.process(user=user, action=action, rule=self.rule)

        task.status |should| equal_to(CommentTask.STATUS.inprogress)
        task.actions |should| have(1).items

        action = CommentAction(content=same_cmt)
        (task.process, user, action, task.rule) |should| throw(TaskConditionDoesNotMeet)
        task.actions |should| have(1).items


    def test_finish_comment_task(self):
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


from activity.documents.actions.signin import *


class SigninTestCase(TestCase):

    rule = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.rule = SigninTaskRule.objects.get(code=SigninTaskRule.CODE)
        except:
            cls.rule = SigninTaskRule()
            cls.rule.save()

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

        action = SigninAction(user=user)
        task.make_done = Mock(return_value=None)
        task.process(user=user, action=action, rule=self.rule)
        task.make_done.called |should| be(True)

        task.status |should| equal_to(CommentTask.STATUS.done)
        task.actions |should| have(1).items

        action = SigninAction(user=user)
        (task.process, user, action, task.rule) |should| throw(TaskAlreadyDone)
        task.make_done.call_count |should| equal_to(1)
        assert False
