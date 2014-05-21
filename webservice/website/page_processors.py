# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from mezzanine.conf import settings

from website.ios_pc_models import get_package_by_package_name, get_packageversion_by_package
from website.ios_pc_models import get_root_category_slug_by_package, get_all_categories, get_leaf_categories
from website.ios_pc_models import filter_packages_by_category_slug, get_all_packages, get_authors_by_topic
from website.ios_pc_models import is_topic_slug, get_topic_slug, get_topic_by_slug, filter_packages_by_topic
from website.ios_pc_models import paginize_items, get_supported_language, filter_packages_by_supported_language
from website.ios_pc_models import get_category_slug, get_all_sub_cats, get_all_collections, get_packages_by_topic
from website.ios_pc_models import get_comments_by_packageversion


categories_page_slug = 'categories'
@processor_for(categories_page_slug)
def categories_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            func, args, kwargs = resolve(request.path_info)
            # mezzine.pages.views.page contains kwargs['slug']
            # with value "categories", replace it to default category slug
            slug = kwargs.get('slug')
            if categories_page_slug == slug:
                slug = settings.GC_CATEGORIES_DEFAULT_SLUG
            if slug is None:
                slug = settings.GC_CATEGORIES_DEFAULT_SLUG
            data['category'] = Category.objects.get(slug=slug)
        except (Resolver404, Category.DoesNotExist) as e:
            raise Http404()
    return data

topics_page_slug = 'topics'
@processor_for(topics_page_slug)
def topics_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            func, args, kwargs = resolve(request.path_info)
            slug = kwargs.get('slug')
            if topics_page_slug == slug:
                slug = settings.GC_TOPICS_CHOICE_SLUG
            if slug is None:
                slug = settings.GC_TOPICS_CHOICE_SLUG
            data['topic'] = Topic.objects.get(slug=slug)
        except (Resolver404, Topic.DoesNotExist) as e:
            raise Http404()
    return data

masterpiece_page_slug = 'masterpiece'
@processor_for(masterpiece_page_slug)
def masterpiece_fill(request, page):
    data = dict()
    if request.method == "GET":
        try:
            data['topic'] = Topic.objects.get(slug=settings.GC_TOPICS_MASTERPIECE_SLUG)
        except Topic.DoesNotExist as e:
            raise Http404()

    return data


game_page_slug = 'iospc/game'
@processor_for(game_page_slug)
def game_page(request, page):
    slug = 'game'
    other_slug = None

    if request.method == "GET":
        all_packages = get_all_packages()
        packages = filter_packages_by_category_slug(all_packages, slug)
        category_slug, category_query = get_category_slug(request)
        if category_slug != False:
            packages = filter_packages_by_category_slug(packages, category_slug)
        elif request.GET.get('topic', None):
            other_slug = request.GET.get('topic')
            topic_slug = get_topic_slug(other_slug, slug)
            topic = get_topic_by_slug(topic_slug)
            packages = filter_packages_by_topic(packages, topic)
        elif request.GET.get('pub', None) == 'latest':
            other_slug = request.GET.get('pub')
            packages = packages.by_published_order()
        elif request.GET.get('lang', None):
            other_slug = request.GET.get('lang')
            lang = get_supported_language(other_slug)
            if lang:
                packages = filter_packages_by_supported_language(packages, lang)
            else:
                packages = []
        else:
            packages = []

        sub_cats = get_leaf_categories(get_all_sub_cats(slug))
        pkgs, page_query, limit_range = paginize_items(request, packages)

    data = {
        'items': pkgs,
        'slug': slug,
        'cats': sub_cats,
        'page_query': page_query,
        'category_query': category_query,
        'category_slug': category_slug,
        'other_slug': other_slug,
        'limit_range': limit_range,
    }

    return data
