# -*- coding: utf-8 -*-
import os
MOGOENGINE_CONNECTS = {
    'default': {
        'host': os.getenv('MONGODB_HOST_DC', 'localhost'),
        'port': int(os.getenv('MONGODB_PORT_DC', 27017)),
        'name': os.getenv('MONGODB_NAME_DC', 'data_center'),
        },
    'data_center': {
        'host': os.getenv('MONGODB_HOST_DC', 'localhost'),
        'port': int(os.getenv('MONGODB_PORT_DC', 27017)),
        'name': os.getenv('MONGODB_NAME_DC', 'data_center'),
    },
    'systemresource': {
        'host': os.getenv('MONGODB_HOST_SR', 'localhost'),
        'port': int(os.getenv('MONGODB_PORT_SR', 27017)),
        'name': os.getenv('MONGODB_NAME_SR', 'systemresource'),
    },
    'datawarehouse': {
        'host': os.getenv('MONGODB_HOST_DW', 'localhost'),
        'port': int(os.getenv('MONGODB_PORT_DW', 27017)),
        'name': os.getenv('MONGODB_NAME_DW', 'datawarehouse'),
    },
}
