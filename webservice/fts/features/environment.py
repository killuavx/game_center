# -*- coding: utf-8 -*-
__author__ = 'me'
import os
from behaving import environment as benv
from behaving.personas import environment as personaenv
from behaving.web import environment as webenv
from fts.tests import helpers
from fts.middlewares import get_current_request
from fts.features import support
from django.test.client import Client

PERSONAS = {}


def setup(context):
    import fts

    _dir = os.path.dirname(fts.__file__)
    context.fixture_dir = os.path.join(_dir, 'tests/fixtures')
    context.attachment_dir = context.fixture_dir
    context.get_current_request = get_current_request

    if not hasattr(context, 'world'):
        context.world = {}


def setup_client(context):
    context.base_url = 'http://localhost:8080'
    if 'browser' not in context.tags:
        client_initial_params = dict(HTTP_ACCEPT='application/json',
                                     HTTP_CACHE_CONTROL='no-cache')
        context.client_initial_params = client_initial_params
        context.client = Client(client_initial_params)


def teardown_client(context):
    if hasattr(context, 'client'):
        context.client = None


def teardown(context):
    context.world = {}
    helpers.clear_data()

    if hasattr(context, 'browser'):
        try:
            context.browser.quit()
        except:pass


def before_all(context):
    setup(context)
    personaenv.before_all(context)
    webenv.before_all(context)


def after_all(context):
    personaenv.after_all(context)
    webenv.after_all(context)
    teardown(context)


def before_feature(context, feature):
    personaenv.before_feature(context, feature)
    webenv.before_feature(context, feature)
    context.config.log_capture = False


def after_feature(context, feature):
    webenv.after_feature(context, feature)
    personaenv.after_feature(context, feature)
    teardown(context)


def before_scenario(context, scenario):
    setup(context)
    personaenv.before_scenario(context, scenario)
    webenv.before_scenario(context, scenario)
    setup_client(context)


def after_scenario(context, scenario):
    personaenv.after_scenario(context, scenario)
    webenv.after_scenario(context, scenario)
    teardown_client(context)
    teardown(context)


"""
import threading
from wsgiref import simple_server
from selenium import webdriver

def before_all(context):
    context.server = simple_server.WSGIServer(('', 8000))
    from webservice.wsgi import application as webapp
    context.server.set_app(webapp(dict(environment='test')))
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()
    context.browser = webdriver.Chrome()

def after_all(context):
    context.server.shutdown()
    context.thread.join()
    context.browser.quit()

def before_feature(context, feature):
    model.init(environment='test')
"""
