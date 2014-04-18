# -*- coding: utf-8 -*-
import os
MOGOENGINE_CONNECTS = {
    'default': {
        'host': os.getenv('MONGODB_HOST_DW', 'localhost'),
        'port': os.getenv('MONGODB_PORT_DW', 27017),
        'name': os.getenv('MONGODB_NAME_DW', 'datawarehouse'),
        },
    'systemresource': {
        'host': os.getenv('MONGODB_HOST_SR', 'localhost'),
        'port': os.getenv('MONGODB_PORT_SR', 27017),
        'name': os.getenv('MONGODB_NAME_SR', 'systemresource'),
        }
}
