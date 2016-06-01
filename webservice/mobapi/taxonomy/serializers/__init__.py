# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def get_url_for_taxonomy(request, obj, related_items, reverse_viewname):
    if related_items.count() > 0:
        path = reverse(reverse_viewname, kwargs=dict(slug=obj.slug))
        if request:
            return request.build_absolute_uri(path)
        return path
    return None