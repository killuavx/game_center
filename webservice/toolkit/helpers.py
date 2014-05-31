# -*- coding: utf-8 -*-
import hashlib
import json
import re
import copy
from urllib.parse import urljoin
from django.core.urlresolvers import reverse
from django.utils import importlib
import unicodedata
from django.utils.encoding import smart_text
from django.contrib.sites.models import Site, SITE_CACHE


def file_md5(f, iter_read_size=1024 ** 2 * 8):
    m = hashlib.md5()
    while True:
        data = f.read(iter_read_size)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def slugify_unicode(s):
    """
    Replacement for Django's slugify which allows unicode chars in
    slugs, for URLs in Chinese, Russian, etc.
    Adopted from https://github.com/mozilla/unicode-slugify/
    """
    chars = []
    for char in str(smart_text(s)):
        cat = unicodedata.category(char)[0]
        if cat in "LN" or char in "-_~":
            chars.append(char)
        elif cat == "Z":
            chars.append(" ")
    return re.sub("[-\s]+", "-", "".join(chars).strip()).lower()


def import_from(fullname):
    if callable(fullname):
        return fullname
    splited = fullname.split('.')
    classname = splited[-1]
    packagename = ".".join(splited[:-1])
    return getattr(importlib.import_module(packagename), classname)


def thumbnail_scale_percents(source, size_percents,
                             thumbnail_options={'quality': 85,
                                                'crop': False,
                                                'upscale': False}):
    from easy_thumbnails.files import get_thumbnailer
    thumbnailer = get_thumbnailer(source)
    size = calc_scale_percents_size(origin_size=(thumbnailer.width,
                                                 thumbnailer.height),
                                    size_percents=size_percents)
    thumbnail_options.update(size=size)
    return thumbnailer.get_thumbnail(thumbnail_options)


def calc_scale_percents_size(origin_size, size_percents):
    assert 0 < size_percents < 100, 'invalid size percents'
    size_w, size_h = [float(s) for s in origin_size]
    return int(size_w * size_percents / 100.0), int(size_h * size_percents / 100.0)


def sync_status_from(obj):
    from website.documents.cdn import SyncQueue
    publish_queues = SyncQueue.objects \
        .filter(latest_op_name='publish') \
        .by_content_object(obj)
    publish_count = publish_queues.count()
    FEEDBACK_CODE = 'SUCCESS'
    publish_finish = publish_queues.filter(latest_fb_result=FEEDBACK_CODE)
    publish_finish_count = publish_finish.count()
    return dict(finish=publish_finish_count, total=publish_count)


def sync_status_summary(obj):
    result = sync_status_from(obj)
    span_wrapper = '<span class="result">%s</span>'
    if not result['total']:
        return span_wrapper % 'Nofile/Unpublish'
    if result['finish'] == result['total']:
        return span_wrapper % 'OK'
    return span_wrapper %("""%s/%s""" %(result['finish'], result['total']))


def sync_status_actions(obj):
    from website.documents.cdn import PublishOperation
    from website.cdn.utils import get_dict_by_content_object
    mask = """<a href="javascript:void(0);" onclick="sync_%(op_name)s_file(this, '%(content_type)s', '%(object_pk)s', %(publishlevel)s);">%(text)s</a>"""
    data = get_dict_by_content_object(obj)
    refresh_link = mask % dict(op_name='publish',
                               text='publish(refresh)',
                               content_type=data['content_type'],
                               object_pk=data['object_pk'],
                               publishlevel=PublishOperation.FILE_LEVEL_REFRESH)
    preload_link = mask % dict(op_name='publish',
                               text='publish(preload)',
                               content_type=data['content_type'],
                               object_pk=data['object_pk'],
                               publishlevel=PublishOperation.FILE_LEVEL_PRELOAD)
    update_link = mask % dict(op_name='update',
                              text='update',
                              content_type=data['content_type'],
                              object_pk=data['object_pk'],
                              publishlevel=None)
    return " | ".join([refresh_link, preload_link, update_link])


def get_client_event_data(request):
    kwargs = dict()
    event_json = request.META.get('HTTP_X_CLIENT_EVENT')
    if event_json:
        try:
            data = dict(json.loads(event_json))
            kwargs.update(data)
        except ValueError:
            pass
    return kwargs


# -1 not using
# 0 not set using hostname
# 1 android
# 2 ios

SITE_DISABLE = -1

SITE_NOT_SET = 0

SITE_ANDROID = 1

SITE_IOS = 2

SITE_MAIN = 3

_GC_SITE_ID = SITE_NOT_SET


def set_global_site_id(site_id):
    global _GC_SITE_ID
    _GC_SITE_ID = site_id


def get_global_site_id():
    global _GC_SITE_ID
    return _GC_SITE_ID


def get_global_site():
    site_id = get_global_site_id()
    if site_id == SITE_DISABLE:
        return None

    if site_id == SITE_NOT_SET:
        site_id = current_site_id()

    if site_id not in SITE_CACHE:
        SITE_CACHE[site_id] = Site.objects.get(pk=site_id)
    return SITE_CACHE[site_id]


def build_site_absolute_uri(site, location):
    if site:
        current_uri = 'http://%s' % site.domain
        return urljoin(current_uri, location)
    else:
        return location


def current_site_id():
    """
        0. combine
        1. android
        2. ios
    """
    from mezzanine.utils.sites import current_site_id as _cur_site_id
    site_id = _cur_site_id()
    if site_id == 3:
        return 1
    return int(site_id)


def current_site():
    from mezzanine.utils.sites import current_site_id as _cur_site_id
    site_id = _cur_site_id()
    return Site.objects.get(pk=site_id)


def current_request():
    from mezzanine.core.request import current_request as _cur_request
    return _cur_request()


def admin_changelist_url(object):
    return reverse('admin:%s_%s_changelist' %(object._meta.app_label,
                                          object._meta.module_name), args=())


def iosappdata_listtag(package_name, content=None, target='_blank'):
    from crawler.models import IOSAppData
    url = "%s?q=%s" %(admin_changelist_url(IOSAppData), package_name)
    return '<a href="%s" target="%s">%s</a>' % (url, target, content or package_name)

