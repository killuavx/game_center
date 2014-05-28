# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from warehouse.models import Author

__all__ = ['vendors_fill']

@processor_for('/pc/game')
def category_fill(request, page):
    game = Category.objects.get(slug='game')
    data = dict()
    data['category'] = game
    return data

@processor_for('pc/vendors')
def vendors_fill(request, page):
    author_pk = request.GET.get('author')
    if not author_pk:
        author = None
    else:
        try:
            author = Author.objects.get(pk=author_pk)
        except ObjectDoesNotExist:
            author = None
    return dict(
        author=author
    )

