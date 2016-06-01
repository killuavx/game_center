# -*- coding: utf-8 -*-
from django.template.base import Library

register = Library()


def version_data(context, version, **kwargs):
    entrytype = kwargs.pop('entrytype', None)
    is_dynamic = kwargs.pop('is_dynamic', False)
    try:
        if is_dynamic is False:
            entrytype = None
        dw_url = version.get_download_url(entrytype=entrytype,
                                          is_dynamic=is_dynamic)
    except Exception as e:
        dw_url = ''

    if dw_url and context.get('request'):
        dw_url = context['request'].build_absolute_uri(dw_url)

    package = version.package
    if package.is_ios:
        appid = package.as_ios.track_id
    else:
        appid = package.pk

    return dict(
        appid=appid,
        title=package.title,
        package_name=version.package.package_name,
        version_name=version.version_name,
        download_url=dw_url,
    )

register.assignment_tag(version_data, takes_context=True, name='version_data_as')
register.simple_tag(version_data, takes_context=True)


@register.inclusion_tag('includes/pagination_pc.haml', takes_context=True)
def pagination(context, current_page, *args, **kwargs):
    return dict(
        request=context.get('request'),
        current_page=current_page
    )
