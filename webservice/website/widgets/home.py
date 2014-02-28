# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django_widgets import Widget
from .common.blog import *
from .common.promotion import *
from .common.package import *
from .common.author import *
from .common.topic import *
from .common.category import *
from .common.picture import *
from .common.webspide import *


def str_to_bytes(string):
    if hasattr(string, 'encode'):
        return string.encode('utf-8')
    return string

#get the cache key for storage
def cache_get_key(*args, **kwargs):
    import hashlib
    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key,arg in kwargs.items():
        serialise.append(str(key))
        serialise.append(str(arg))
    key = hashlib.md5(str_to_bytes("".join(serialise))).hexdigest()
    return key

#decorator for caching functions
def cache_for(time):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            print('wrapper')
            print(args)
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                result = fn(*args, **kwargs)
                cache.set(key, result, time)
            return result
        return wrapper
    return decorator

import types

class DebugTrace(object):

    def __init__(self, f):
        print("Tracing: {0}".format(f.__name__))
        self.f = f
        self.ownerClass = None

    def __get__(self, obj, ownerClass=None):
        # Return a wrapper that binds self as a method of obj (!)
        self.ownerClass = ownerClass
        return types.MethodType(self, obj)

    def __call__(self, *args, **kwargs):
        print("Calling: {0}".format(self.f.__name__))
        print(self.f.__module__)
        print(self.f.__qualname__)

        instance = args[0]
        cls = instance.__class__
        print(cls.__module__)
        print(cls.__name__)

        return self.f(*args, **kwargs)

################################################################################


class HomeTopBannerWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/widgets/home/top-banner.haml'


class HomeTopCarouselAdvWidget(BaseMultiAdvWidget, Widget):

    template = 'pages/widgets/home/carousel-adv.haml'


class HomeTopSingleAdvWidget(BaseSingleAdvWidget, Widget):

    template = 'pages/widgets/common/single-adv.haml'


class HomeNewsPanelWidget(BasePostWidget, Widget):

    template = 'pages/widgets/home/news-panel.haml'


class HomeLatestPackagePanelWidget(BasePackageListWidget):

    def get_more_url(self):
        return reverse('mezzanine.pages.views.page', kwargs=dict(slug='latest'))

    template = 'pages/widgets/home/package-latest-panel.haml'


class HomeFirstCrackPackagePanelWidget(BasePackageListWidget):

    template = 'pages/widgets/home/package-firstcrack-panel.haml'


class HomeTopicPanelWidget(BaseTopicWidget, Widget):

    template = 'pages/widgets/home/topic-spec-panel.haml'


class HomeTopicAuthorPanelWidget(BaseTopicAuthorPanelWidget, Widget):

    template = 'pages/widgets/home/topic-author-panel.haml'


class HomeRankingPanelWidget(BaseRankingPackageListWidget, Widget):

    template = 'pages/widgets/home/package-ranking-panel.haml'


class HomeCategoryPackageTabsPanelWidget(BaseCategoryPackageListWidget, Widget):

    template = 'pages/widgets/home/category-packages-panel.haml'


class HomePictureShowcaseWidget(BasePictureShowcaseWidget, Widget):

    template = BasePictureShowcaseWidget.template


class HomeForumThreadPanelWidget(BaseForumThreadPanelWdiget, Widget):

    template = 'pages/widgets/home/forum-thread-panel.haml'
