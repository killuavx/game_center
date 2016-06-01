# -*- coding: utf-8 -*-
import os
CELERY_BROKER_HOST = os.getenv('CELERY_BROKER_HOST', 'localhost')
BROKER_URL = 'redis://{0}:6379/2'.format(CELERY_BROKER_HOST)

# RabbitMQ management api
#broker_api = 'http://guest:guest@localhost:15672/api/'

# Enable debug logging
#logging = 'DEBUG'
