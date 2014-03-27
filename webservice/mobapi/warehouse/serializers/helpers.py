# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from toolkit.helpers import get_client_event_data


def get_packageversion_download_url(request, version, **kwargs):
    try:
        if request:
            data = get_client_event_data(request)
            data.update(**kwargs)
            url = request.build_absolute_uri(version.get_download_url(**data))
        else:
            url = version.get_download_url(**kwargs)
    except (AttributeError, ValueError):
        return '#'
    return url


def get_packageversion_download_size(version):
    return version.get_download_size()


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
