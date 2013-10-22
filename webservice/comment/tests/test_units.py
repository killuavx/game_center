# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.conf import settings

from fts.tests.helpers import ApiDSL
from should_dsl import should

class CommentUnitTest(TestCase):

    def test_post_comment_to_packageversion(self):
        player = ApiDSL.Given_i_have_account(self)
        package = ApiDSL.Given_i_have_published_package(self, title='愤怒的小鸟')
        version = package.versions.get()
        cmt = Comment(site=Site.objects.get_current())
        cmt.content_object = version
        cmt.comment = '好玩!'
        cmt.user = player

        cmt.save |should| change(
            Comment.objects.for_model(version).count
        ).from_(0).to(1)

        except_cmt = Comment.objects.get(pk=cmt.pk)
        except_cmt.content_object |should| equal_to(version)
