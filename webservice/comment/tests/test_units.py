# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from comment.models import Comment
from django.contrib.sites.models import Site
from django.utils.timezone import datetime, now
from django.test.testcases import override_settings
from django.conf import settings

from fts.helpers import ApiDSL
from should_dsl import should

class CommentUnitTest(TestCase):

    @override_settings(COMMENTS_POST_PUBLISHED=False)
    def test_post_comment_to_packageversion(self):
        player = ApiDSL.Given_i_have_account(self)
        package = ApiDSL.Given_i_have_published_package(self, title='愤怒的小鸟')
        version = package.versions.get()
        cmt = Comment(site=Site.objects.get_current())
        cmt.submit_date = now()
        cmt.content_object = version
        cmt.comment = '好玩!'
        cmt.user = player

        cmt.save()
        Comment.objects.for_model(version).count() |should| equal_to(1)
        Comment.objects.for_model(version)\
            .published().count() |should| equal_to(0)

        cmt.is_public = True
        cmt.save |should| change(
            Comment.objects.for_model(version).published().count
        ).from_(0).to(1)

        except_cmt = Comment.objects.get(pk=cmt.pk)
        except_cmt.content_object |should| equal_to(version)
