# -*- encoding: utf-8-*-
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from promotion.models import Place, Advertisement, Advertisement_Places
from toolkit.helpers import sync_status_summary, sync_status_actions
from toolkit.admin import ResourceInlines
from mezzanine.core.admin import (TabularDynamicInlineAdmin as TabularInline,
                                  StackedDynamicInlineAdmin as StackedInline)


class AdvertisementPlacesInline(TabularInline):
    model = Advertisement_Places
    fields = ('place', 'created_datetime', 'updated_datetime',)
    readonly_fields = ('created_datetime', 'updated_datetime',)
    #extra = 1


class AdvertisementAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'cover',
            )
        }),
        (_('Content'), {
            'fields': (
                ('content_type', 'object_id',),
                ('link', 'target', ),
            )
        }),
        (_('Status'), {
            'fields': ('status',
                       'released_datetime',
                       'updated_datetime',
                       'created_datetime'
            )
        }),
    )
    list_select_related = True
    list_display = ('show_cover',
                    'title',
                    'is_published',
                    'released_datetime',
                    'sync_file_status'
    )
    list_display_links = ('show_cover', 'title', )
    readonly_fields = ('updated_datetime', 'created_datetime',)
    inlines = (ResourceInlines, AdvertisementPlacesInline, )
    search_fields = ('title',)
    list_filter = ('content_type',
                   'places__slug',
                   'released_datetime',
                   'status')

    def get_readonly_fields(self, request, obj=None):
        fields = self.readonly_fields
        if obj and obj.pk:
            return fields + ('content_type', 'object_id')
        return fields

    def show_cover(self, obj):
        try:
            return mark_safe('<img src="%s" alt="%s"/>' % \
                             (obj.cover.url, obj.title))
        except ValueError:
            return obj.name

    show_cover.short_description = _('Icon')
    show_cover.allow_tags = True

    def sync_file_status(self, obj):
        return sync_status_summary(obj) + " | " + sync_status_actions(obj)
    sync_file_status.short_description = _('Sync Status')
    sync_file_status.allow_tags = True

    class Media:
        #from django.conf import settings
        #static_url = getattr(settings, 'STATIC_URL', '/static')
        static_url = '/static/'
        js = [static_url+'js/syncfile.action.js', ]


class AdvertisementPlacesOrderingInline(TabularInline):
    model = Advertisement_Places
    fields = ('advertisement', 'ordering',
              'created_datetime', 'updated_datetime',)
    ordering = ('-ordering', )
    readonly_fields = ('created_datetime', 'updated_datetime',)
    #extra = 1


class PlaceAdmin(VersionAdmin):
    list_display = ('slug', 'help_text')
    inlines = (AdvertisementPlacesOrderingInline, )


admin.site.register(Place, PlaceAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
