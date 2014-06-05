# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from taxonomy.models import Category
from website.views import base
from os.path import join


template404 = 'pages/web/errors/404.html'

template_prefix = 'pages'


class NotFound(base.TemplateResponseNotFound):

    template = template404


def package_detail(request, pk,
                   template_name=join(template_prefix, 'package/detail.haml'), *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.package_detail(request=request, pk=pk,
                               template_name=template_name,
                               template_not_found_class=NotFound,
                               product=ETS.web,
                               *args, **kwargs)


def packageversion_detail(request, pk,
                          template_name=join(template_prefix, 'package/detail.haml'),
                          *args, **kwargs):
    ETS = settings.ENTRY_TYPES()
    return base.packageversion_detail(request=request, pk=pk,
                                      template_name=template_name,
                                      template_not_found_class=NotFound,
                                      product=ETS.web,
                                      *args, **kwargs)


def category_page(request, slug,
                  template_name=join(template_prefix, 'category/page.haml'),
                  *args, **kwargs):
    return base.category_page(request=request, slug=slug, template_name=template_name,
                              template_not_found_class=NotFound,
                              *args, **kwargs)


def topic_detail(request, slug,
                 template_name=join(template_prefix, 'collections/page.haml'),
                 *args, **kwargs):
    return base.topic_detail(request, slug, template_name=template_name,
                             template_not_found_class=NotFound, *args, **kwargs)


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

def _qrcode_cdn_publish_one(relative_file):
    from website.cdn.processors.base import StaticProcessor
    from website.documents.cdn import SyncQueue
    if not SyncQueue.objects.filter(resource_path=relative_file).count():
        processor = StaticProcessor(content_type=StaticProcessor.CONTENT_TYPE_MEDIA,
                                    relative_path='qr')
        processor.publish_one(relative_file)

    if settings.DEBUG:
        return '/%s/%s' % (StaticProcessor.CONTENT_TYPE_MEDIA, relative_file)

    return join(settings.MEDIA_URL, relative_file)

def qrcode_gen(request, *args, **kwargs):
    url = request.GET.get('url')
    if url is None or not url.strip():
        return HttpResponse(content='404', status=404)

    hash_qr = _hash_data(url)
    img = _get_qrcode(url)

    relative_file = join('qr', '%s.png' % hash_qr)
    qr_fp = join(settings.MEDIA_ROOT, relative_file)
    with open(qr_fp, 'wb') as f:
        img.save(f)

    image_url = _qrcode_cdn_publish_one(relative_file=relative_file)
    return redirect(to=image_url)


