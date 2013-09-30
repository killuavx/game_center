# -*- encoding: utf-8-*-
from rest_framework import routers
from django.conf.urls import url, patterns
from mobapi import views

rest_router = routers.DefaultRouter()
rest_router.register('authors', views.AuthorViewSet)
rest_router.register('packages', views.PackageViewSet)
rest_router.register('search', views.PackageSearchViewSet, base_name='search')
rest_router.register('rankings', views.PackageRankingsViewSet, base_name='rankings')
rest_router.register('categories', views.CategoryViewSet)
rest_router.register('topics', views.TopicViewSet)
rest_router.register('tipswords', views.TipsWordViewSet)
views.documentation_advertisement_viewset()
rest_router.register('advertisements', views.AdvertisementViewSet)

urlpatterns = rest_router.urls

from mobapi.views import ( AccountCreateView,
                           AccountMyProfileView,
                           AccountSignoutView,
                           AccountAuthTokenView
                           )
urlpatterns += patterns('',
    url(r'^accounts/signup/?$', AccountCreateView.as_view(), name='account-signup'),
    url(r'^accounts/signin/?$', AccountAuthTokenView.as_view(), name='account-signin'),
    url(r'^accounts/signout/?$', AccountSignoutView.as_view(), name='account-signout'),
    url(r'^accounts/myprofile/?$', AccountMyProfileView.as_view(), name='account-myprofile'),
)
