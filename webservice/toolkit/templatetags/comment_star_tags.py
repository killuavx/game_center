# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate
from django.template.base import Library
from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from toolkit.forms import CommentWithStarForm


DEFAULT_PER_PAGE = 10

register = Library()

def content_object_id(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.id, obj.pk


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
    qstr = "?content_type=%s&object_pk=%s" % content_object_id(parent)
    context["comment_list_url"] = reverse("comment_list") + qstr
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

@register.inclusion_tag("generic/web/includes/comments.html", takes_context=True)
def comment_star_for(context, obj):
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

