# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from clientapp.models import ClientPackageVersion
from toolkit.helpers import sync_status_summary, sync_status_actions


class ClientPackageVersionAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'package_name',
                'version_code',
                'version_name',
            )
        }),
        (_('Files'), {
            'fields': (
                'icon',
                'cover',
                'download',
                'download_size',
            )
        }),
        (_('More Information'), {
            'fields': (
                'summary',
                'whatsnew',
                'memorandum',
                'download_count',
            )
        }),
        (_('Release'), {
            'fields': ('released_datetime',
                       'status',
                       'created_datetime',
                       'updated_datetime'
            )
        }),
    )
    readonly_fields = (
        'download_size',
        'download_count',
        'created_datetime',
        'updated_datetime',
    )
    list_editable = ('status',)
    list_display = ('show_icon',
                    'package_name',
                    'version_name',
                    'version_code',
                    'released_datetime',
                    'status',
                    'download_count',
                    'download_url',
                    'sync_file_status',
    )
    list_display_links = ('package_name', )

    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }

    def download_url(self, obj):
        try:
            a = '<a href="{url}" target="_blank">下载地址</a>'
            return a.format(url=obj.download.url)
        except:
            pass
        return None

    download_url.short_description = _('download url')
    download_url.allow_tags = True

    def show_icon(self, obj):
        try:
            return mark_safe(
                '<img src="%s" alt="%s"/>' % (obj.icon.url, obj.summary))
        except ValueError:
            return ''

    show_icon.short_description = _('Icon')
    show_icon.allow_tags = True

    def sync_file_status(self, obj):
        return sync_status_summary(obj) + " | " + sync_status_actions(obj)
    sync_file_status.short_description = _('Sync Status')
    sync_file_status.allow_tags = True

    class Media:
        static_url = '/static/'
        js = [static_url+'js/syncfile.action.js', ]

admin.site.register(ClientPackageVersion, ClientPackageVersionAdmin)
