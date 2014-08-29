# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate
from django.template.base import Library
from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from warehouse.models import PackageVersion
from toolkit.forms import CommentWithStarForm
from django.db import models


DEFAULT_PER_PAGE = 10

register = Library()

def content_object_id(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.id, obj.pk


def comment_list_url(obj, content_type=None, view_name='comment_list'):
    obj = get_content_object(obj, content_type)
    qstr = "?content_type=%s&object_pk=%s" % content_object_id(obj)
    return reverse(view_name) + qstr

register.simple_tag(comment_list_url)


@register.simple_tag()
def comment_star_form_url_for(obj, content_type, view_name='comment_form'):
    obj = get_content_object(obj, content_type)
    qstr = "?content_type=%s&object_pk=%s" % content_object_id(obj)
    return reverse(view_name) + qstr


@register.inclusion_tag("generic/web/includes/comment.html", takes_context=True)
def comment_star_thread(context, parent, page=1,
                        per_page=DEFAULT_PER_PAGE,
                        with_paginator=True,
                        max_paging_links=10,
                        load_selector='#comment-list',
                        *args, **kwargs):

    if "all_comments" not in context:
        if "request" in context and context["request"].user.is_staff:
            comments_queryset = parent.comments.all()
        else:
            comments_queryset = parent.comments.visible()

        all_comments_queryset = comments_queryset.select_related("user")
        context["all_comments"] = all_comments_queryset
        comments_no_reply = all_comments_queryset.filter(replied_to=None)

        if with_paginator:
            context['comments_page'] = paginate(comments_no_reply,
                                                page_num=page,
                                                per_page=per_page,
                                                max_paging_links=max_paging_links)
        else:
            context['comments_page'] = None
        context['comments'] = context['comments_page']
    parent_id = parent.id if isinstance(parent, ThreadedComment) else None
    context["comment_list_url"] = comment_list_url(parent)
    try:
        replied_to = int(context["request"].POST["replied_to"])
    except KeyError:
        replied_to = 0
    context.update({
        "comments_for_thread": [],
        "no_comments": parent_id is None and not context["all_comments"],
        "replied_to": replied_to,
        'with_paginator': with_paginator,
        'comments_load_selector': load_selector,
    })
    return context


def get_content_object(obj, content_type=None):
    if not content_type:
        return obj

    if obj and isinstance(obj, int) \
        and content_type and isinstance(content_type, str):
        app_label, model = content_type.split('.')
        model_cls = models.get_model(app_label, model, only_installed=False)
        if hasattr(model_cls.objects, 'get_cache_by'):
            return model_cls.objects.get_cache_by(obj)
        else:
            return model_cls.objects.get(pk=obj)

    raise TypeError


@register.inclusion_tag("generic/web/includes/comments.html", takes_context=True)
def comment_star_for(context, obj, content_type=None):
    obj = get_content_object(obj, content_type)
    form = CommentWithStarForm(context["request"], obj)
    try:
        context["posted_comment_form"]
    except KeyError:
        context["posted_comment_form"] = form
    context["unposted_comment_form"] = form
    context["comment_star_form"] = form
    context["comment_url"] = reverse("comment")
    context["object_for_comments"] = context["star_object"] = context["star_obj"] = obj

    ratings = context["request"].COOKIES.get("comment-star", "")
    star_string = "%s.%s" % (obj._meta, obj.pk)
    context["stared"] = (star_string in ratings)
    star_name = obj.get_starsfield_name()
    for f in ("average", "count", "sum"):
        context["star_" + f] = getattr(obj, "%s_%s" % (star_name, f))
    return context


@register.inclusion_tag("generic/web/includes/comment_form_fields.html", takes_context=True)
def comment_fields_for(context, form):
    context["form_for_fields"] = form
    return context


@register.filter
def comment_content_star_value(comment):
    if not hasattr(comment, '_cache_content_star'):
        try:
            comment._cache_content_star = comment.content_star.all()[0]
        except IndexError:
            comment._cache_content_star = None

    if comment._cache_content_star:
        return comment._cache_content_star.value
    else:
        return 0


"""
-block extra_js_footer
  :javascript
    $(function(){
      $.ajax({
        url: '{% comment_star_form_url_for package.latest_version_id "warehouse.packageversion" %}',
        type:'text',
        success:function(text){
          $('#comment-panel').prepend(text);
        }
      });
      $.ajax({
        url:'{% comment_list_url package.latest_version_id "warehouse.packageversion" %}',
        type:'text',
        success:function(text){
          $('#comment-list').html(text);
        }
      });
    });
"""
