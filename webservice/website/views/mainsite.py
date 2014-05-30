# -*- coding: utf-8 -*-
import json
from mezzanine.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.contrib.auth import authenticate, login

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from website.response import WidgetHttpResponse, HttpResponse
from warehouse.models import PackageVersion, Package
from account.models import User


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

def login_view(request):
    template = 'login.html'
    context = {}
    if request.method == 'GET':
        return TemplateResponse(request=request, template=template, context=context)
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if request.is_ajax():
            resp = {"result": 0}
            if user:
                resp["result"] = 1
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            if user:
                return HttpResponseRedirect('/')
            return TemplateResponse(request=request, template=template, context=context)


def register_view(request):
    template = 'reg.html'
    context = {}
    if request.method == 'GET':
        return TemplateResponse(request=request, template=template, context=context)
    else:
        #print (request.POST)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password-confirm', None)
        email = request.POST.get('email', None)
        agreement = request.POST.get('agreement', None)

        if not (username and password and password_confirm and email and agreement) :
            return TemplateResponse(request=request, template=template, context=context)

        if password != password_confirm:
            return TemplateResponse(request=request, template=template, context=context)
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/')
