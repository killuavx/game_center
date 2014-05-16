# -*- coding: utf-8 -*-
from django.contrib import admin
from reversion.admin import VersionAdmin
from warehouse.models import *
from crawler.models import IOSAppData, IOSBuyInfo
from toolkit.admin import admin_edit_linktag


def linktag(url, content, target='_blank'):
    return '<a href="%s" target="%s">%s</a>' % (url, target, content)


def download_linktag(iosapp_pk, text, help_text=''):
    mask = '<a title="%(tips)s" href="javascript:void(0);" onclick="down_iosapp_resource(this, %(id)s);">%(text)s</a>'
    return mask % {'id': iosapp_pk, 'text': text, 'tips': help_text}


def sync_to_version(iosapp_pk, text, help_text=''):
    mask = '<a title="%(tips)s" href="javascript:void(0);" onclick="sync_resources_to_version(this, %(id)s);">%(text)s</a>'
    return mask % {'id': iosapp_pk, 'text': text, 'tips': help_text }


def result_tags():
    return '<span class="result"><span>'


class MainAdmin(VersionAdmin):

    def get_list_display_links(self, request, list_display):
        return ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return obj.__class__._meta.get_all_field_names()

    def get_actions(self, request):
        return ()


class IOSBuyInfoInline(admin.TabularInline):
    model = IOSBuyInfo
    fields = ('account', 'buy_status', 'version', 'short_version', 'updated')
    readonly_fields = ('account', 'buy_status', 'version', 'short_version', 'updated',)
    ordering = ('created', )
    def has_delete_permission(self, request, obj=None):
        return False


class IOSAppDataAdmin(MainAdmin):
    model = IOSAppData
    inlines = [IOSBuyInfoInline, ]
    fieldsets = (
        (None, {
            'fields': (
                'appid',
                ('package_name', 'version_name',),
                ('mainclass', 'subclass',),
            )
        }),
        ('Process', {
            'fields': (
                ('is_analysised', 'analysised',),
                ('is_image_downloaded', 'image_downloaded',),
            )
        })

    )
    list_display = ('pk',
                    'title',
                    'package_link', 'version_link',
                    'is_analysised',
                    'is_image_downloaded',
                    'image_downloaded', 'status_description', 'buyinfo')
    list_display_links = ('pk',)
    ordering = ('id',)
    search_fields = ('package_name',)
    list_filter = ('is_analysised', 'is_image_downloaded',
                   'mainclass', 'subclass')
    date_hierarchy = 'analysised'

    def _fetch_cache_content_data(self, obj):
        if not hasattr(obj, '_content_data'):
            obj._content_data = obj.content_data
        return obj._content_data

    def title(self, obj):
        content_data = self._fetch_cache_content_data(obj)
        if not content_data:
            return content_data['trackName']
        view = linktag(content_data['trackViewUrl'], 'view')
        lookup = linktag(obj.lookup_url(obj.appid), 'lookup')
        return "ID: %s, [%s], Name: %s" % (
            obj.appid,
            " | ".join([view, lookup]),
            content_data['trackName'])
    title.allow_tags = True
    title.admin_order_field = 'appid'
    title.short_description = 'Track'

    def _fetch_cache_package_version(self, obj):
        if not hasattr(obj, '_package'):
            try:
                package = Package.objects.get(
                    package_name=obj.package_name)
                obj._package = package
            except Package.DoesNotExist:
                pass

            if obj.packageversion_id is not None \
                and obj.packageversion_id > 0:
                try:
                    version = obj.packageversion
                    obj.convert_normal_version(version)
                    obj._package = version.package
                    obj._version = version
                except ObjectDoesNotExist:
                    pass

        if not hasattr(obj, '_version') \
            and hasattr(obj, '_package'):
            try:
                version = obj._package.versions \
                    .filter(version_name=obj.version_name)
                obj._version = version
            except PackageVersion.DoesNotExist:
                pass
        return obj

    def package_link(self, obj):
        obj = self._fetch_cache_package_version(obj)
        if hasattr(obj, '_package') and getattr(obj, '_package'):
            admin_edit_linktag(obj._package, obj._package)
        else:
            return obj.package_name
    package_link.allow_tags = True
    package_link.admin_order_field = 'package_name'
    package_link.short_description = 'package name'

    def version_link(self, obj):
        obj = self._fetch_cache_package_version(obj)
        if hasattr(obj, '_version') and getattr(obj, '_version'):
            return admin_edit_linktag(obj._version, obj._version)
        else:
            return obj.version_name
    version_link.allow_tags = True
    version_link.admin_order_field = 'version_name'
    version_link.short_description = 'version name'

    def status_description(self, obj):
        if obj.packageversion_id == obj.ANALYSIS_PACKAGEVERSION_DUPLICATION:
            _status =  '重复数据'
        elif obj.packageversion_id == obj.ANALYSIS_PACKAGEVERSION_EMPTY:
            _status = '空数据'
        else:
            _status = 'app2ver completed'

        _action = ", ".join((
            download_linktag(obj.pk, 'down', help_text='下载图片'),
            sync_to_version(obj.pk, 'sync', help_text='同步图片至PackageVersion'),
            result_tags(),
        ))
        return "%s | %s" % (_action, _status)
    status_description.short_description = 'status'
    status_description.allow_tags = True

    def buyinfo(self, obj):
        if obj.iosbuyinfo_set.count():
            return True
        return False
    buyinfo.boolean = True

    class Media:
        #from django.conf import settings
        #static_url = getattr(settings, 'STATIC_URL', '/static')
        static_url = '/static/'
        js = [static_url+'js/custom/crawler.action.js', ]

admin.site.register(IOSAppData, IOSAppDataAdmin)

