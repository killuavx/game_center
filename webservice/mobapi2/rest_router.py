# -*- coding: utf-8 -*-
from rest_framework import routers

class ApiVersionRouter(routers.DefaultRouter):

    prefix = 'api'

    version_prefix = 'v2'

    def __init__(self, version, trailing_slash=False):
        super(ApiVersionRouter, self).__init__(trailing_slash=trailing_slash)
        self.version_prefix = version

    def register(self, prefix, viewset, base_name=None):
        if base_name is not None:
            base_name = self.get_base_name(base_name)
        super(ApiVersionRouter, self).register(prefix=prefix, viewset=viewset, base_name=base_name)

    def get_default_base_name(self, viewset):
        name = super(ApiVersionRouter, self).get_default_base_name(viewset)
        return self.get_base_name(name)

    def get_base_name(self, base_name):
        return "-".join([self.prefix+self.version_prefix, base_name])

rest_router = ApiVersionRouter('v2', trailing_slash=True)
