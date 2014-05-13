# -*- coding: utf-8 -*-
from django.conf import settings
from website.cdn.model_register import *
from warehouse.models import Package, PackageVersion
from mptt.models import MPTTModel


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


def get_mptt_categories(pkg):
    result =  []

    cats = pkg.categories.all()
    for cat in cats:
        if MPTTModel.is_leaf_node(cat):
            result.append(cat)

    return result


def get_root_category_slug_by_cat(cat):
    return MPTTModel.get_root(cat).slug


def get_root_category_slug_by_package(package):
    cats = get_mptt_categories(package)
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

