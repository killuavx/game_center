# -*- encoding=utf-8 -*-
from warehouse.models import Package, Author
from taxonomy.models import Category
def create_category(**defaults):
    defaults.setdefault('name', "Game")
    return Category.objects.create(**defaults)

def create_author(**defaults):
    defaults.setdefault('name', "Kent Back")
    return Author.objects.create(**defaults)

def create_package(**defaults):
    defaults.setdefault('title', "大富翁")
    defaults.setdefault('package_name', "com.dafuweng")
    if not defaults.get('author'):
        defaults.setdefault('author', create_author())
    return Package.objects.create(**defaults)
