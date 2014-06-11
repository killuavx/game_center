# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils.timezone import is_aware, make_aware, UTC
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.timezone import now, get_default_timezone
from django.views.decorators.cache import cache_control
from taxonomy.models import Category
from website.views import base
from os.path import join

max_age = 3600

template404 = 'errors/web/404.html'

template_prefix = 'pages'


class NotFound(base.TemplateResponseNotFound):

    template = template404


@cache_control(public=True, max_age=max_age)
def package_detail(request, pk,
                   template_name=join(template_prefix, 'package/detail.haml'), *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.package_detail(request=request, pk=pk,
                               template_name=template_name,
                               template_not_found_class=NotFound,
                               product=ETS.web,
                               *args, **kwargs)


@cache_control(public=True, max_age=max_age)
def packageversion_detail(request, pk,
                          template_name=join(template_prefix, 'package/detail.haml'),
                          *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.packageversion_detail(request=request, pk=pk,
                                      template_name=template_name,
                                      template_not_found_class=NotFound,
                                      product=ETS.web,
                                      *args, **kwargs)


@cache_control(public=True, max_age=max_age)
def category_page(request, slug,
                  template_name=join(template_prefix, 'category/page.haml'),
                  *args, **kwargs):
    return base.category_page(request=request, slug=slug, template_name=template_name,
                              template_not_found_class=NotFound,
                              *args, **kwargs)


@cache_control(public=True, max_age=max_age)
def topic_detail(request, slug,
                 template_name=join(template_prefix, 'collections/page.haml'),
                 *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.topic_detail(request, slug, template_name=template_name,
                             product=ETS.web,
                             template_not_found_class=NotFound, *args, **kwargs)


@cache_control(public=True, max_age=max_age)
def search(request, template_name=join(template_prefix, 'category/search.haml'),
           *args, **kwargs):
    cat_slug = request.GET.get('cat', 'game')
    if cat_slug not in Category.ROOT_SLUGS:
        cat_slug = 'game'
    root_category = Category.objects.get(slug=cat_slug)

    cat_pk = request.GET.get('category')
    category = None
    if cat_pk:
        try:
            category = Category.objects.get(pk=cat_pk)
        except ObjectDoesNotExist:
            pass
    else:
        category = root_category

    return TemplateResponse(
        request=request,
        template=template_name,
        context=dict(
            root_category=root_category,
            category=category,
        )
    )


import qrcode
import hashlib
import qrcode.constants
from django.utils.encoding import force_bytes


def _hash_data(*args):
    m = hashlib.md5()
    [m.update(force_bytes(arg)) for arg in args]
    return m.hexdigest()

def _get_qrcode(*args):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
        )
    for arg in args:
        qr.add_data(arg)
    qr.make(fit=True)
    return qr.make_image()


def _qrcode_cdn_publish_one_and_get_image_url(relative_file, created=True):
    from website.cdn.processors.base import StaticProcessor
    from website.documents.cdn import SyncQueue

    if created and not SyncQueue.objects.filter(resource_path=relative_file).count():
        processor = StaticProcessor(content_type=StaticProcessor.CONTENT_TYPE_MEDIA,
                                    relative_path='qr')
        processor.publish_one(relative_file)

    is_published_ok = False
    try:
        sync_queue = SyncQueue.objects.filter(resource_path=relative_file).get()
        if sync_queue.latest_fb_result == 'SUCCESS':
            is_published_ok = True
    except:
        pass

    if created or is_published_ok:
        return '/%s/%s' % (StaticProcessor.CONTENT_TYPE_MEDIA, relative_file)

    return join(settings.MEDIA_URL, relative_file)


def _qrcode_get_or_save_file_to_relative_path(img, hash_qr):
    relative_file = join('qr', '%s.png' % hash_qr)
    qr_fp = join(settings.MEDIA_ROOT, relative_file)

    if os.path.isfile(qr_fp):
        return relative_file, False

    with open(qr_fp, 'wb') as f:
        img.save(f)

    return relative_file, True


@cache_control(public=True, max_age=86400)
def qrcode_gen(request, *args, **kwargs):
    url = request.GET.get('url')
    if url is None or not url.strip():
        return HttpResponse(content='404', status=404)

    hash_qr = _hash_data(url)
    img = _get_qrcode(url)
    relative_file, created = _qrcode_get_or_save_file_to_relative_path(img, hash_qr)
    image_url = _qrcode_cdn_publish_one_and_get_image_url(relative_file=relative_file)
    return redirect(to=image_url)


