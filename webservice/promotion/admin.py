# -*- encoding: utf-8-*-
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from suit.admin import SortableTabularInline
from reversion.admin import VersionAdmin
from promotion.models import Place, Advertisement, Advertisement_Places

class AdvertisementAdmin(VersionAdmin):

    fieldsets = (
        (None, {
            'fields':(
                'title',
                'cover',
                'places',
            )
        }),
        (_('Content'), {
            'fields':(
                'content_type', 'object_id',
            )
        }),
        (_('Status'), {
            'fields':('status',
                      'released_datetime',
                      'updated_datetime',
                      'created_datetime'
            )
        }),
    )
    list_select_related = True
    list_display = ('show_cover', 'title', 'is_published',)
    list_display_links = ('show_cover', 'title', )
    readonly_fields = ('updated_datetime', 'created_datetime',)

    def show_cover(self, obj):
        try:
            return mark_safe('<img src="%s" alt="%s"/>' % \
                             (obj.cover.url, obj.title))
        except ValueError:
            return obj.name
    show_cover.short_description = _('Icon')
    show_cover.allow_tags = True

class AdvertisementInline(SortableTabularInline):
    sortable = 'ordering'
    model = Advertisement_Places
    extra = 0

class PlaceAdmin(VersionAdmin):
    list_display = ('slug', 'help_text')
    inlines = (AdvertisementInline, )

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Place, PlaceAdmin)
