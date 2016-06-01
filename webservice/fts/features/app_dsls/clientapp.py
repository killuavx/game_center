# -*- coding: utf-8 -*-
import json


class ClientAppBaseDSL(object):

    _update_url = '/api/updates'

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        pass

    @classmethod
    def post_package_to_update(cls, context, **clientpkg):
        cls.post_many_packages_to_update(context, clientpkg)

    @classmethod
    def post_many_packages_to_update(cls, context, *clientpkgs):
        api_url = "%s%s" %(context.base_url, cls._update_url)
        qs = json.dumps(dict(versions=clientpkgs))
        context.client.post(api_url,
                            content_type='application/json',
                            data=qs)


def factory_dsl(context):
    return ClientAppBaseDSL


def setup(context):
    factory_dsl(context).setup(context)


def teardown(context):
    factory_dsl(context).teardown(context)
