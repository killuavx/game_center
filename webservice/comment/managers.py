# -*- coding: utf-8 -*-
from model_utils.managers import PassThroughManagerMixin
from toolkit.managers import CurrentSiteManager


class LetterManager(PassThroughManagerMixin, CurrentSiteManager):
    pass