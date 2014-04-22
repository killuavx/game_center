# -*- coding: utf-8 -*-
from mongoengine.connection import register_connection, get_connection
from website.settings import MOGOENGINE_CONNECTS

for con_key, con_opts in MOGOENGINE_CONNECTS.items():
    register_connection(alias=con_key,
                        name=con_opts.get('name'),
                        host=con_opts.get('host'),
                        port=con_opts.get('port'))
