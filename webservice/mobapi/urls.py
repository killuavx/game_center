# -*- encoding: utf-8-*-
from rest_framework import routers
from mobapi import views

rest_router = routers.DefaultRouter()
rest_router.register('authors', views.AuthorViewSet)
rest_router.register('packages', views.PackageViewSet)
rest_router.register('search', views.PackageSearchViewSet, base_name='search')
rest_router.register('rankings', views.PackageRankingsViewSet, base_name='rankings')
rest_router.register('categories', views.CategoryViewSet)
rest_router.register('topics', views.TopicViewSet)
rest_router.register('tipswords', views.TipsWordViewSet)
rest_router.register('advertisements', views.AdvertisementViewSet)

urlpatterns = rest_router.urls
