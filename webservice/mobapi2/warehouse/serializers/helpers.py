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
    desc_langs = version.language_names
    return ",".join(desc_langs)


def get_packageversion_reported(version):
    try:
        pkgreport_field = version._meta._name_map['reported'][0]
        return {key: getattr(version, val[0] % 'reported')
                for key, val in pkgreport_field.added_fields.items()}
    except:
        return {}
