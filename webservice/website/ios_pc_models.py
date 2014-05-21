# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from warehouse.models import Package, SupportedLanguage, Author
from mptt.models import MPTTModel
from taxonomy.models import Category, TopicalItem, Topic
from django.contrib.comments import Comment

def get_limit_range(p, r, n=10):
    # p - request page number
    # r - paginator.page_range
    # n - num of links on a page

    l = r[-1]
    if n >= l:
        return r
    x, y = divmod(p, n)
    m = n//2
    if y > 0:
        if p-m <= 0:
            return range(1, 2*m+1)
        elif p+m > l:
            end = l
        else:
            end = p+m
        return range(end-n+1, end+1)
    else:
        if p-m <= 0:
            return range(1, 2*m+1)
        elif p+m > l:
            end = l+1
            return range(end-n, end)
        else:
            end = p+m
        return range(p-m, end)

def get_all_categories(pkg):
    return pkg.categories.all()


def get_leaf_categories(cats):
    result =  []

    for cat in cats:
        if MPTTModel.is_leaf_node(cat):
            result.append(cat)

    return result


def get_root_category_slug_by_cat(cat):
    slug = None
    root_cat =  MPTTModel.get_root(cat)

    if root_cat:
        slug =  root_cat.slug

    return slug


def get_root_category_slug_by_package(package):
    cats = get_all_categories(package)
    slug = None

    if cats:
        slug = get_root_category_slug_by_cat(cats[0])

    return slug


def get_package_by_package_name(package_name):
    try:
        pkg = Package.objects.get(package_name=package_name)
    except:
        return None

    return pkg


def get_packageversion_by_package(package):
    try:
        pv = package.versions.latest_published()
    except:
        return None

    return pv


def get_root_category_by_slug(slug):
    try:
        root_cat = Category.objects.get(slug=slug)
    except:
        root_cat = None

    return root_cat



def filter_packages_by_category_slug(packages, slug):

    root_cat = get_root_category_by_slug(slug)

    if root_cat is None:
        return []

    cats = root_cat.get_descendants(True)
    pkgs =  packages.filter(categories__in=cats)
    if not pkgs:
        return []

    return  pkgs.distinct().by_published_order()


def get_all_sub_cats(slug):
    root_cat = get_root_category_by_slug(slug)

    if root_cat is None:
        return []
    else:
        return root_cat.get_descendants()


def get_all_packages():
    return Package.objects.published()


def is_topic_slug(slug):
    return slug in ['recommend', 'install']


def get_topic_slug(topic_slug, cat_slug):

    dic = {
        'recommend': ''.join(['home-recommend-', cat_slug]),
        'install': 'homebar-basic-installed',
    }

    #print (dic.get(topic_slug, None))
    return  dic.get(topic_slug, None)


def get_topic_by_slug(slug):

    try:
        topic = Topic.objects.filter(slug=slug).published().get()
    except:
        topic = None

    return topic


def paginize_items(request, items, per_page=20):
    page_query = 'page'

    page = request.GET.get(page_query)

    paginator = Paginator(items, per_page)

    try:
        pkgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        pkgs  = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pkgs = paginator.page(paginator.num_pages)

    limit_range = get_limit_range(int(page), paginator.page_range)

    return pkgs, page_query, limit_range


def get_category_slug(request):
    category_query = 'subcat'

    slug = request.GET.get(category_query)
    if slug is None or slug == '':
        return False, category_query

    return slug, category_query


def filter_packages_by_topic(packages, topic):
    return TopicalItem.objects.filter_items_by_topic(topic, Package, packages)


def get_supported_language(slug):
    try:
        lang = SupportedLanguage.objects.get(code=slug.upper())
    except:
        lang = None

    return lang


def filter_packages_by_supported_language(packages, lang):
    return packages.filter(versions__supported_languages__in=[lang])


#def filter_packages_by_supported_language(packages, lang):
#    pkgs = []
#
#    for pkg in packages:
#        flag = False
#        try:
#            flag = lang in pkg.versions.latest_published().supported_languages.all()
#        except:
#            pass
#
#        if flag:
#            pkgs.append(pkg)
#
#    return pkgs


def get_all_topics():
    return Topic.objects.published()


def get_all_collections():
    collections = []
    topics = get_all_topics()

    for tp in topics:
        lst = tp.get_children()
        collections.extend(lst)

    return collections


def get_packages_by_topic(topic):
    try:
        packages = TopicalItem.objects.get_items_by_topic(topic=topic, item_model=Package).published()
    except:
        packages = []

    return packages


def get_authors_by_topic(topic):
    try:
        authors = TopicalItem.objects.get_items_by_topic(topic=topic, item_model=Author)
    except:
        authors = []

    return authors


def get_comments_by_packageversion(packageversion):
    comments = Comment.objects.filter(object_pk=packageversion.pk)\
               .filter(is_public=True, is_removed=False)
    return comments

