# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


def admin_edit_url(object):
    return reverse('admin:%s_%s_change' %(object._meta.app_label,
                                          object._meta.module_name),
                   args=[object.id])


def admin_edit_linktag(object, content=None, target='_blank'):
    url = admin_edit_url(object)
    return '<a href="%s" target="%s">%s</a>' % (url, target, content or object)


