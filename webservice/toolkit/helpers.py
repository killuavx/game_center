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