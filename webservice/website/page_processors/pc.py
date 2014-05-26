# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic


@processor_for('pc/game')
def category_fill(request, page):
    game = Category.objects.get(slug='game')
    data = dict()
    data['category'] = game
    return data
