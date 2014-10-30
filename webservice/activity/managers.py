# -*- coding: utf-8 -*-
from toolkit.managers import CurrentSitePassThroughManager, PublishedManager
from model_utils.managers import PassThroughManagerMixin


class GiftBagManager(CurrentSitePassThroughManager,
                     PublishedManager):
    pass


class GiftCardManager(CurrentSitePassThroughManager):
    pass


class ActivityManager(CurrentSitePassThroughManager,
                      PublishedManager):
    pass


class BulletinManager(CurrentSitePassThroughManager,
                      PublishedManager):
    pass


class LotteryManager(PassThroughManagerMixin,
                     PublishedManager):
    pass
