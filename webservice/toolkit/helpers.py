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
from django.utils.timezone import make_aware, is_aware, get_default_timezone
from url_tools.helper import UrlHelper as _UrlHelper


class UrlHelper(_UrlHelper):

    def update_query_data(self, **kwargs):
        for key, val in kwargs.items():
            if not isinstance(val, str) and hasattr(val, '__iter__'):
                self.query_dict.setlist(key, val)
            else:
                self.query_dict[key] = val


def qurl_to(url, **kwargs):
    """
    Usage:
        >>> qurl_to('/news/2014/04/13', {'page':1})
        '/news/2014/04/13?page=1'

        >>> qurl_to('/news/2014/04/13?ref=other', {'ref':None})
        '/news/2014/04/13'

        >>> qurl_to('/news/2014/04/13', {'ids':[1,2,3]})
        '/news/2014/04/13?ids=1&ids=2&ids=3'
    """
    if not kwargs:
        return url

    _del_args = []
    _kwargs = dict()
    for k, v in kwargs.items():
        if v is None:
            _del_args.append(k)
        else:
            _kwargs[k] = v

    if _kwargs:
        u = UrlHelper(url)
        u.del_params(*_del_args)
        u.update_query_data(**_kwargs)
        url = u.get_full_path()
    return url


def released_hourly_datetime(dt, hourly=True):
    dt = dt if is_aware(dt) else make_aware(dt, get_default_timezone())
    if hourly:
        dt = dt.replace(minute=0, second=0, microsecond=0)
    return dt.astimezone()


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
    return " | ".join([refresh_link])
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


def language_codes_to_names(lang_codes):
    """
        根据language code列表，获取语言描述内容
    """
    lang_desc_maps = dict(
        ZH='中文',
        EN='英文',
        _='其他'
    )
    desc_langs = []
    if len(lang_codes):
        if 'ZH' in lang_codes:
            del lang_codes[lang_codes.index('ZH')]
            desc_langs.append(lang_desc_maps['ZH'])
        if 'EN' in lang_codes:
            del lang_codes[lang_codes.index('EN')]
            desc_langs.append(lang_desc_maps['EN'])
        if len(lang_codes):
            desc_langs.append(lang_desc_maps['_'])
    else:
        desc_langs.append(lang_desc_maps['_'])
    return desc_langs


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


def get_global_site(site_id=None):
    if site_id is None:
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


import random
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from os.path import join


def captcha(img_width=90, img_height=37, font_size=25):
    """
    background  #随机背景颜色
    line_color #随机干扰线颜色
    img_width = #画布宽度
    img_height = #画布高度
    font_color = #验证码字体颜色
    font_size = #验证码字体尺寸
    font = I#验证码字体
    """
    num = '2345678'
    string = 'ABCDEFHKLMNPQRSTUVWXYZ'
    background = (255, 255, 255)
    font_color = ['black','darkblue','darkred']
    fonts = [ImageFont.truetype(join(settings.FONT_DIRECTORY, 'Pointy.ttf'),font_size),
             ImageFont.truetype(join(settings.FONT_DIRECTORY, 'Pointy.ttf') ,font_size)]

    #新建画布
    im = Image.new('RGB',(img_width,img_height), background)
    draw = ImageDraw.Draw(im)
    #新建画笔
    draw = ImageDraw.Draw(im)

    #画干扰线
    #for i in range(random.randrange(6,8)):
    #    xy = (random.randrange(0,img_width),random.randrange(0,img_height),
    #          random.randrange(0,img_width),random.randrange(0,img_height))
    #    draw.line(xy,fill=line_color,width=1)

    #写入验证码文字
    code = random.sample(''.join([string, num, string.lower()]), 4)
    x = 2
    for i in code:
        y = random.randrange(0,10)
        draw.text((x,y), i, font=fonts[random.randrange(0,2)], fill=random.choice(font_color))
        x += 15

    verify = ''.join(code).upper()

    return im, verify


from mezzanine.conf import registry, register_setting as mz_register_setting


def register_setting(name="", label="", editable=False, description="",
                     default=None, choices=None, append=False, **kwargs):
    mz_register_setting(name=name, label=label,
                        editable=editable, description=description,
                        default=default, choices=choices, append=append)
    if 'widget' in kwargs:
        registry[name]['widget'] = kwargs.get('widget')



from django.utils.functional import SimpleLazyObject, empty


class LazyIter(SimpleLazyObject):

    def __iter__(self):
        if self._wrapped is empty:
            return iter(self._setup())
        rtn = iter(self._wrapped)
        self._wrapped = empty
        return rtn


