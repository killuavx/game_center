# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.template.base import Library

register = Library()


@register.assignment_tag
def queryset_filter(qs, **kwargs):
    return qs.filter(**kwargs)


@register.filter_function
def queryset_order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.assignment_tag
def settings_value(name):
    from mezzanine.conf import settings
    return getattr(settings, name, None)


@register.inclusion_tag('includes/breadcrumbs_package.haml')
def breadcrumbs_from(package, category,
                     product,
                     all_ancestors=False, *args, **kwargs):
    breadcrumb_insts = []
    if all_ancestors:
        for cat in category.get_ancestors(include_self=True):
            cat.bcname = cat.name
            breadcrumb_insts.append(cat)
    else:
        root = category.get_root()
        root.bcname = root.name
        breadcrumb_insts.append(root)
        category.bcname = category.name
        breadcrumb_insts.append(category)
    package.bcname = package.title
    breadcrumb_insts.append(package)

    return dict(
        home_name=kwargs.get('home_name', '首页'),
        home_url=kwargs.get('home_url', '#'),
        product=product,
        breadcrumbs=breadcrumb_insts,
    )


@register.inclusion_tag('includes/pagination_common.haml', takes_context=True)
def pagination(context, current_page, *args, **kwargs):
    return dict(
        request=context.get('request'),
        current_page=current_page
    )
