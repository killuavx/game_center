# -*- encoding: utf-8-*-
from rest_framework import routers
from mobapi import views
from searcher import views_rest as searcher_views_rest

rest_router = routers.DefaultRouter()
rest_router.register('authors', views.AuthorViewSet)
rest_router.register('packages', views.PackageViewSet)
rest_router.register('search', views.PackageSearchViewSet)
rest_router.register('categories', views.CategoryViewSet)
rest_router.register('topics', views.TopicViewSet)
rest_router.register('tipswords', searcher_views_rest.TipsWordViewSet)

urlpatterns = rest_router.urls
