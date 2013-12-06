# -*- coding: utf-8 -*-
from mongoengine.connection import get_connection


class AnalysisBaseDSL(object):

    @classmethod
    def setup(cls, context):
        pass

    @classmethod
    def teardown(cls, context):
        connect = get_connection()
        [connect.drop_database(dbname) for dbname in connect.database_names()]
        connect.close()

    @classmethod
    def post_event(cls, context, **kwargs):
        raise NotImplementedError('you must implement %s.%s' %(
            cls, 'post_event'
        ))


class AnalysisRestDSL(AnalysisBaseDSL):

    _event_url = '/api/events/'

    @classmethod
    def post_event(cls, context, **kwargs):
        context.client.post(cls._event_url, kwargs)


def factory_dsl(context):
    return AnalysisRestDSL


def setup(context):
    return factory_dsl(context).setup(context)


def teardown(context):
    return factory_dsl(context).teardown(context)
