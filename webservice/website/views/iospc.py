# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.core.urlresolvers import resolve
from website.ios_pc_models import *


def iospc_package_detail_views(request, package_name, *args, **kwargs):
    template = 'iospc/package-detail.html'

    pkg = get_package_by_package_name(package_name)
    all_cats = get_all_categories(pkg)
    leaf_cats = get_leaf_categories(all_cats)

    context = {}
    context['pkgver'] =  get_packageversion_by_package(pkg)
    context['slug'] = get_root_category_slug_by_package(pkg)
    context['cats'] = leaf_cats
    context['current_page'] = context['slug']
    try:
        category = pkg.categories.all()[0]
    except:
        category = ''

    context['root_cat'] = context['slug']
    context['sub_cat_name'] = category.name if category else ''
    context['sub_cat_slug'] = category.slug if category else ''
    context['package_title'] = pkg.title if pkg.title else ''
    comments = get_comments_by_packageversion(context['pkgver'])
    items, page_query, limit_range = paginize_items(request, comments, 1)
    context['items'] = items
    context['limit_range'] = limit_range
    context['page_query'] = page_query
    print (len(items))

    return TemplateResponse(request=request, template=template, context=context)


def iospc_packages_cat_list_views(request, slug, *args, **kwargs):
    template = 'iospc/categorized-packages-list.html'
    all_packages = get_all_packages()
    packages = filter_packages_by_category_slug(all_packages, slug)
    category_slug, category_query = get_category_slug(request)
    if category_slug != False:
        packages = filter_packages_by_category_slug(packages, category_slug)
    pkgs, page_query, limit_range = paginize_items(request, packages)

    sub_cats = get_leaf_categories(get_all_sub_cats(slug))

    context = {
        'items': pkgs,
        'slug': slug,
        'cats': sub_cats,
        'page_query': page_query,
        'category_query': category_query,
        'category_slug': category_slug,
        'current_page': slug,
        'limit_range': limit_range,
    }

    return TemplateResponse(request=request, template=template, context=context)


def iospc_packages_topic_list_views(request, cat_slug, other_slug, *args, **kwargs):

    template = 'iospc/categorized-packages-list.html'
    all_packages = get_all_packages()
    cat_packages = filter_packages_by_category_slug(all_packages, cat_slug)

    if is_topic_slug(other_slug):
        topic_slug = get_topic_slug(other_slug, cat_slug)
        topic = get_topic_by_slug(topic_slug)
        packages = filter_packages_by_topic(cat_packages, topic)
    elif other_slug == 'latest':
        packages = cat_packages.by_published_order()
    else:
        lang = get_supported_language(other_slug)
        #print (lang)
        if lang:
            packages = filter_packages_by_supported_language(cat_packages, lang)
        else:
            packages = cat_packages

    sub_cats = get_leaf_categories(get_all_sub_cats(cat_slug))
    pkgs, page_query, limit_range = paginize_items(request, packages)
    context = {
        'items': pkgs,
        'cats': sub_cats,
        'slug': cat_slug,
        'other_slug': other_slug,
        'page_query': page_query,
        'category_query': 'cat',
        'current_page': 'topic',
        'limit_range': limit_range,
    }

    return TemplateResponse(request=request, template=template, context=context)


def iospc_collectios_list_views(request, *args, **kwargs):

    template = 'iospc/collections-packages-list.html'

    collections = get_all_collections()

    result = []
    for collection in collections:
        packages = get_packages_by_topic(collection)
        result.append({
            'collection': collection,
            'packages': packages,
        })

    items, page_query, limit_range = paginize_items(request, result, 2)

    context = {
        'items': items,
        'page_query': page_query,
        'current_page': 'collection',
        'limit_range': limit_range,
    }

    return TemplateResponse(request=request, template=template, context=context)



def iospc_collection_detail_views(request, slug, *args, **kwargs):

    template = 'iospc/collection-packages.html'
    packages = []
    collection = get_topic_by_slug(slug)

    if collection:
        packages = get_packages_by_topic(collection)

    context = {
        'collection': collection,
        'packages': packages,
        'current_page': 'collection',
    }

    if slug == 'topic-xiaomo' and 'iospc_masterpiece_packages' \
            == resolve(request.path_info).url_name: # for masterpiece
        items, page_query, limit_range = paginize_items(request, packages, 2)
        template = 'iospc/masterpiece-packages.html'
        context =  {
            'items': items,
            'page_query': page_query,
            'current_page': 'masterpiece',
            'limit_range': limit_range,
        }

    return TemplateResponse(request=request, template=template, context=context)


def iospc_vendors_list_views(request, slug, pk, *args, **kwargs):
    template = 'iospc/vendors-packages.html'

    vendors = []
    current_vendor = None
    topic = get_topic_by_slug(slug)
    if topic:
        vendors = get_authors_by_topic(topic)
        #print (vendors.count())
        if vendors and pk:
            try:
                current_vendor = vendors.get(pk=pk)
            except:
                pass

    if vendors and current_vendor is None:
        current_vendor = vendors[0]

    packages = current_vendor.packages.published()
    items, page_query, limit_range = paginize_items(request, packages, 1)

    #print (len(items))
    context = {
        'current_vendor': current_vendor,
        'items': items,
        'vendors': vendors,
        'page_query': page_query,
        'current_page': 'vendor',
        'limit_range': limit_range,
    }

    return TemplateResponse(request=request, template=template, context=context)
