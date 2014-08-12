# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
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

from toolkit.helpers import get_global_site
from website.models import TopicProxy


@cache_control(public=True, max_age=max_age)
def topic_detail(request, slug,
                 template_name=join(template_prefix, 'collections/page.haml'),
                 template_not_found_class=NotFound,
                 *args, **kwargs):
    try:
        topic = TopicProxy.objects.get_cache_by_slug(get_global_site().pk,
                                                     slug=slug)
        if not topic or not topic.is_published():
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return template_not_found_class(request)

    ETS = settings.ENTRY_TYPES()
    return TemplateResponse(
        request=request, template=template_name,
        context=dict(
            topic=topic,
            product=ETS.web,
            )
    )


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


def _get_qrcode(*args, **kwargs):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=kwargs.get('box_size', 3),
        border=kwargs.get('border', 1),
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


def _qrcode_get_or_save_file_to_relative_path(gen_img_func, hash_qr):
    relative_file = join('qr', '%s.png' % hash_qr)
    qr_fp = join(settings.MEDIA_ROOT, relative_file)

    if os.path.isfile(qr_fp):
        return relative_file, False

    with open(qr_fp, 'wb') as f:
        img = gen_img_func()
        img.save(f)

    return relative_file, True


@cache_control(public=True, max_age=86400)
def qrcode_gen(request, *args, **kwargs):
    url = request.GET.get('url')
    if url is None or not url.strip():
        return HttpResponse(content='404', status=404)

    hash_qr = _hash_data(url)
    style = request.GET.get('s')
    if not style:
        gen_img = lambda: _get_qrcode(url)
    else:
        gen_img = lambda: _get_qrcode(url, box_size=4, border=2)

    relative_file, created = _qrcode_get_or_save_file_to_relative_path(gen_img, hash_qr)
    image_url = _qrcode_cdn_publish_one_and_get_image_url(relative_file=relative_file)
    return redirect(to=image_url)


from django.contrib.messages import info, error
from website.web.forms import LoginForm, CaptchaVerifyForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import NoReverseMatch, get_script_prefix, reverse
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from mezzanine.utils.views import render
from mezzanine.utils.urls import login_redirect, next_url
from account import authenticate
import json


def is_ajax_request(request):
    return request.is_ajax() or request.GET.get('is_ajax') or request.POST.get('is_ajax')


def previous_url(request):
    previous = request.META.get('HTTP_REFERER', '')
    host = request.get_host()
    return previous if previous and is_safe_url(previous, host=host) else None

@csrf_exempt
def login(request, template='accounts/web/account_login.html'):
    form = LoginForm(request=request,
                     check_captcha=True,
                     data=request.POST or None)
    data = dict(code=-1, msg='')
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            data = dict(code=0, msg='登陆成功', next=next_url(request))
        else:
            data = dict(code=1, msg='登陆失败', errors=form.errors)

    if is_ajax_request(request):
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif data['code'] == 0:
        return login_redirect(request)

    context = {"form": form, "title": "登陆"}
    return render(request, template, context)


def logout(request):
    auth_logout(request)
    msg = '登出成功'
    if is_ajax_request(request):
        data = dict(code=0, msg=msg)
        return HttpResponse(json.dumps(data), content_type='application/json')
    info(request, msg)
    return redirect(next_url(request) or previous_url(request) or get_script_prefix())


@never_cache
def captcha(request):
    form = CaptchaVerifyForm(request)
    img = form.build_captcha()
    response = HttpResponse(mimetype="image/gif")
    img.save(response, "gif")
    return response


@csrf_exempt
def signup(request, template='accounts/web/account_signup.html'):
    form = SignupForm(request=request,
                      check_captcha=True,
                      data=request.POST or None)
    data = dict(code=-1, msg='')
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, check_password=False)
            auth_login(request, user)
            data = dict(code=0,
                        msg='注册成功',
                        next=next_url(request))
        else:
            data = dict(code=1, msg='注册错误', errors=form.errors)

    if is_ajax_request(request):
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif data['code'] == 0:
        info(request, data['msg'])
        return login_redirect(request)

    context = {'form': form, 'title': '注册'}
    return render(request, template, context)

from mezzanine.conf import settings as mz_settings
from toolkit.forms import CommentWithStarForm
from toolkit.templatetags.comment_star_tags import comment_star_thread
from django.db.models import get_model
from django.contrib.contenttypes.models import ContentType


def initial_post_data_redirect_url(request, prefix):
    mz_settings.use_editable()
    post_data = request.POST
    login_required_setting_name = prefix.upper() + "S_ACCOUNT_REQUIRED"
    posted_session_key = "unauthenticated_" + prefix
    redirect_url = ''
    if getattr(mz_settings, login_required_setting_name, False):
        if not request.user.is_authenticated():
            request.session[posted_session_key] = request.POST
            error(request, '请登陆后再操作')
            redirect_url = "%s?next=%s" % (mz_settings.LOGIN_URL, reverse(prefix))
        elif posted_session_key in request.session:
            post_data = request.session.pop(posted_session_key)
    if "referer" in post_data:
        redirect_url = post_data.get('referer')
    return post_data, redirect_url


def initial_model_object(get_data, post_data=None):
    if post_data is None:
        post_data = dict()
    model = obj = None

    if 'content_type' not in post_data and 'content_type' not in get_data:
        raise Http404

    if 'content_type' in post_data:
        try:
            model = get_model(*post_data.get("content_type", "").split(".", 1))
            if model:
                obj = model.objects.get(id=post_data.get("object_pk", None))
                return model, obj
            return model, model()
        except (TypeError, ObjectDoesNotExist):
            pass
        if model:
            return model, model()
        else:
            raise Http404

    else:
        ct_id = get_data.get('content_type')
        try:
            ct = ContentType.objects.get_for_id(ct_id)
        except ObjectDoesNotExist:
            raise Http404

        model = ct.model_class()
        obj_id = get_data.get('object_pk')
        if obj_id:
            try:
                obj = ct.get_object_for_this_type(id=obj_id)
            except ObjectDoesNotExist:
                obj = model()
        return model, obj


def initial_validation(request, prefix):
    post_data, redirect_url = initial_post_data_redirect_url(request, prefix)
    model, obj = initial_model_object(request.GET, post_data)
    return dict(
        model=model,
        object=obj,
        post_data=post_data,
        redirect_url=redirect_url,
    )


def comment(request):
    initial = initial_validation(request, 'comment')
    target_object = initial['object']
    form = CommentWithStarForm(request, target_object,
                               data=initial['post_data'])
    data = dict(code=-1, msg='')
    if request.method == 'POST':
        if not request.user.is_authenticated():
            data['code'] = 2
            data['msg'] = '请先登陆后再评论'
            data['errors'] = []
        if form.is_valid():
            comment = form.save(request)
            data['code'], data['msg'] = 0, '评论成功'
        else:
            data['code'], data['msg'] = 1, '评论失败'
            data['errors'] = form.errors

    if is_ajax_request(request):
        _json_data = json.dumps(data)
        return HttpResponse(_json_data, 'application/json')
    else:
        error(request, data['msg'])
        return redirect(initial['redirect_url'])


def comment_list(request, template='generic/web/includes/comment.html'):
    initial = initial_validation(request, 'comment')
    model, target_object = initial_model_object(request.GET)
    if target_object and target_object.pk:
        form = CommentWithStarForm(request, target_object,
                                   data=initial['post_data'])
        context = {"obj": target_object, "posted_comment_form": form}
        response_context = comment_star_thread(
            context=context,
            parent=target_object,
            page=request.GET.get('page', 1)
        )
        return TemplateResponse(request, template=template,
                                context=response_context)
    else:
        raise Http404
