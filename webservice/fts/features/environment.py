# -*- coding: utf-8 -*-

import os
from behaving.personas import environment as personaenv
from behaving.web import environment as webenv
from fts import helpers
from fts.features import support
from toolkit.middleware import get_current_request, get_current_response
from toolkit.helpers import import_from
import time

PERSONAS = {}


def setup(context):
    import fts

    _dir = os.path.dirname(fts.__file__)
    context.fixture_dir = os.path.join(_dir, 'tests/fixtures')
    context.attachment_dir = context.fixture_dir
    context.get_current_request = get_current_request
    context.get_current_response = get_current_response

    if not hasattr(context, 'world'):
        context.world = {}


def setup_client(context):
    context.base_url = 'http://localhost:8080'
    factory_web_dsl = import_from('fts.features.app_dsls.web.factory_dsl')
    WebDSL = factory_web_dsl(context)
    WebDSL.browser_or_client(context)


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
    if context.failed:
        time.sleep(60)
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
