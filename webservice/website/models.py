# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from website.cdn.model_register import *
from warehouse.models import Package, PackageVersion, SupportedLanguage
from mptt.models import MPTTModel
from taxonomy.models import Category, TopicalItem, Topic


def mock_processor_class(processor_class):
    from website.cdn.parsers import OperationRequest

    class MockOperationRequest(OperationRequest):

        def request(self):
            self.request_data = self.create_querydata()
            STATUS_CODE_SUCCESS = self.response_class.STATUS_CODE_SUCCESS
            response = self.response_class(STATUS_CODE_SUCCESS, 'receive finish')
            response.result = response.result_string(STATUS_CODE_SUCCESS)
            return response

    class MockProcessorMixin(object):

        request_class = MockOperationRequest

        def get_source_host(self):
            return 'gc.ccplay.com.cn'

    class MockProcessor(MockProcessorMixin, processor_class):
        pass
    return MockProcessor

if settings.DEBUG:
    PackageVersion.sync_processor_class = \
        mock_processor_class(PackageVersionProcessor)

    Advertisement.sync_processor_class = \
        mock_processor_class(AdvertisementProcessor)

    Topic.sync_processor_class = \
        mock_processor_class(TopicProcessor)

    Category.sync_processor_class = \
        mock_processor_class(CategoryProcessor)

    ClientPackageVersion.sync_processor_class = \
        mock_processor_class(ClientPackageVersionProcessor)

    LoadingCover.sync_processor_class = \
        mock_processor_class(LoadingCoverProcessor)


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


def paginize_packages(request, packages, per_page=20):
    page_query = 'page'

    page = request.GET.get(page_query)

    paginator = Paginator(packages, per_page)

    try:
        pkgs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pkgs  = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pkgs = paginator.page(paginator.num_pages)

    return pkgs, page_query


def get_category_slug(request):
    category_query = 'cat'

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


def get_all_topics():
    return Topic.objects.all()


def get_all_collections():
    collections = []
    topics = get_all_topics()

    for tp in topics:
        lst = tp.get_children()
        collections.extend(lst)

    return collections
