# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from fts import helpers
from should_dsl import should


class AdminBaseDSL(object):

    login_page = '/admin'

    @classmethod
    def create_staff_user(cls, context, username, password):
        User = get_user_model()
        user = User.objects.create_superuser(
            username=username,
            email=None,
            password=password)
        helpers.add_model_objects(user)
        return user

    @classmethod
    def login(cls, context, username, password):
        raise NotImplementedError()

    @classmethod
    def login_successful_above(cls, context):
        return context.world.get('is_logined')

    @classmethod
    def login_as_supperuser_already_exists(cls, context, username):
        password = 'default_pass'
        cls.create_staff_user(context, username, password)
        cls.login(context, username, password)


class AdminUsingBrowserDSL(AdminBaseDSL):

    @classmethod
    def login(cls, context, username, password):
        context.execute_steps("""
            When I visit "%(url)s"
             And I fill in "username" with "%(username)s"
             And I fill in "password" with "%(password)s"
             And I press the element with xpath "%(submit_xpath)s"
        """ % dict(
            url=cls.login_page,
            username=username,
            password=password,
            submit_xpath='//input[@type="submit"]'
        ))
        content_text = context.browser.html
        flag = '欢迎，' in content_text \
                    and username in content_text \
                    and '注销' in content_text
        context.world.update(dict(is_logined=flag))


class AdminUsingNoUIClientDSL(AdminBaseDSL):

    @classmethod
    def login(cls, context, username, password):
        flag = context.client.login(username=username, password=password)
        context.world.update(is_logined=flag)


def factory_dsl(context):
    if 'browser' in context.tags:
        return AdminUsingBrowserDSL
    else:
        return AdminUsingNoUIClientDSL