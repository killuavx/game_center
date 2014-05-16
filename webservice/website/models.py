# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from website.cdn.model_register import *
from warehouse.models import Package, PackageVersion
from mptt.models import MPTTModel
from taxonomy.models import Category, TopicalItem


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


def filter_packages_by_category_slug(packages, slug):
    try:
        root_cat = Category.objects.get(slug=slug)
    except:
        return []

    cats = root_cat.get_descendants(True)
    pkgs =  packages.filter(categories__in=cats)
    if not pkgs:
        return []

    return  pkgs.distinct().by_published_order()


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
    topic = None

    try:
        topic = Topic.objects.filter(slug=slug).published().get()
    except:
        pass

    return topic


def paginize_packages(packages, page, per_page=20):
    pg = Paginator(packages, per_page)
    page = 1 if page is None else int(page)

    try:
        pkgs = pg.page(page)
    except EmptyPage:
        pkgs = []

    return pkgs


def get_filtered_packages_by_topic(packages, topic):
    return TopicalItem.objects.filter_items_by_topic(topic, Package, packages)







