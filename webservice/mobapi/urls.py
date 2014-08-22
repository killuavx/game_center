# -*- encoding: utf-8-*-
from rest_framework import routers
from django.conf.urls import url, include, patterns
from mobapi.warehouse.views.author import AuthorViewSet
from mobapi.warehouse.views.package import (
    PackageViewSet,
    PackagePushView,
    PackageRankingsViewSet,
    PackageSearchViewSet,
    PackageUpdateView)
from mobapi.taxonomy.views.category import CategoryViewSet
from mobapi.taxonomy.views.topic import TopicViewSet
from mobapi.searcher.views import TipsWordViewSet
from mobapi.promotion.views import (
    AdvertisementViewSet,
    documentation_advertisement_viewset)
from mobapi.account.views import PackageBookmarkViewSet
from mobapi.comment.views import CommentViewSet
from mobapi.warehouse.views.packageversion import PackageVersionViewSet

rest_router = routers.DefaultRouter()
rest_router.register('authors', AuthorViewSet)
rest_router.register('packages', PackageViewSet)
rest_router.register('packageversions', PackageVersionViewSet)
rest_router.register('search', PackageSearchViewSet, base_name='search')
rest_router.register('rankings', PackageRankingsViewSet, base_name='rankings')
rest_router.register('categories', CategoryViewSet)
rest_router.register('topics', TopicViewSet)
rest_router.register('tipswords', TipsWordViewSet)
#documentation_advertisement_viewset()
rest_router.register('advertisements', AdvertisementViewSet)
rest_router.register('bookmarks',
                     PackageBookmarkViewSet,
                     base_name='bookmark')
rest_router.register('comments', CommentViewSet)

from analysis.views.rest_views import EventCreateView

urlpatterns = rest_router.urls

import mobapi.account
import mobapi.account.urls
from mobapi.clientapp.views import SelfUpdateView
urlpatterns += patterns('',
    url(r'^accounts/', include(mobapi.account.urls)),
    url(r'^selfupdate/?$', SelfUpdateView.as_view(),
        name='selfupdate',
        prefix='selfupdate'),
    url(r'^push/packages/?$', PackagePushView.as_view(), name='push-packages', prefix='push'),

    url(r'^updates/?$', PackageUpdateView.as_view(), name='update-create', prefix='update'),
    url(r'^events/?$', EventCreateView.as_view(), name='event-create')
)

