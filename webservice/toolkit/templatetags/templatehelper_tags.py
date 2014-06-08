# -*- coding: utf-8 -*-
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
def settings_value(name, default=None):
    from mezzanine.conf import settings
    return getattr(settings, name, default)


@register.inclusion_tag('includes/breadcrumbs_package.haml')
def breadcrumbs_from(package, category,
                     product,
                     all_ancestors=False, *args, **kwargs):
    breadcrumb_insts = []
    try:
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
    except:
        pass
    package.bcname = package.title
    breadcrumb_insts.append(package)

    return dict(
        home_name=kwargs.get('home_name', '首页'),
        home_url=kwargs.get('home_url', '#'),
        product=product,
        breadcrumbs=breadcrumb_insts,
    )




@register.assignment_tag
def is_site_android():
    from toolkit import helpers
    site = helpers.get_global_site()
    return helpers.SITE_ANDROID == site.pk

@register.assignment_tag
def is_site_ios():
    from toolkit import helpers
    site = helpers.get_global_site()
    return helpers.SITE_IOS == site.pk
