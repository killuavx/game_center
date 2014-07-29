# -*- encoding: utf-8-*-
from django.conf.urls import url, include, patterns
from mobapi2.warehouse.views.author import AuthorViewSet
from mobapi2.warehouse.views.package import (
    PackageViewSet,
    PackagePushView,
    PackageSearchViewSet,
    PackageUpdateView)
from mobapi2.taxonomy.views.category import CategoryViewSet
from mobapi2.taxonomy.views.topic import TopicViewSet
from mobapi2.searcher.views import TipsWordViewSet
from mobapi2.promotion.views import AdvertisementViewSet
from mobapi2.account.views import PackageBookmarkViewSet
from mobapi2.comment.views import CommentViewSet, FeedbackViewSet
from mobapi2.warehouse.views.packageversion import PackageVersionViewSet
from mobapi2.account.views import (AccountCreateView,
                                   AccountMyProfileView,
                                   AccountSignoutView,
                                   AccountAuthTokenView,
                                   AccountCommentPackageView)
from mobapi2.event.views import EventViewSet
from mobapi2.clientapp.views import SelfUpdateView, LoadingCoverView
from mobapi2.rest_router import rest_router
from mobapi2.ranking.views import PackageRankingViewSet
from mobapi2.activity.views import GiftBagViewSet


rest_router.register('authors', AuthorViewSet)
rest_router.register('packages', PackageViewSet)
rest_router.register('packageversions', PackageVersionViewSet)
rest_router.register('search', PackageSearchViewSet, base_name='search')
rest_router.register('rankings', PackageRankingViewSet,
                     base_name=PackageRankingViewSet.view_name)
rest_router.register('categories', CategoryViewSet)
rest_router.register('topics', TopicViewSet)
rest_router.register('tipswords', TipsWordViewSet)
rest_router.register('advertisements', AdvertisementViewSet)
rest_router.register('bookmarks', PackageBookmarkViewSet, base_name='bookmark')
rest_router.register('comments', CommentViewSet)
rest_router.register('feedbacks', FeedbackViewSet)
rest_router.register('events', EventViewSet, base_name='event')
rest_router.register('giftbags', GiftBagViewSet)


my_giftbags_list = GiftBagViewSet.as_view({
    'get': 'mine'
})

def _account_basename(name):
    prefix='account'
    basename = "%s-%s" %(prefix, name)
    return rest_router.get_base_name(basename)

account_urlpatterns = patterns('',
                       url(r'^signup/?$', AccountCreateView.as_view(),
                           name=_account_basename('signup')),
                       url(r'^signin/?$', AccountAuthTokenView.as_view(),
                           name=_account_basename('signin')),
                       url(r'^signout/?$', AccountSignoutView.as_view(),
                           name=_account_basename('signout')),
                       url(r'^myprofile/?$', AccountMyProfileView.as_view(),
                           name=_account_basename('myprofile')),
                       url(r'^commented_packages/?$',
                           AccountCommentPackageView.as_view(),
                           name=_account_basename('commentedpackages')),
                       url(r'^giftbags/?$', my_giftbags_list,
                           name=_account_basename('giftbags')),
                       )

slug_pattern = '[\w_.-]+'

urlpatterns = rest_router.urls
urlpatterns += patterns('',
    url(r'^selfupdate/?$', SelfUpdateView.as_view(),
        name=rest_router.get_base_name('selfupdate')),
    url(r'^push/packages/?$', PackagePushView.as_view(),
        name=rest_router.get_base_name('push-packages')),
    url(r'^updates/?$', PackageUpdateView.as_view(),
        name=rest_router.get_base_name('update-create')),
    url(r'^accounts/', include(account_urlpatterns)),
    url(r'^loadingcovers/(?P<package_name>%s)(/(?P<version_name>%s))?/?' %(slug_pattern,
                                                                         slug_pattern),
        LoadingCoverView.as_view(),
        name=rest_router.get_base_name('loadingcover')),
)

