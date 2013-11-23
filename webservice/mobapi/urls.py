# -*- encoding: utf-8-*-
from rest_framework import routers
from django.conf.urls import url, patterns
from mobapi.warehouse.views.author import AuthorViewSet
from mobapi.warehouse.views.package import (
    PackageViewSet,
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

rest_router = routers.DefaultRouter()
rest_router.register('authors', AuthorViewSet)
rest_router.register('packages', PackageViewSet)
rest_router.register('search', PackageSearchViewSet, base_name='search')
rest_router.register('rankings', PackageRankingsViewSet, base_name='rankings')
rest_router.register('categories', CategoryViewSet)
rest_router.register('topics', TopicViewSet)
rest_router.register('tipswords', TipsWordViewSet)
documentation_advertisement_viewset()
rest_router.register('advertisements', AdvertisementViewSet)
rest_router.register('bookmarks',
                     PackageBookmarkViewSet,
                     base_name='bookmark')
rest_router.register('comments', CommentViewSet)

urlpatterns = rest_router.urls

from mobapi.views import SelfUpdateView

from mobapi.account.views import (AccountCreateView,
                                  AccountMyProfileView,
                                  AccountSignoutView,
                                  AccountAuthTokenView,
                                  AccountCommentPackageView)

urlpatterns += patterns('',
    url(r'^accounts/signup/?$', AccountCreateView.as_view(),
        name='account-signup', prefix='account'),
    url(r'^accounts/signin/?$', AccountAuthTokenView.as_view(),
        name='account-signin', prefix='account'),
    url(r'^accounts/signout/?$', AccountSignoutView.as_view(),
        name='account-signout', prefix='account'),
    url(r'^accounts/myprofile/?$', AccountMyProfileView.as_view(),
        name='account-myprofile', prefix='account'),
    url(r'^accounts/commented_packages/?$', AccountCommentPackageView.as_view(),
        name='account-commentedpackages', prefix='accont'),

    url(r'^selfupdate/?$', SelfUpdateView.as_view(),
        name='selfupdate',
        prefix='selfupdate'),

    url(r'^updates/?$', PackageUpdateView.as_view(), name='update-create', prefix='update'),
)

