# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author
from taxonomy.models import Category
from django.utils.timezone import now
import random
import logging

_models = []

def create_category(**defaults):
    logging.info('create_category', defaults)
    defaults.setdefault('name', "Game")
    inst = Category.objects.create(**defaults)
    _models.append(inst)
    return inst

def create_author(**defaults):
    logging.info('create_author', defaults)
    defaults.setdefault('email', 'kent-back@testcase.com')
    defaults.setdefault('name', "Kent Back")
    inst, flag = Author.objects.get_or_create(**defaults)
    _models.append(inst)
    return inst

def create_package(**defaults):
    logging.info('create_package', defaults)
    defaults.setdefault('title', "大富翁")
    defaults.setdefault('package_name', "com.package.%s" % now().strftime('%Y%m%d%H%M%s'))
    if not defaults.get('author'):
        rdnum = random.randint(1, 1000),
        defaults.setdefault('author', create_author(
            name="tc %d" % rdnum,
            email="tc%d@testcase.com" % rdnum
        ))
    inst = Package.objects.create(**defaults)
    _models.append(inst)
    return inst

def clear_data():
    [m.delete() for m in _models]
