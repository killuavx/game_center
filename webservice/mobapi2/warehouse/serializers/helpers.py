# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def get_packageversion_download_url(request, version, **kwargs):
    try:
        data = dict()
        if kwargs.get('entrytype'):
            data['entrytype'] = kwargs.get('entrytype')
        if request:
            url = request.build_absolute_uri(version.get_download_url(**data))
        else:
            url = version.get_download_url(**data)
    except (AttributeError, ValueError):
        return '#'
    return url


def get_packageversion_download_size(version):
    return version.get_download_size()


def get_packageversion_urls(request, versions, router=None):
    view_name = router.get_base_name('packageversion-detail') if router else 'packageversion-detail'
    version_uris = [reverse(view_name, kwargs=dict(pk=version.pk)) for version in versions]
    if request:
        version_uris = \
            [request.build_absolute_uri(uri) for uri in version_uris]

    return version_uris


def get_versions_url(request, package, router=None):
    view_name = router.get_base_name('packageversion-list') if router else 'packageversion-list'
    uri = "%s?package=%d" % (reverse(view_name), package.pk)
    if request:
        return request.build_absolute_uri(uri)
    return uri


def get_packageversion_supported_languages(version):
    lang_desc_maps = dict(
        ZH='中文',
        EN='英文',
        _='其他'
    )
    lang_codes = version.supported_languages.values_list('code', flat=True)
    desc_langs = []
    if len(lang_codes):
        if 'ZH' in lang_codes:
            lang_codes.pop(lang_codes.index('ZH'))
            desc_langs.append(lang_desc_maps['ZH'])
        if 'EN' in lang_codes:
            lang_codes.pop(lang_codes.index('EN'))
            desc_langs.append(lang_desc_maps['EN'])
        if len(lang_codes):
            desc_langs.append(lang_desc_maps['_'])
    else:
        desc_langs.append(lang_desc_maps['_'])
    return ",".join(desc_langs)
