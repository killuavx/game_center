# -*- coding: utf-8 -*-
import json
from django.utils.datastructures import SortedDict
from django.core.urlresolvers import get_script_prefix
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.utils.cache import patch_cache_control
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import View, TemplateView
from apksite.forms import LoginForm, SignupForm, CaptchaVerifyForm
from apksite.utils import login as auth_login, logout as auth_logout, authenticate


def login_redirect(request):
    next = next_url(request) or ""
    return redirect(next)


def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.REQUEST.get("next", "")
    host = request.get_host()
    return next if next and is_safe_url(next, host=host) else None


def is_ajax_request(request):
    return request.is_ajax() or request.GET.get('is_ajax') or request.POST.get('is_ajax')


def previous_url(request):
    previous = request.META.get('HTTP_REFERER', '')
    host = request.get_host()
    return previous if previous and is_safe_url(previous, host=host) else None


@csrf_exempt
def login(request, template='apksite/accounts/login.html'):
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
            data = dict(code=1, msg='登陆失败', errors=SortedDict(form.errors))

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
    return redirect(next_url(request) or previous_url(request) or get_script_prefix())


@never_cache
def captcha(request):
    form = CaptchaVerifyForm(request)
    img = form.build_captcha()
    response = HttpResponse(mimetype="image/gif")
    img.save(response, "gif")
    return response


@csrf_exempt
def signup(request, template='apksite/accounts/signup.html'):
    form = SignupForm(request=request,
                      check_captcha=True,
                      data=request.POST or None)
    data = dict(code=-1, msg='')
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            data = dict(code=0,
                        msg='注册成功',
                        next=next_url(request))
        else:
            data = dict(code=1, msg='注册错误', errors=form.errors)

    if is_ajax_request(request):
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif data['code'] == 0:
        return login_redirect(request)

    context = {'form': form, 'title': '注册'}
    return render(request, template, context)


class UserAuthenticatedPanelView(View):

    template_prefix = 'apksite/accounts'
    template_name = 'user_panel.haml'

    @method_decorator(vary_on_cookie)
    def get(self, request):
        data = dict(
            title=None if request.user.is_anonymous() else request.user.username,
            panel=loader.render_to_string(template_name="%s/%s" %(self.template_prefix,
                                                                  self.template_name),
                                          context_instance=RequestContext(request,
                                                                          dict(request=request)
                                          )
            )
        )
        response = HttpResponse(content=json.dumps(data),
                                content_type='application/json')
        if request.user.is_anonymous():
            patch_cache_control(response, public=True)
        else:
            patch_cache_control(response, private=True)

        return response


authpanel = UserAuthenticatedPanelView.as_view()
