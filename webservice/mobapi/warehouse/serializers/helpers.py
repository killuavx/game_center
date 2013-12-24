# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def get_packageversion_download_url(version):
    try:
        return version.di_download.url
    except ValueError:
        pass
    try:
        return version.download.url
    except ValueError:
        pass

    return None


def get_packageversion_download_size(version):
    try:
        return version.di_download.size
    except ValueError:
        pass
    try:
        return version.download.size
    except ValueError:
        pass

    return 0


def get_packageversion_urls(request, versions):
    version_uris = [reverse('packageversion-detail', kwargs=dict(pk=version.pk)) for version in versions]
    if request:
        version_uris = \
            [request.build_absolute_uri(uri) for uri in version_uris]

    return version_uris


def get_versions_url(request, package):
    uri = "%s?package=%d" % (reverse('packageversion-list'), package.pk)
    if request:
        return request.build_absolute_uri(uri)
    return uri
