# -*- coding: utf-8 -*-

from easy_thumbnails.processors import scale_and_crop as easy_thumbnails_scale_and_crop
from toolkit.helpers import calc_scale_percents_size


def scale_percents_and_crop(im, size=None, crop=False, upscale=False, **kwargs):

    if size is None:
        size = im.size

    if 'size_percents' in kwargs:
        size_percents = kwargs.get('size_percents')
        size = calc_scale_percents_size(origin_size=im.size,
                                        size_percents=size_percents)

    return easy_thumbnails_scale_and_crop(im, size, crop, upscale, **kwargs)


