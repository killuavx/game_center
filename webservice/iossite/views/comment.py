# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from iossite.templatetags.iossite_comment_tags import comment_star_for, comment_star_thread
from iossite.views.base import is_ajax_request, previous_url, next_url, login_redirect
from iossite.forms import CommentWithStarForm
from django import forms


def initial_post_data_redirect_url(request, prefix):
    post_data = request.POST
    login_required_setting_name = prefix.upper() + "S_ACCOUNT_REQUIRED"
    posted_session_key = "unauthenticated_" + prefix
    redirect_url = ''
    if not request.user.is_authenticated():
        request.session[posted_session_key] = request.POST
        #error(request, '请登陆后再操作')
        redirect_url = "%s?next=%s" % (settings.LOGIN_URL, reverse(prefix))
    elif posted_session_key in request.session:
        post_data = request.session.pop(posted_session_key)

    if "referer" in post_data:
        redirect_url = post_data.get('referer')
    return post_data, redirect_url


def initial_data(get_data, post_data=None):
    if post_data is None:
        post_data = dict()

    if 'content_type' not in post_data and 'content_type' not in get_data:
        raise Http404

    data = None
    if 'content_type' in post_data:
        data = dict(id=post_data.get('object_pk'))
    else:
        data = dict(id=get_data.get('object_pk'))

    return data


def initial_validation(request, prefix):
    post_data, redirect_url = initial_post_data_redirect_url(request, prefix)
    obj = initial_data(request.GET, post_data)
    return dict(
        object=obj,
        post_data=post_data,
        redirect_url=redirect_url,
    )


def comment(request):
    data = dict(code=-1, msg='')
    initial = initial_validation(request, 'comment')
    target_object = initial['object']
    form = CommentWithStarForm(request=request, target_object=target_object,
                               data=initial['post_data'])
    if request.method == 'POST':
        if not request.user.is_authenticated():
            data['code'] = 2
            data['msg'] = '请先登陆后再评论'
            data['errors'] = []
        else:
            if not form.is_valid():
                data['code'], data['msg'] = 2, '评论失败'
                data['errors'] = form.errors
            else:
                try:
                    comment = form.save()
                    data['code'], data['msg'] = 0, '评论成功'
                except forms.ValidationError as e:
                    data['code'], data['msg'] = 1, e.messages[0]

    if is_ajax_request(request):
        _json_data = json.dumps(data)
        return HttpResponse(_json_data, 'application/json')
    else:
        return redirect(initial['redirect_url'])


def comment_list(request, template='iossite/comment/comment_list.html'):
    initial = initial_validation(request, 'comment')
    target_object = initial_data(request.GET)
    page = request.GET.get('page')
    page = int(page) if str(page).isnumeric() else 1
    if target_object and target_object.get('id'):
        form = CommentWithStarForm(request, target_object=target_object,
                                   data=initial['post_data'])
        context = {"obj": target_object, "posted_comment_form": form}
        response_context = comment_star_thread(
            context=context,
            obj=target_object,
            page=page,
        )
        return TemplateResponse(request, template=template,
                                context=response_context)
    else:
        raise Http404


def comment_form(request, template='iossite/comment/comment_form.html'):
    target_object = initial_data(request.GET)
    if target_object and target_object.get('id'):
        context = {"obj": target_object, "request": request}
        response_context = comment_star_for(
            context=context,
            obj=target_object
        )
        return TemplateResponse(request, template=template,
                                context=response_context)
    else:
        raise Http404


from comment.models import Comment


def comment_remove(request, pk, *args, **kwargs):
    data = dict()
    if not request.user.is_authenticated():
        data['code'] = 2
        data['msg'] = '请先登陆'
        data['errors'] = []
    elif not request.user.is_staff:
        data['code'] = 2
        data['msg'] = '非法操作'
        data['errors'] = []
    else:
        try:
            comment = Comment.objects.get(pk=pk)
            data['code'], data['msg'] = 0, '成功删除'
            comment.is_removed = True
            comment.save()
        except ObjectDoesNotExist:
            data['code'], data['msg'] = 1, '没有评论内容'

    if is_ajax_request(request):
        _json_data = json.dumps(data)
        return HttpResponse(_json_data, 'application/json')
    else:
        referer = request.META.get('HTTP_REFERER', None)
        return redirect(referer)

