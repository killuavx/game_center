# -*- encoding=utf-8 -*-
import io
import os
from os.path import join, dirname, abspath
import json
from urllib import parse as urlparse
from collections import namedtuple

from django.test.testcases import TestCase
from django.test.client import Client
from django import forms
from django.core.files import File
from django.db.models.signals import pre_save
from rest_framework.authtoken.models import Token
from django.utils.timezone import now, timedelta
from should_dsl import should

from searcher.models import TipsWord
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from warehouse.models import package_version_pre_save
from taxonomy.models import Category, Topic, TopicalItem
from account.models import User as Player
from toolkit.middleware import get_current_request
from mobapi.warehouse.serializers.package import PackageSummarySerializer, PackageDetailSerializer


fixtures_dir = join(dirname(abspath(__file__)), 'fixtures')

StatusCode = namedtuple('StatusCode', ['code', 'reason'])

import random

_models = []
_files = []


def guid():
    def S4():
        return hex(int(((1 + random.random()) * 0x10000) or 0))[2:]

    return "%s-%s-%s-%s" % (S4(), S4(), S4(), S4())


def add_model_objects(*args):
    _models.extend(args)


def create_category(**defaults):
    defaults.setdefault('name', "Game")
    inst = Category.objects.create(**defaults)
    _models.append(inst)
    return inst


def create_author(**defaults):
    defaults.setdefault('email', 'kent-back@testcase.com')
    defaults.setdefault('name', "Kent Back")
    inst, flag = Author.objects.get_or_create(**defaults)
    _models.append(inst)
    return inst


def create_package(**defaults):
    id = guid()
    defaults.setdefault('title', "fts-dsl game %s" % id)
    defaults.setdefault('package_name', "com.fts.dsl-helper.%s" % id)
    if not defaults.get('author'):
        rdnum = random.randint(1, 1000),
        defaults.setdefault('author', create_author(
            name="tc %d" % rdnum,
            email="tc%d@testcase.com" % rdnum
        ))
    inst = Package.objects.create(**defaults)
    _models.append(inst)
    return inst


def create_packageversion(package, **default):
    inst = PackageVersion.objects.create(package=package,
                                         **default)
    _models.append(inst)
    return inst


def create_packageversionscreenshot(**defaults):
    id = guid()
    defaults.setdefault('alt', 'alt-%s' % id)
    inst = PackageVersionScreenshot(**defaults)
    _models.append(inst)
    return inst


def create_topic(**defaults):
    id = guid()
    defaults.setdefault('name', 'topic %s' % id)
    defaults.setdefault('slug', 'topic-%s' % id)
    inst = Topic.objects.create(**defaults)
    _models.append(inst)
    return inst


def create_topicalitem(topic, item):
    inst = TopicalItem.objects.create(topic=topic, content_object=item)
    _models.append(inst)
    return inst


def create_tipsword(**defaults):
    inst = TipsWord.objects.create(**defaults)
    _models.append(inst)
    return inst


def create_account(**default):
    gid = guid()
    default.setdefault('username', "player-%s" % gid)
    default.setdefault('email', '%s@testcase.com' % gid)

    def rint():
        return str(random.randint(10, 99))

    default.setdefault('phone',
                       '+86-021-%s%s%s%s' % (rint(), rint(), rint(), rint()))
    inst = Player.objects.create_user(**default)
    _models.append(inst)
    return inst


def create_auth_token(user):
    token, is_newed = Token.objects.get_or_create(user=user)
    _models.append(token)
    return token.key


def clear_data():
    while True:
        try:
            m = _models.pop()
            m.delete()
        except AssertionError:
            pass
        except IndexError:
            break

    while True:
        f = None
        try:
            f = _files.pop()
        except IndexError:
            break
        try:
            os.remove(f)
        except:
            pass


def convert_content(content):
    try:
        content = content.decode('utf-8')
    except:
        pass

    try:
        return json.loads(content)
    except:
        return content


def disconnect_packageversion_pre_save():
    pre_save.disconnect(package_version_pre_save, PackageVersion)


def connect_packageversion_pre_save():
    pre_save.connect(package_version_pre_save, PackageVersion)


def _world_response_status(context, res):
    context.world.update(dict(
        response=res,
        content=convert_content(res.content),
        status=StatusCode(
            code=res.status_code,
            reason=res.status_text
        )
    ))


def sub_file_package():
    return join(fixtures_dir, 'tinysize.apk')


class SubFile(object):

    fixtures_dir = fixtures_dir

    @classmethod
    def package(cls, type='apk'):
        name = 'tinysize.apk'
        if type == 'cpk':
            name = 'appexample/appdata-nodata-gpk.cpk'
        return cls.file(name)

    @classmethod
    def icon(cls):
        name = 'icon.png'
        return cls.file(name)

    @classmethod
    def cover(cls):
        name = 'cover.jpg'
        return cls.file(name)

    @classmethod
    def screenshot(cls):
        name = 'screenshot1.jpg'
        return cls.file(name)


    @classmethod
    def file(cls, name):
        return File(io.FileIO(join(cls.fixtures_dir, name)))

    @classmethod
    def fixture_filename(cls, name):
        return join(fixtures_dir, name)

