# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def get_url_for_taxonomy(request, obj, related_items, viewname, router=None):
    if related_items.count() > 0:
        reverse_viewname = router.get_base_name(viewname) if router else viewname
        path = reverse(reverse_viewname, kwargs=dict(slug=obj.slug))
        if request:
            return request.build_absolute_uri(path)
        return path
    return None