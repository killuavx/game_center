# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from mezzanine.pages.page_processors import processor_for
from taxonomy.models import Category, Topic
from warehouse.models import Package
from mezzanine.conf import settings


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


android_game_page_slug = 'android/game'
@processor_for(android_game_page_slug)
def android_game(request, page):
    data = dict()
    if request.method == "GET":
        cat = request.GET.get('cat', None)
        topic = request.GET.get('topic', None)
        pub = request.GET.get('pub', None)
        page_num = request.GET.get('page', None)
        data['cat'] = cat
        data['topic'] = topic
        data['pub'] = pub
        data['page_num'] = page_num

    return data

android_app_page_slug = 'android/application'
@processor_for(android_app_page_slug)
def android_app(request, page):
    data = dict()
    if request.method == "GET":
        cat = request.GET.get('cat', None)
        topic = request.GET.get('topic', None)
        pub = request.GET.get('pub', None)
        page_num = request.GET.get('page', None)
        data['cat'] = cat
        data['topic'] = topic
        data['pub'] = pub
        data['page_num'] = page_num

    return data


android_crack_page_slug = 'android/crack'
@processor_for(android_crack_page_slug)
def android_crack(request, page):
    data = dict()
    if request.method == "GET":
        typl = request.GET.get('type', None)
        topic = request.GET.get('topic', None)
        page_num = request.GET.get('page', None)
        data['page_num'] = page_num
        data['type'] = typl
        data['topic'] = topic

    return data


android_topic_page_slug = 'android/topic'
@processor_for(android_topic_page_slug)
def android_topic(request, page):
    data = dict()
    if request.method == "GET":
        page_num = request.GET.get('page', None)
        name = request.GET.get('name', None)
        data['page_num'] = page_num
        data['topic'] = name

    return data


android_vendor_page_slug = 'android/vendor'
@processor_for(android_vendor_page_slug)
def android_vendor(request, page):
    data = dict()
    if request.method == "GET":
        id = request.GET.get('id', None)
        page_num = request.GET.get('page', None)
        data['page_num'] = page_num
        data['id'] = id

    return data


android_package_page_slug = 'package'
@processor_for(android_package_page_slug)
def android_package(request, page):
    data = dict()
    if request.method == "GET":
        name = request.GET.get('name', None)
        page_num = request.GET.get('page', None)
        try:
            pkg = Package.objects.get(package_name=name)
            pkgv = pkg.versions.latest_published()
        except:
            pkg, pkgv = None, None

        try:
            cat = pkg.categories.all()[0]
            related_pkgs =  cat.packages.published()
        except:
            cat, related_pkgs = None, None

        data['page_num'] = page_num
        data['name'] = name
        data['pkg'] = pkg
        data['pkgv'] = pkgv
        data['cat'] = cat
        data['related_pkgs'] = related_pkgs

    return data


android_rank_page_slug = 'android/rank'
@processor_for(android_rank_page_slug)
def android_rank(request, page):
    data = dict()
    if request.method == "GET":
        type = request.GET.get('type', None)
        data['type'] = type

    return data

