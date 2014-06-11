# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
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


from toolkit.helpers import captcha as build_captcha
from django.contrib.messages import info, error
from website.web.forms import LoginCaptchaForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import NoReverseMatch, get_script_prefix, reverse
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from mezzanine.utils.views import render
from mezzanine.utils.urls import login_redirect, next_url
from mezzanine.accounts import views as account_views
import json


def previous_url(request):
    previous = request.META.get('HTTP_REFERER', '')
    host = request.get_host()
    return previous if previous and is_safe_url(previous, host=host) else None


def login(request, template='accounts/web/account_login_form.html'):
    form = LoginCaptchaForm(request=request,
                            check_captcha=True,
                            data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            data = dict(code=0, msg='登陆成功')
        else:
            data = dict(code=1, msg='登陆失败', errors=form.errors)

        if request.is_ajax() or request.DATA.get('is_ajax'):
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif data['code'] == 0:
            info(request, data['msg'])
            return login_redirect(request)
    else:
        if request.is_ajax() or request.DATA.get('is_ajax'):
            data = dict()
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            context = {"form": form, "title": "登陆"}
            return render(request, template, context)


def logout(request):
    auth_logout(request)
    msg = '登出成功'
    if request.is_ajax() or request.GET.get('is_ajax'):
        data = dict(code=0, msg=msg)
        return HttpResponse(json.dumps(data), content_type='application/json')
    info(request, msg)
    return redirect(next_url(request) or previous_url(request) or get_script_prefix())


@never_cache
def captcha(request):
    captcha_key = 'captcha_verify'
    img, request.session[captcha_key] = build_captcha()
    response = HttpResponse(mimetype="image/gif")
    img.save(response, "gif")
    return response


def signup(request, template='accounts/web/account_signup.html'):
    pass
