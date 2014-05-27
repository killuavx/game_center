# -*- coding: utf-8 -*-
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic

@processor_for('/pc/game')
def category_fill(request, page):
    game = Category.objects.get(slug='game')
    data = dict()
    data['category'] = game
    return data

@processor_for('/pc/venders')
def vendors_fill(request, page):
    data = dict()
    from pprint import pprint as print
    print(request.__dict__)
    return data
