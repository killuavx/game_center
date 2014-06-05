# -*- coding: utf-8 -*-
import json
from mezzanine.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.contrib.auth import authenticate, login, logout

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from website.response import WidgetHttpResponse, HttpResponse
from warehouse.models import PackageVersion, Package
from account.models import User
from website.models import captcha


def packageversion_detail(request, package_name, version_name=False,
                          template='pages/packages/version-detail.html',
                          *args, **kwargs):
    if version_name is False:
        try:
            package = Package.objects.published().get(package_name=package_name)
        except Package.DoesNotExist:
            raise Http404
        version = package.versions.latest_publish()
    else:
        try:
            version = PackageVersion.objects.published() \
                .get(package__package_name=package_name, version_name=version_name)
        except PackageVersion.DoesNotExist:
            raise Http404()
        package = version.package

    return TemplateResponse(request=request, template=template, context=dict(
        package=package,
        version=version,
        package_name=package_name,
        version_name=version_name,
        ))


def category_package_list(request, slug=settings.GC_CATEGORIES_DEFAULT_SLUG,
                          template='pages/categories.html', *args, **kwargs):
    context = dict(
        slug=slug,
        ordering=request.GET.get('ordering'),
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='CategoryPackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def masterpiece_view(request, template='pages/masterpiece.html', *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        response = WidgetHttpResponse(request=request,
                                      context=context,
                                      widget_name='MasterpiecePackageListWidget')
        return response

    return TemplateResponse(request=request, template=template, context=context)


def topics_view(request, template='pages/topics.html',
                *args, **kwargs):
    context = dict(
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsTopicListWidget')
            return response
        except Exception as e:
            raise Http404()
    return TemplateResponse(request=request, template=template, context=context)


def topic_package_list(request, slug, template='pages/topics/detail.html',
                       *args, **kwargs):
    context = dict(
        slug=slug,
        page_num=request.GET.get('page'),
        )
    if request.is_ajax() or request.GET.get('ajax'):
        try:
            response = WidgetHttpResponse(request=request,
                                          context=context,
                                          widget_name='TopicsPackageListWidget')
        except EmptyPage:
            raise Http404()
        return response

    return TemplateResponse(request=request, template=template, context=context)

def mainsite_view(request):
    template = 'mainsite.html'
    context = {}
    return TemplateResponse(request=request, template=template, context=context)

def ajax_login_view(request):
    resp = {"login": -1}

    if request.method == 'POST' and request.is_ajax():
        verify_code = request.POST.get('verify_code', None)
        if verify_code:
            verify_code = verify_code.upper()

        if verify_code != request.session['verify_code']:
            resp["login"] = -2
        else:
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                resp["login"] = 0

    return HttpResponse(json.dumps(resp), content_type="application/json")


def ajax_logout_view(request):
    resp = {"logout": -1}

    if request.method == 'POST' and request.is_ajax():
        logout(request)
        resp["logout"] = 0

    return HttpResponse(json.dumps(resp), content_type="application/json")


def check_username_exists(username=None):
    if not username:
        return None

    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return False

    return True


def check_email_exists(email=None):
    if not email:
        return None

    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return False

    return True


def check_register_username_view(request):
    resp = {'exists': 0}

    if request.method == 'POST' and request.is_ajax():
        username = request.POST.get('username', None)
        if username and check_username_exists(username):
            resp = {'exists': 1}

    return HttpResponse(json.dumps(resp), content_type="application/json")


def check_register_email_view(request):
    resp = {'exists': 0}

    if request.method == 'POST' and request.is_ajax():
        email = request.POST.get('email', None)
        if email and check_email_exists(email):
            resp = {'exists': 1}

    return HttpResponse(json.dumps(resp), content_type="application/json")


def register_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    template = 'reg.html'
    context = {}
    if request.method == 'GET':
        return TemplateResponse(request=request, template=template, context=context)
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password-confirm', None)
        email = request.POST.get('email', None)
        agreement = request.POST.get('agreement', None)
        verify_code = request.POST.get('verify_code', None)
        if verify_code:
            verify_code = verify_code.upper()
        if verify_code != request.session['verify_code']:
            return TemplateResponse(request=request, template=template, context=context)

        if not (username and password and password_confirm and email and agreement) :
            return TemplateResponse(request=request, template=template, context=context)

        if password != password_confirm:
            return TemplateResponse(request=request, template=template, context=context)

        if check_username_exists(username):
            return TemplateResponse(request=request, template=template, context=context)

        if check_email_exists(email):
            return TemplateResponse(request=request, template=template, context=context)

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        login(request, authenticate(username=username, password=password))
        return HttpResponseRedirect('/')


def reset_password_view(request):
    resp = {"reset": -1}
    if request.method == 'POST' and request.is_ajax():
        old_pass = request.POST.get('old_password', None)
        new_pass = request.POST.get('new_password', None)
        new_pass_conf =  request.POST.get('new_password_confirm', None)
        user = request.user
        if not user or not user.is_authenticated():
            resp = {"reset": -2}
        else:
            check_old_pass = user.check_password(old_pass)
            if not check_old_pass:
                resp = {"reset": -3}
            elif new_pass != new_pass_conf:
                resp = {"reset": -4}
            elif new_pass == old_pass:
                resp = {"reset": -5}
            else:
                user.set_password(new_pass)
                user.save()
                resp = {"reset": 0}

    return HttpResponse(json.dumps(resp), content_type="application/json")


def captcha_view(request):
    img, verify = captcha()
    request.session['verify_code'] = verify
    response = HttpResponse(mimetype="image/gif")
    img.save(response, "gif")
    return response
