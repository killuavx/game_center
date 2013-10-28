# -*- coding: utf-8 -*-
from os.path import join, abspath, dirname
from django.conf import settings

app_dir = join(dirname(abspath(__file__)), 'utils')

AAPT_CMD = getattr(settings, 'AAPT_CMD',
                   join(app_dir, 'utils/android-tools-linux-x64/aapt'))

UNZIP_FILE_TEMP_DIR = getattr(settings, 'UNZIP_FILE_TEMP_DIR', '/tmp/warehouse-uploader')
