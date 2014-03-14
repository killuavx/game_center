# -*- coding: utf-8 -*-
import os
from os.path import join, isdir
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .errors import StaticContentTypeError


def relative_path_to_object_pk(abs_root_path, relative_path):
    # assert file/directory exists
    _abs_file_path = join(abs_root_path, relative_path)
    os.stat(_abs_file_path)

    # fill object_pk with root directory name
    object_pk = ''
    bits = relative_path.split(os.path.sep)
    if len(bits) > 1 or \
            (isdir(_abs_file_path) and len(bits) == 1):
        object_pk = bits[0]
    return object_pk


def publish_path_to_content_type(publish_path):
    if publish_path.startswith(settings.STATIC_URL):
        return 'static'
    if publish_path.startswith(settings.MEDIA_URL):
        return 'media'
    raise StaticContentTypeError

PUBLISH_URLS = {
    'static': settings.STATIC_URL,
    'media': settings.MEDIA_URL,
}


def publish_path_prefix(content_type='static'):
    try:
        return PUBLISH_URLS[content_type]
    except KeyError:
        raise StaticContentTypeError


def get_content_object(content_type, object_pk):
    if str(content_type).isnumeric() and str(object_pk).isnumeric():
        ct = ContentType.objects.get_for_id(int(content_type))
        return ct.get_object_for_this_type(pk=int(object_pk))
    else:
        return join(publish_path_prefix(content_type), str(object_pk))


def get_dict_by_content_object(obj):
    if isinstance(obj, str):
        return dict(content_type=publish_path_to_content_type(obj),
                    object_pk=relative_path_to_object_pk(obj))
    else:
        ct = ContentType.objects.get_for_model(obj.__class__)
        return dict(content_type=str(ct.pk), object_pk=str(obj.pk))