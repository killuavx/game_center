# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline, GenericStackedInline
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from toolkit.models import Star, Resource


def admin_edit_url(object):
    return reverse('admin:%s_%s_change' %(object._meta.app_label,
                                          object._meta.module_name),
                   args=[object.id])


def admin_edit_linktag(object, content=None, target='_blank'):
    url = admin_edit_url(object)
    return '<a href="%s" target="%s">%s</a>' % (url, target, content or object)


class StarAdmin(admin.ModelAdmin):

    list_display = ('rating_date', 'content_title', 'content_stars_show', 'value', 'user')
    list_filter = ('content_type', )

    def content_stars_show(self, obj):
        content = obj.content_object
        return "[G:%d %0.2f%%, M:%d %0.2f%%, L:%d %0.2f%%] C:%d/ S:%d/ A:%0.2f" % (
            content.stars_good_count,
            content.stars_good_rate*100,
            content.stars_medium_count,
            content.stars_medium_rate*100,
            content.stars_low_count,
            content.stars_low_rate*100,
            content.stars_count,
            content.stars_sum,
            content.stars_average)

    def content_title(self, obj):
        content = obj.content_object
        try:
            return admin_edit_linktag(content, obj)
        except: pass
        return admin_edit_linktag(content)
    content_title.allow_tags = True
    content_title.short_description = _('Object Title')

#admin.site.register(Star, StarAdmin)


class ResourceInlines(GenericStackedInline):
    model = Resource
    ct_field = "content_type"
    ct_fk_field = "object_pk"
    fields = ('file', 'kind', 'alias', 'alt', 'file_size', 'file_md5', )
    ordering = ('kind', 'alias', )
    readonly_fields = ('file_size', 'file_md5')

