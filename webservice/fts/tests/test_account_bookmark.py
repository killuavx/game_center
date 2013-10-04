# -*- coding: utf-8 -*-
__author__ = 'me'
from fts.tests.helpers import RestApiTest, ApiDSL
from rest_framework import status

class AccountBookmarkRestApiTest(RestApiTest):

    def test_add_bookmark(self):
        player = ApiDSL.Given_i_have_account(self)
        ApiDSL.Given_i_have_signup(self, player)
        ApiDSL.When_i_access_mybookmarks(self)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_404_NOT_FOUND)

        pkg1 = ApiDSL.Given_i_have_published_package(self, title='愤怒的小鸟')
        pkg2 = ApiDSL.Given_i_have_published_package(self, title='植物大战僵尸')
        ApiDSL.When_i_add_bookmark(self, pkg1)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        ApiDSL.When_i_access_mybookmarks(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, count=1, num=1)

        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_package_summary_list(self, results)

    def test_remove_bookmark(self):
        player = ApiDSL.Given_i_have_account(self)
        ApiDSL.Given_i_have_signup(self, player)

        pkg1 = ApiDSL.Given_i_have_published_package(self, title='愤怒的小鸟')
        pkg2 = ApiDSL.Given_i_have_published_package(self, title='植物大战僵尸')
        ApiDSL.When_i_add_bookmark(self, pkg1)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        ApiDSL.When_i_add_bookmark(self, pkg2)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        ApiDSL.When_i_access_mybookmarks(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, count=2, num=2)

        results = self.world.get('content').get('results')
        ApiDSL.Then_i_should_see_package_summary_list(self, results)

        # check package bookmark status
        except_pkg = results[0]
        actions =except_pkg.get('actions')
        ApiDSL.When_i_access_url_with_head_method(self, actions.get('mark'))
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_200_OK)


        ApiDSL.When_i_remove_bookmark(self, pkg1)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_204_NO_CONTENT)

        ApiDSL.When_i_access_mybookmarks(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, count=1, num=1)

        expect_pkg = self.world.get('content').get('results')[0]
        self.assertEqual(expect_pkg.get('title'), pkg2.title)

    def test_has_bookmark(self):
        player = ApiDSL.Given_i_have_account(self)
        ApiDSL.Given_i_have_signup(self, player)

        pkg1 = ApiDSL.Given_i_have_published_package(self, title='愤怒的小鸟')
        pkg2 = ApiDSL.Given_i_have_published_package(self, title='植物大战僵尸')
        ApiDSL.When_i_add_bookmark(self, pkg1)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        ApiDSL.When_i_add_bookmark(self, pkg2)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        ApiDSL.When_i_access_bookmark_check(self, pkg1)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_200_OK)

        pkg3 = ApiDSL.Given_i_have_published_package(self, title='水果忍者')
        ApiDSL.When_i_access_bookmark_check_with(self, package_name=pkg3.package_name)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_404_NOT_FOUND)

        ApiDSL.When_i_access_bookmark_check(self, pkg3)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_404_NOT_FOUND)
