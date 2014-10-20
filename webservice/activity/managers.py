# -*- coding: utf-8 -*-
from toolkit.managers import CurrentSitePassThroughManager, PublishedManager


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
