# -*- coding: utf-8 -*-
from django.conf import settings
from website.cdn.model_register import *


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
    Author.sync_processor_class = \
        mock_processor_class(AuthorProcessor)
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


from searcher.helpers import get_default_package_query
from searcher.search_results import PackageSearchResult
from toolkit.helpers import get_global_site
from taxonomy.models import Topic, TopicManager, AllTopicManager, TopicQuerySet


class TopicProxy(Topic):

    @property
    def parent(self):
        if hasattr(self, '__parent'):
            return self.__parent
        parent = super(TopicProxy, self).parent
        if parent:
            parent.__class__ = TopicProxy

        self.__parent = parent
        return parent

    @parent.setter
    def parent(self, parent):
        self.__parent = parent


    @property
    def children(self):
        children = super(TopicProxy, self).children
        children.model = TopicProxy
        return children

    @property
    def get_children(self):
        children = super(TopicProxy, self).get_children()
        children.model = TopicProxy
        return children

    def _search_packages_queryset(self):
        return get_default_package_query(PackageSearchResult)\
            .filter(site=get_global_site().pk)

    def get_packages(self):
        return self._search_packages_queryset().filter(topic_ids=self.pk)

    def get_packages_topicalordering(self):
        return self.get_packages().order_by('topic_%d_ordering_i' % self.pk)

    @property
    def packages_count(self):
        return self.get_packages().count()

    @property
    def packages(self):
        return self.get_packages().order_by('-released_datetime')

    @property
    def packages_topicalordering(self):
        return self.get_packages_topicalordering()

    class Meta:
        proxy = True
