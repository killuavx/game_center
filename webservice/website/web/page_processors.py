# -*- coding: utf-8 -*-
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from django.core.exceptions import ObjectDoesNotExist
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from warehouse.models import Author

__all__ = ['vendors_fill', 'category_fill', 'ranking_fill']


def category_fill(request, page):
    cat_slug = 'game'
    if page.slug.endswith('game'):
        cat_slug = 'game'
    if page.slug.endswith('application'):
        cat_slug = 'application'

    cat_pk = request.GET.get('category')
    category = None
    if cat_pk:
        try:
            category = Category.objects.get(pk=cat_pk)
        except ObjectDoesNotExist:
            pass

    topic_pk = request.GET.get('topic')
    topic = None
    if topic_pk:
        try:
            topic = Topic.objects.get(pk=topic_pk)
        except ObjectDoesNotExist:
            pass

    root = Category.objects.get(slug=cat_slug)
    if not category:
        category = root
    data = dict(
        category=category,
        topic=topic,
        root_category=root,
        lang=request.GET.get('lang')
    )
    return data

processor_for('game')(category_fill)
processor_for('application')(category_fill)

@processor_for('vendors')
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


def ranking_fill(request, page):
    if page.slug == 'ranking':
        cat_slug = 'game'
    else:
        cat_slug = page.slug.split('/')[1]
    category = Category.objects.get(slug=cat_slug)

    return dict(
        category=category
    )

processor_for('ranking')(ranking_fill)
processor_for('ranking/game')(ranking_fill)
processor_for('ranking/application')(ranking_fill)
