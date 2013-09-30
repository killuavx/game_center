# -*- coding: utf-8 -*-
__author__ = 'me'
from fts.tests.helpers import ApiDSL, RestApiTest
from rest_framework import status

class AccountRestApiTest(RestApiTest):

    def test_basic_visit(self):

        user_data = dict(
            username='testuser',
            password='testuser123',
            phone='+86-021-44354322',
            email='testuser@testcase.com',
        )
        # sign up
        ApiDSL.When_i_signup_with(self, user_data)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_201_CREATED)

        # sign in
        ApiDSL.When_i_signin_with(self, user_data)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_receive_auth_token(self)

        # visit my profile
        ApiDSL.When_i_prepare_auth_token(self, self.world.get('content').get('token'))
        ApiDSL.When_i_access_myprofile(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_myprofile_information(self, user_data)

        # sign out
        ApiDSL.When_i_signout(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.When_i_access_myprofile(self)
        ApiDSL.Then_i_should_receive_response_with(self, status_code=status.HTTP_401_UNAUTHORIZED)

