# -*- encoding: utf-8-*-
from django.conf.urls import url, include, patterns
from mobapi2.warehouse.views.author import AuthorViewSet
from mobapi2.warehouse.views.package import (
    PackageViewSet,
    PackagePushView,
    PackageSearchViewSet,
    PackageUpdateView)
from mobapi2.warehouse.views import package as package_views
from mobapi2.taxonomy.views.category import CategoryViewSet
from mobapi2.taxonomy.views.topic import TopicViewSet
from mobapi2.searcher.views import TipsWordViewSet
from mobapi2.promotion import views as promotion_views
from mobapi2.account.views import PackageBookmarkViewSet
from mobapi2.comment.views import CommentViewSet, FeedbackViewSet
from mobapi2.warehouse.views.packageversion import PackageVersionViewSet
from mobapi2.account import views as account_views
from analysis.views.rest_views import EventCreateView
from mobapi2.clientapp import views as clientapp_views
from mobapi2.rest_router import rest_router
from mobapi2.ranking.views import PackageRankingViewSet
from mobapi2.activity import views as activity_views

rest_router.register('authors', AuthorViewSet)
rest_router.register('packages', PackageViewSet)
rest_router.register('packageversions', PackageVersionViewSet)
rest_router.register('search', PackageSearchViewSet, base_name='search')
rest_router.register('rankings', PackageRankingViewSet,
                     base_name=PackageRankingViewSet.view_name)
rest_router.register('categories', CategoryViewSet)
rest_router.register('topics', TopicViewSet)
rest_router.register('tipswords', TipsWordViewSet)
rest_router.register('advertisements', promotion_views.AdvertisementViewSet)
rest_router.register('bookmarks', PackageBookmarkViewSet, base_name='bookmark')
rest_router.register('comments', CommentViewSet)
rest_router.register('feedbacks', FeedbackViewSet)
rest_router.register('coin_packages', package_views.PackageCoinViewSet, base_name='coin_package')
rest_router.register('notes', activity_views.NoteViewSet)
rest_router.register('bulletins', activity_views.BulletinViewSet)
rest_router.register('activities', activity_views.ActivityViewSet)
rest_router.register('lotteries', activity_views.LotteryViewSet)
lottery_active_view = activity_views.LotteryViewSet.as_view({'get': 'active'})
lottery_winning_view = activity_views.LotteryViewSet.as_view({'get': 'winning_detail_richpage'})
lottery_viewname = rest_router.get_default_base_name(activity_views.LotteryViewSet)
lottery_urlpatterns = patterns('',
   url('^active/?$', lottery_active_view, name="%s-active" %lottery_viewname),
   url('^winning/(?P<winning_id>\d+)/?$', lottery_winning_view, name="%s-winning-detail-richpage" %lottery_viewname),
)

rest_router.register('giftbags', activity_views.GiftBagViewSet)
scratchcard_play = activity_views.ScratchCardViewSet.as_view({'get': 'play'})
scratchcard_award = activity_views.ScratchCardViewSet.as_view({'post': 'award'})
scratchcard_winners = activity_views.ScratchCardViewSet.as_view({'get': 'winners'})
scratchcard_basename = rest_router.get_default_base_name(activity_views.ScratchCardViewSet)
scratchcard_urlpatterns = patterns('',
   url('^winners/?$', scratchcard_winners, name="%s-winners" %scratchcard_basename),
   url('^play/?$', scratchcard_play, name="%s-play" %scratchcard_basename),
   url('^award/?$', scratchcard_award, name="%s-award" %scratchcard_basename),
)

my_giftbags_list = activity_views.GiftBagViewSet.as_view({
    'get': 'mine'
})

def _account_basename(name):
    prefix='account'
    basename = "%s-%s" %(prefix, name)
    return rest_router.get_base_name(basename)

account_urlpatterns = patterns('',
                       url(r'^signup/?$', account_views.AccountCreateView.as_view(),
                           name=_account_basename('signup')),
                       url(r'^signin/?$', account_views.AccountAuthTokenView.as_view(),
                           name=_account_basename('signin')),
                       url(r'^signin/weixin/?$', account_views.AccountWXAuthTokenView.as_view(),
                           name=_account_basename('signin-wx')),
                       url(r'^signout/?$', account_views.AccountSignoutView.as_view(),
                           name=_account_basename('signout')),
                       url(r'^myprofile/?$', account_views.AccountMyProfileView.as_view(),
                           name=_account_basename('myprofile')),
                       url(r'^newpassword/?$', account_views.AccountChangePasswordView.as_view(),
                           name=_account_basename('newpassword')),
                       url(r'^commented_packages/?$',
                           account_views.AccountCommentPackageView.as_view(),
                           name=_account_basename('commentedpackages')),
                       url(r'^giftbags/?$', my_giftbags_list,
                           name=_account_basename('giftbags')),
                       )

task_urlpatterns = patterns('',
    url(r'^mystatus/(.(?P<format>[\w_-]+))?$',
        activity_views.TaskViewSet.as_view({'get': 'mystatus'}),
        name=rest_router.get_base_name('task-mystatus')),
    url(r'^install/(.(?P<format>[\w_-]+))?$',
        activity_views.TaskViewSet.as_view({'post': 'install'}),
        name=rest_router.get_base_name('task-install')),
    url(r'^share/(.(?P<format>[\w_-]+))?$',
        activity_views.TaskViewSet.as_view({'post': 'share'}),
        name=rest_router.get_base_name('task-share')),
    url(r'^signin/(.(?P<format>[\w_-]+))?$',
        activity_views.TaskViewSet.as_view({'post': 'signin'}),
        name=rest_router.get_base_name('task-signin')),
)

from mobapi2.clientapp.views import HomePageViewSet

home_urlpatterns = patterns('',
    url(r'^network/(.(?P<format>[\w_-]+))?',
        HomePageViewSet.as_view({'get':'network'}),
        name=rest_router.get_base_name('home-network')),
    url(r'^recommend/(.(?P<format>[\w_-]+))?',
        HomePageViewSet.as_view({'get':'recommend'}),
        name=rest_router.get_base_name('home-recommend')),
)

slug_pattern = '[\w_.-]+'

urlpatterns = patterns('',
                       url(r'^lotteries/', include(lottery_urlpatterns)),
                       )
urlpatterns += rest_router.urls
urlpatterns += patterns('',
    url(r'^home/', include(home_urlpatterns)),
    url(r'^tasks/', include(task_urlpatterns)),
    url(r'^recommends/(.(?P<format>[\w_-]+))?$', promotion_views.RecommendListView.as_view(),
        name=rest_router.get_base_name('recommend-list')),
    url(r'^recommends/(?P<date>[\d-]+)/(.(?P<format>[\w_-]+))?$', promotion_views.RecommendView.as_view(),
        name=rest_router.get_base_name('recommend-detail')),
    url(r'^scratchcards/', include(scratchcard_urlpatterns)),
    url(r'^selfupdate/?$', clientapp_views.SelfUpdateView.as_view(),
        name=rest_router.get_base_name('selfupdate')),
    url(r'^push/packages/?$', PackagePushView.as_view(),
        name=rest_router.get_base_name('push-packages')),
    url(r'^updates/?$', PackageUpdateView.as_view(),
        name=rest_router.get_base_name('update-create')),
    url(r'^accounts/', include(account_urlpatterns)),
    url(r'^notification/?$',
        activity_views.NotificationViewSet.as_view({'get':'retrieve_all'}),
        name=rest_router.get_base_name('notification-all')),
    url(r'^loadingcovers/active/?$',
        clientapp_views.LoadingCoverViewSet.as_view({'get':'active'}),
        name=rest_router.get_base_name('loadingcover-active')),
    url(r'^events/?$', EventCreateView.as_view(), name=rest_router.get_base_name('event'))
)
