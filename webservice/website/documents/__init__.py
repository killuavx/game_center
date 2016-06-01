# -*- coding: utf-8 -*-
from mongoengine.connection import register_connection, get_connection
from django.conf import settings

con_key = 'systemresource'
con_opts = settings.MOGOENGINE_CONNECTS[con_key]
register_connection(alias=con_key,
                    name=con_opts.get('name'),
                    host=con_opts.get('host'),
                    port=con_opts.get('port'))
