# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from clientapp.models import ClientPackageVersion, LoadingCover, CLIENT_PACKAGEVERSION_DIRECTORY_PREFIX
from toolkit.helpers import sync_status_summary, sync_status_actions
from toolkit.admin import admin_edit_linktag, ResourceInlines as BaseResourceInlines
from django import forms


class ResourceForm(forms.ModelForm):

    class Meta:
        model = BaseResourceInlines.model


class ResourceInlines(BaseResourceInlines):

    form = ResourceForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'alias' and self.parent_model is ClientPackageVersion:
            return super(BaseResourceInlines, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'file':
            db_field.directory = CLIENT_PACKAGEVERSION_DIRECTORY_PREFIX
        return super(ResourceInlines, self).formfield_for_dbfield(db_field, **kwargs)


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
                'workspace',
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

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if not str(obj.workspace):
            return readonly_fields
        if obj and obj.pk:
            return readonly_fields + ['workspace', ]
        return readonly_fields

    inlines = (ResourceInlines, )


class LoadingCoverAdmin(VersionAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'image',
                ('package_name', 'version',),
                ('publish_date', 'expiry_date'),
                'status',
            )
        }),
    )

    list_display = ('pk', 'show_image', 'title', 'clientapp', 'status', 'publish_date_since',
                    '_order', 'sync_file_status',)
    list_editable = ('status', '_order',)
    list_filter = ('status',)

    def show_image(self, obj):
        try:
            return mark_safe('<a href="%s" target="_blank">'
                             '<img width="100" src="%s" alt="%s"/></a>' % \
                             (obj.image.url, obj.image.url, obj.title))
        except ValueError:
            return obj.name
    show_image.short_description = _('Image')
    show_image.allow_tags = True

    def clientapp(self, obj):
        if obj.version:
            return admin_edit_linktag(obj.version)
        return obj.package_name
    clientapp.short_description = 'Client App'
    clientapp.allow_tags = True


    def get_action(self, action):
        return ()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return ('package_name', 'version')
        return ()

    def sync_file_status(self, obj):
        return sync_status_summary(obj) + " | " + sync_status_actions(obj)
    sync_file_status.short_description = _('Sync Status')
    sync_file_status.allow_tags = True

    class Media:
        static_url = '/static/'
        js = [static_url+'js/syncfile.action.js', ]

admin.site.register(ClientPackageVersion, ClientPackageVersionAdmin)
admin.site.register(LoadingCover, LoadingCoverAdmin)
