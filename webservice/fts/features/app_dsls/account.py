# -*- coding: utf-8 -*-
from account.models import User as Player
from account.models import *
from fts.helpers import add_model_objects
from rest_framework import status
from contextlib import contextmanager


class AccountBaseDSL(object):
    from account.forms.mob import SignupForm

    clear_usernames = []

    _signin_url = '/api/accounts/signin/'

    _signup_url = '/api/accounts/signup/'

    _signout_url = '/api/accounts/signout/'

    _profile_url = '/api/accounts/myprofile/'

    _PASSWORD = '123456'

    @classmethod
    def setup(cls, context):
        cls.clear_usernames = []

    @classmethod
    def already_exists_player_create(cls, context, username):
        form = cls.SignupForm(data=dict(username=username,
                                        password=cls._PASSWORD))
        form.is_valid()
        user = form.save()
        cls.clear_usernames.append(user.username)

    @classmethod
    def signup(cls, context, **user_data):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'signup')
        )

    @classmethod
    @contextmanager
    def signin(cls, context, **kwargs):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'signin')
        )

    @classmethod
    def set_authorizate_token(cls, context, token_key):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'set_authorizate_token')
        )

    @classmethod
    def signout(cls, context):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'signout')
        )

    @classmethod
    def visit_profile(cls, context):
        raise NotImplementedError(
            'you must implement %s.%s' %(cls, 'visit_profile')
        )

    # bookmark
    @classmethod
    def visit_bookmarks(cls):
        raise NotImplementedError(
            '%s.%s implement' %(cls, 'visit_bookmark')
        )

    @classmethod
    def add_bookmark(cls, context, package):
        raise NotImplementedError(
            '%s.%s implement' %(cls, 'add_bookmark')
        )

    @classmethod
    def remove_bookmark(cls, context, package):
        raise NotImplementedError(
            '%s.%s not implement' %(cls, 'remove_bookmark')
        )

    @classmethod
    def teardown(cls, context):
        try:
            clear_usernames = list(map(lambda e: e.lower(), cls.clear_usernames))
            cls.clear_usernames = []
            if clear_usernames and any(clear_usernames):
                Player.objects.filter(username__in=clear_usernames).delete()
        except Player.DoesNotExist as e:
            pass


class AccountRestApiUsingNoUIClientDSL(AccountBaseDSL):

    @classmethod
    def signup(cls, context, **user_data):
        api_url = "%s%s" %(context.base_url, cls._signup_url)
        context.client.post(api_url, user_data)
        cls.clear_usernames.append(user_data.get('username'))

    @classmethod
    @contextmanager
    def signin(cls, context, **user_data):
        cls.remove_authorizate_token(context)
        api_url = "%s%s" %(context.base_url, cls._signin_url)
        context.client.post(api_url, user_data)
        user_data.update(token=None)
        yield user_data
        cls.set_authorizate_token(context, user_data.get('token'))
        context.world.update(the_user=user_data)

    @classmethod
    def set_authorizate_token(cls, context, token_key):
        context.client.defaults.update(dict(
            HTTP_AUTHORIZATION='Token %s' % token_key
        ))

    @classmethod
    def remove_authorizate_token(cls, context):
        try:
            del context.client.defaults['HTTP_AUTHORIZATION']
        except KeyError:
            pass

    @classmethod
    def signout(cls, context):
        api_url = "%s%s" %(context.base_url, cls._signout_url)
        context.client.get(api_url)

    @classmethod
    def visit_myprofile(cls, context):
        api_url = "%s%s" %(context.base_url, cls._profile_url)
        context.client.get(api_url)

    _bookmark_url = '/api/bookmarks/'

    @classmethod
    def visit_bookmarks(cls, context):
        api_url = "%s%s" % (context.base_url, cls._bookmark_url)
        context.client.get(api_url)

    @classmethod
    def add_bookmark(cls, context, package):
        api_url = "%s%s" %(context.base_url, cls._bookmark_url)
        context.client.post(api_url, dict(package_name=package.package_name))

    @classmethod
    def remove_bookmark(cls, context, package):
        api_url = "%s%s%d/" %(context.base_url, cls._bookmark_url, package.pk)
        context.client.delete(api_url)


class AccountWebAppUsingBrowserDSL(AccountBaseDSL):

    @classmethod
    def signup(cls, context, **user_data):
        api_url = "%s%s" %(context.base_url, cls._signup_url)
        # FIXME
        context.browser.visit(api_url, user_data)
        cls.clear_usernames.append(user_data.get('username'))

    @contextmanager
    @classmethod
    def signin(cls, context, **user_data):
        api_url = "%s%s" %(context.base_url, cls._signin_url)
        context.client.post(api_url, user_data)
        yield user_data
        cls.set_authorizate_token(context, user_data.get('token'))

    @classmethod
    def set_authorizate_token(cls, context, token_key):
        pass

    @classmethod
    def signout(cls, context):
        api_url = "%s%s" %(context.base_url, cls._signup_url)
        context.client.get(api_url)


def factory_dsl(context):
    return AccountRestApiUsingNoUIClientDSL


def setup(context):
    factory_dsl(context).setup(context)


def teardown(context):
    factory_dsl(context).teardown(context)
