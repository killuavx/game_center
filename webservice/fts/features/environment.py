# -*- coding: utf-8 -*-
__author__ = 'me'
import os
from behaving import environment as benv
from behaving.personas import environment as personaenv
from fts.tests.helpers import ApiDSL
from fts.tests import helpers
from fts.middlewares import get_current_request
from django.conf import settings
import logging

PERSONAS = {}
def before_all(context):
    import fts
    _dir = os.path.dirname(fts.__file__)
    context.fixture_dir = os.path.join(_dir, 'tests/fixtures')
    context.attachment_dir = context.fixture_dir
    context.get_current_request = get_current_request

    ApiDSL.setUp(context)
    personaenv.before_all(context)

    context.config.log_capture = False
    if not context.config.log_capture:
        logging.basicConfig(level=settings.DEBUG)

def after_all(context):
    personaenv.after_all(context)
    helpers.clear_data()

def before_feature(context, feature):
    ApiDSL.setUp(context)
    personaenv.before_feature(context, feature)
    context.config.log_capture = False

def after_feature(context, feature):
    personaenv.after_feature(context, feature)
    helpers.clear_data()

def before_scenario(context, scenario):
    personaenv.before_scenario(context, scenario)
    #context.personas = PERSONAS

def after_scenario(context, scenario):
    personaenv.after_scenario(context, scenario)
    helpers.clear_data()

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
