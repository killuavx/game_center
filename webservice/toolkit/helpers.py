# -*- coding: utf-8 -*-
from django.utils import importlib


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

