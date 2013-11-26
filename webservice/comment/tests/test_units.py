# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from comment.models import Comment
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.test.testcases import override_settings
from should_dsl import should
from fts.features.app_dsls import warehouse, account


class CommentBaseUnitTest(TestCase):
    tags = []

    world = {}

    def setUp(self):
        super(CommentBaseUnitTest, self).setUp()
        self.WarehouseDSL = warehouse.factory_dsl(self)
        self.WarehouseDSL.setup(self)
        self.AccountDSL = account.factory_dsl(self)
        self.AccountDSL.setup(self)

    def tearDown(self):
        self.WarehouseDSL.teardown(self)
        self.AccountDSL.teardown(self)
        super(CommentBaseUnitTest, self).tearDown()

    def create_package(self, with_version=False, **kwargs):
        return self.WarehouseDSL.create_package_without_ui(
            self,
            with_version=with_version,
            **kwargs)

    def create_account(self, username):
        return self.AccountDSL \
            .already_exists_player_create(context=self,
                                          username=username)


class CommentUnitTest(CommentBaseUnitTest):

    def test_post_comment_to_packageversion(self):
        player = self.create_account(username='kentback')
        package = self.create_package(with_version=True,
                                      title='愤怒的小鸟')
        version = package.versions.get()


        cmt = Comment(site=Site.objects.get_current())
        cmt.submit_date = now()
        cmt.content_object = version
        cmt.comment = '好玩!'
        cmt.user = player

        @override_settings(COMMENTS_POST_PUBLISHED=False)
        def comment_save_wrapper_for_orveride_settings():
            cmt.save()
        comment_save_wrapper_for_orveride_settings()

        Comment.objects.for_model(version).count() | should | equal_to(1)

        cmt.is_public |should| be(False)

        Comment.objects.for_model(version) \
            .published().count() | should | equal_to(0)

        cmt.is_public = True
        cmt.save | should | change(
            Comment.objects.for_model(version).published().count
        ).from_(0).to(1)

        except_cmt = Comment.objects.get(pk=cmt.pk)
        except_cmt.content_object | should | equal_to(version)
