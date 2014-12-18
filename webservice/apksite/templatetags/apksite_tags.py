# -*- coding: utf-8 -*-
from django.template.base import Library
from django.core.urlresolvers import reverse

register = Library()
@register.inclusion_tag('apksite/includes/pagination_web.haml', takes_context=True)
def pagination(context, current_page, *args, **kwargs):
    return dict(
        request=context.get('request'),
        current_page=current_page
    )

@register.inclusion_tag('apksite/includes/pagination_web_ajax.html', takes_context=True)
def pagination_ajax(context, current_page, load_selector='#list', *args, **kwargs):
    return dict(
        request=context.get('request'),
        load_selector=load_selector,
        paginator_url=kwargs.get('paginator_url'),
        current_page=current_page
    )

@register.inclusion_tag('apksite/includes/package-box.haml', takes_context=True)
def package_box(context, package, *args, **kwargs):
    return dict(
        request=context.get('request'),
        package=package,
        product='web',
    )

def adv_content_url(adv, *args, **kwargs):
    if adv.get('content_type') == 'package':
        return reverse(viewname='package_detail', kwargs=dict(pk=adv.get('object_id')))
    else:
        return adv.get('content_url')

register.assignment_tag(adv_content_url, name='adv_content_url_as')
register.simple_tag(adv_content_url)


def package_url(pkg, *args, **kwargs):
    return reverse(viewname='package_detail_default',
                   kwargs=dict(
                       pk=pkg.get('id'),
                       package_name=pkg.get('package_name'),
                   ))
register.assignment_tag(package_url, name='package_url_as')
register.simple_tag(package_url)
