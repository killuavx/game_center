# -*- encoding: utf-8-*-
from fts.tests import  helpers
from django.utils.timezone import now, timedelta
from rest_framework import status
from fts.tests.helpers import ApiDSL, RestApiTest
from searcher.models import TipsWord

class SearchRestApiTest(RestApiTest):
    """ 搜索接口测试 """

    def test_search_list(self):
        """ TODO 搜索软件列表测试 """
        #ApiDSL.When_i_access_api_root(self)
        #ApiDSL.Then_i_should_see_the_api_in_content(self, name='search')

class SearchPackageRestApiTest(RestApiTest):
    """ 搜索软件列表接口 """

    def test_empty_query_not_allow(self):
        yestoday = now() - timedelta(days=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self,
                                                     title='愤怒的小鸟',
                                                     all_datetime=yestoday)
        keyword = ' '
        ApiDSL.When_i_access_search_package(self, keyword)
        ApiDSL.Then_i_should_receive_response_with(self, status.HTTP_403_FORBIDDEN)

    def test_simple_list(self):
        yestoday = now() - timedelta(days=1)
        pkg1 = ApiDSL.Given_i_have_published_package(self,
                                                     title='愤怒的小鸟',
                                                     all_datetime=yestoday)
        pkg2 = ApiDSL.Given_i_have_published_package(self,
                                                     title='愤怒的小鸟2',
                                                     all_datetime=yestoday)
        keyword = '小鸟'
        ApiDSL.When_i_access_search_package(self, keyword)
        ApiDSL.Then_i_should_receive_success_response(self)
        content = self.world.get('content')
        ApiDSL.Then_i_should_see_result_list(self, num=2, count=2)
        ApiDSL\
            .Then_i_should_see_package_summary_list(self, pkg_list_data=content)


class SearchWordTipsRestApiTest(RestApiTest):

    def test_tips_list(self):
        yestoday = now() - timedelta(days=1)
        ApiDSL.Given_i_have_tipsword_with(self, keyword='愤怒的小鸟',
                                          status=TipsWord.STATUS.published,
                                          released_datetime=yestoday)
        ApiDSL.When_i_access_search_tips(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_result_list(self, num=1, count=1)
        content = self.world.get('content')
        ApiDSL \
            .Then_i_should_see_tips_list(self, tips_list=content.get('results'))
        pass
