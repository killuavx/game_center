# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from mobapi2.account.views import (AccountCreateView,
                                  AccountMyProfileView,
                                  AccountSignoutView,
                                  AccountAuthTokenView,
                                  AccountCommentPackageView)

urlpatterns = patterns('',
                       url(r'^signup/?$', AccountCreateView.as_view(),
                            name='account-signup', prefix='account'),
                       url(r'^signin/?$', AccountAuthTokenView.as_view(),
                           name='account-signin', prefix='account'),
                       url(r'^signout/?$', AccountSignoutView.as_view(),
                           name='account-signout', prefix='account'),
                       url(r'^myprofile/?$', AccountMyProfileView.as_view(),
                            name='account-myprofile', prefix='account'),
                       url(r'^commented_packages/?$',
                           AccountCommentPackageView.as_view(),
                           name='account-commentedpackages', prefix='accont'),

                       )
