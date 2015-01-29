# -*- coding: utf-8 -*-
from django.template.base import Library
from django.core.urlresolvers import reverse
from apksite.forms import CommentWithStarForm

register = Library()

CONTENT_TYPE = 'warehouse.packageversion'

CONTENT_TYPE_ID = 17


def get_content_object(obj, content_type):
    if not isinstance(obj, int):
        return obj
    return dict(id=obj)


@register.inclusion_tag("apksite/comment/comment_form.html", takes_context=True)
def comment_star_for(context, obj, content_type=None):
    obj = get_content_object(obj, content_type)
    form = CommentWithStarForm(request=context["request"], target_object=obj)
    try:
        context["posted_comment_form"]
    except KeyError:
        context["posted_comment_form"] = form
    context["unposted_comment_form"] = form
    context["comment_star_form"] = form
    context["comment_url"] = reverse("comment")
    context["object_for_comments"] = context["star_object"] = context["star_obj"] = obj

    ratings = context["request"].COOKIES.get("comment-star", "")
    star_string = "%s.%s" % (CONTENT_TYPE, obj.get('id'))
    context["stared"] = (star_string in ratings)
    return context

@register.inclusion_tag("apksite/comment/comment_form_fields.html", takes_context=True)
def comment_fields_for(context, form):
    context["form_for_fields"] = form
    return context


def comment_list_url(obj, content_type=None, view_name='comment_list'):
    qstr = "?content_type=%s&object_pk=%s" % (content_type, obj)
    return reverse(view_name) + qstr
register.simple_tag(comment_list_url)
register.assignment_tag(comment_list_url, name='comment_list_url_as')


@register.simple_tag()
def comment_star_form_url_for(obj, content_type, view_name='comment_form'):
    qstr = "?content_type=%s&object_pk=%s" % (content_type, obj)
    return reverse(view_name) + qstr

DEFAULT_PER_PAGE = 10


from apksite.apis import ApiFactory, ApiResponseException, ApiListPaginator, ApiListResultSet
from apksite.views.base import  pageobj_with_visible_range



def _request_comment_page(obj, content_type=CONTENT_TYPE_ID, page=1, per_page=DEFAULT_PER_PAGE):
    api = ApiFactory.factory('comment.list')
    resultset = ApiListResultSet(api, api.name, dict(
        content_type=content_type,
        object_pk=obj.get('id'),
        page=page
    ))
    paginator = ApiListPaginator(object_list=resultset, per_page=per_page)
    page_obj = paginator.page(page)
    return page_obj, paginator


@register.inclusion_tag("generic/web/includes/comment.html", takes_context=True)
def comment_star_thread(context, obj, page=1,
                        per_page=DEFAULT_PER_PAGE,
                        with_paginator=True,
                        max_paging_links=10,
                        load_selector='#comment-list',
                        *args, **kwargs):

    page_obj, paginator = _request_comment_page(obj, content_type=CONTENT_TYPE_ID,
                                                page=page,
                                                per_page=per_page)
    if with_paginator:
        context['comments_page'] = pageobj_with_visible_range(page_obj=page_obj,
                                                              max_paging_links=max_paging_links)
    else:
        context['comments_page'] = page_obj
    context['comments'] = context['comments_page']
    object_id = obj.get('id')
    context["comment_list_url"] = comment_list_url(obj=object_id,
                                                   content_type=CONTENT_TYPE_ID)
    context.update({
        "comments_for_thread": [],
        "no_comments": paginator.count == 0,
        'with_paginator': with_paginator,
        'comments_load_selector': load_selector,
    })
    return context
