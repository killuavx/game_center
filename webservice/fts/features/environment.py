# -*- coding: utf-8 -*-
import os
from behaving.personas import environment as personaenv
from behaving.web import environment as webenv
from fts import helpers
from fts.features import support
from toolkit.middleware import get_current_request, get_current_response
from toolkit.helpers import import_from
from datetime import datetime

PERSONAS = {}


def take_screenshot(ctx):
    if hasattr(ctx, 'browser') and ctx.browser:
        n = datetime.now().isoformat()
        filename = ctx.browser.screenshot(n)
        return filename


def after_screenshot(ctx, filename):
    if not filename:
        return
    print('Fail scenario screenshot: "%s"' % filename)
    try:
        import sh
        sh.open(filename)
    except:
        with open(filename, 'r') as f:
            print(f.readlines())


from fts.features.app_dsls.account import (setup as account_setup,
                                           teardown as account_teardown)
from fts.features.app_dsls.warehouse import (setup as warehouse_setup,
                                             teardown as warehouse_teardown)
from fts.features.app_dsls.comment import (setup as comment_setup,
                                           teardown as comment_teardown)


def setup(context):
    import fts

    _dir = os.path.dirname(fts.__file__)
    context.fixture_dir = os.path.join(_dir, 'tests/fixtures')
    context.attachment_dir = context.fixture_dir
    context.get_current_request = get_current_request
    context.get_current_response = get_current_response

    if not hasattr(context, 'world'):
        context.world = {}


def setup_dsls(context):
    account_setup(context)
    warehouse_setup(context)
    comment_setup(context)


def setup_client(context):
    context.base_url = 'http://localhost:8080'
    factory_web_dsl = import_from('fts.features.app_dsls.web.factory_dsl')
    WebDSL = factory_web_dsl(context)
    WebDSL.browser_or_client(context)


def teardown_client(context):
    if hasattr(context, 'client'):
        context.client = None


def teardown_dsls(context):
    account_teardown(context)
    warehouse_teardown(context)
    comment_teardown(context)


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
    setup_dsls(context)
    personaenv.before_scenario(context, scenario)
    webenv.before_scenario(context, scenario)
    setup_client(context)


def after_scenario(context, scenario):
    if context.failed:
        filename = take_screenshot(context)
        if filename:
            after_screenshot(context, filename)

    personaenv.after_scenario(context, scenario)
    webenv.after_scenario(context, scenario)
    teardown_client(context)
    teardown_dsls(context)
    teardown(context)

