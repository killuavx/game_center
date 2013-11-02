# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from fts import helpers
from should_dsl import should

class AdminBaseDSL(object):

    login_page = '/admin'

    @classmethod
    def create_staff_user(cls, context, username, password):
        user = User.objects.create_user(username=username, password=password)
        user.check_password(password) |should| be(True)
        user.is_staff = True
        user.save()
        helpers.add_model_objects(user)
        return user

    @classmethod
    def login(cls, context, username, password):
        b = context.browser
        context.execute_steps("""
            When I visit "%(url)s"
             And I fill in "username" with "%(username)s"
             And I fill in "password" with "%(password)s"
             And I press the element with xpath "%(submit_xpath)s"
        """)

    @classmethod
    def login_successful_above(cls, context):
        return context.world.get('is_logined')


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
        context.world.update(dict(is_logined=flag))

def factory_dsl(context):
    if 'browser' in context.tags:
        return AdminUsingBrowserDSL
    else:
        return AdminUsingNoUIClientDSL