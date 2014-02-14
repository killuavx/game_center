# -*- coding: utf-8 -*-
from mezzanine.conf import settings
from django.contrib.admin import site
from django.contrib.admin.sites import NotRegistered
from django.utils.translation import ugettext_lazy as _
from mezzanine.generic.admin import ThreadedCommentAdmin
from copy import deepcopy
from django.contrib.comments import get_model as get_comment_model
from toolkit.admin import admin_edit_linktag


class CommentAdmin(ThreadedCommentAdmin):

    list_display = ('object_title', 'content_type', ) + deepcopy(ThreadedCommentAdmin.list_display)
    search_fields = ('object_pk', ) + deepcopy(ThreadedCommentAdmin.search_fields)

    def object_title(self, obj):
        content = obj.content_object
        try:
            return admin_edit_linktag(content,
                                      ("%s[%s, %s]" %(content.package,
                                                      content.version_name,
                                                      content.version_code
                                      )))
        except: pass
        return admin_edit_linktag(content)
    object_title.allow_tags = True
    object_title.short_description = _('Object Title')

    def save_model(self, request, obj, form, change):
        if not obj.ip_address:
            obj.ip_address = request.get_client_ip()
        super(CommentAdmin, self).save_model(request, obj, form, change)


generic_comments = getattr(settings, "COMMENTS_APP", "") == "mezzanine.generic"
if generic_comments and not settings.COMMENTS_DISQUS_SHORTNAME:
    try:
        site.unregister(get_comment_model())
    except NotRegistered:
        pass
    site.register(get_comment_model(), CommentAdmin)



