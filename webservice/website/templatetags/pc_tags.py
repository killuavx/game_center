# -*- coding: utf-8 -*-
from django.template.base import Library

register = Library()


def version_data(context, version, **kwargs):
    entrytype = None
    if 'entrytype' in kwargs:
        entrytype = kwargs.pop('entrytype')

    dw_url = version.get_download_url(entrytype=entrytype)
    if context.get('request'):
        dw_url = context['request'].build_absolute_uri(dw_url)

    return dict(
        package_name=version.package.package_name,
        version_name=version.version_name,
        download_url=dw_url,
    )

register.assignment_tag(version_data, takes_context=True, name='version_data_as')
register.simple_tag(version_data, takes_context=True)
