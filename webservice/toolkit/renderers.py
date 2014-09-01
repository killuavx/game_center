# -*- coding: utf-8 -*-
from rest_framework.renderers import BrowsableAPIRenderer as RFBrowsableAPIRenderer
class BrowsableAPIRenderer(RFBrowsableAPIRenderer):
    """
    HTML renderer used to self-document the API.
    """
    media_type = 'text/html,type=api'
