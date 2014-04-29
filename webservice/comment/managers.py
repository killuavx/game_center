# -*- coding: utf-8 -*-
from model_utils.managers import PassThroughManager
from managers import CurrentSiteManager


class LetterManager(CurrentSiteManager,
                    PassThroughManager):
    pass