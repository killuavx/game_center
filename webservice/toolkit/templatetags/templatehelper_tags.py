# -*- coding: utf-8 -*-
from django.template.base import Library
from toolkit import helpers

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

@register.assignment_tag
def get_site_id():
    from toolkit import helpers
    site = helpers.get_global_site()
    if site:
        return site.pk
    return None

@register.assignment_tag
def get_site_name():
    site = helpers.get_global_site()
    if not site:
        return None
    if site.pk == helpers.SITE_IOS:
        return 'ios'
    elif site.pk == helpers.SITE_ANDROID:
        return 'android'
    else:
        return 'unknown'

@register.filter
def add_param(text, param):
    return "%s.%s" %(text, param)

from toolkit.cache_tagging_mixin import cache_locator

@register.simple_tag(takes_context=True)
def cache_location_register(context, *tags, **kwargs):
    url = context.get('request').build_absolute_uri()
    cache_locator.register(url, *tags, **kwargs)
    return ''

@register.assignment_tag
def mz_page_get(slug):
    from mezzanine.pages.models import Page
    try:
        return Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        return None


from django.conf import settings
from django.template.loader import get_template_from_string

@register.simple_tag(takes_context=True)
def template_string(context, text):
    template = get_template_from_string(text)
    try:
        output = template.render(context)
    except Exception as e:
        if settings.DEBUG:
            raise
        output = ''
    return output


def resource_field(inst, kind, field, alias='default'):
    try:
        res = getattr(inst.resources, kind)[alias]
        return getattr(res, field)
    except:
        pass
    return ""

register.assignment_tag(resource_field, name='resource_field_as')
register.simple_tag(resource_field)

from django.utils.timezone import now, datetime, get_default_timezone

@register.filter
def date_contains_nowdate(datestring):
    ds = datestring.split(",")
    n = now().astimezone().strftime("%Y-%m-%d")
    return n in ds

@register.simple_tag()
def site_logocss():
    n = now().astimezone().date()
    tz = get_default_timezone()
    def _logocss(s, e, path):
        if s <= n <= e:
            return """
            #cc-l .logo a{background:none}
            #cc-l .logo img{visibility:hidden}
            #cc-l .search{background:#fff}
            #cc-l .head .top{background:url(%(static_url)s%(logo_path)s) no-repeat}
            """ % dict(static_url=settings.STATIC_URL, logo_path=path)
        else:
            return None

    #/*12.24-12.25 共显示2天*/
    css = _logocss(datetime(2014, 12, 23, tzinfo=tz).date(),
                   datetime(2014, 12, 25, tzinfo=tz).date(),
                   path='android_web/img/logo-Christmas.png')
    if css:
        return css

    #/*12.31-1.3 共显示4天*/
    css = _logocss(datetime(2014, 12, 31, tzinfo=tz).date(),
                   datetime(2015, 1, 3, tzinfo=tz).date(),
                   path='android_web/img/logo-New-Year.png')
    if css:
        return css

    #/*2.17-2.24 共显示8天*/
    css = _logocss(datetime(2015, 2, 17, tzinfo=tz).date(),
                   datetime(2015, 2, 24, tzinfo=tz).date(),
                   path='android_web/img/logo-Chinese-New-Year.png')
    if css:
        return css
    return ""

