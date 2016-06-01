# -*- coding: utf-8 -*-
from django.template.base import Library

register = Library()
@register.inclusion_tag('includes/pagination_web.haml', takes_context=True)
def pagination(context, current_page, *args, **kwargs):
    return dict(
        request=context.get('request'),
        current_page=current_page
    )

@register.inclusion_tag('includes/pagination_web_ajax.html', takes_context=True)
def pagination_ajax(context, current_page, load_selector='#list', *args, **kwargs):
    return dict(
        request=context.get('request'),
        load_selector=load_selector,
        paginator_url=kwargs.get('paginator_url'),
        current_page=current_page
    )

@register.inclusion_tag('pages/widgets/common/package-box.haml', takes_context=True)
def package_box(context, package, *args, **kwargs):
    return dict(
        request=context.get('request'),
        package=package,
        product='web',
    )

@register.inclusion_tag('pages/widgets/common/package-box-solr.haml', takes_context=True)
def package_box2(context, package, *args, **kwargs):
    return dict(
        request=context.get('request'),
        package=package,
        product='web',
        )
