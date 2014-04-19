# -*- coding: utf-8 -*-
from .models import *
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy


class DiseditableAdminMixin(object):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return obj.__class__._meta.get_all_field_names()

    def get_actions(self, request):
        return ()


class FactAdmin(DiseditableAdminMixin, admin.ModelAdmin):

    def get_list_display_links(self, request, list_display):
        return ()

    def get_list_display(self, request):
        return self.model._meta.get_all_field_names()


class ActivateFactAdmin(FactAdmin):
    pass


class UsinglogFactAdmin(FactAdmin):
    pass


def lookup_allowed_datedim(lookup, value):
    fields = (
        'datevalue',
        'year',
        'month',
        'day',
        'dayofweek',
        'week',
        'day'
    )
    for f in fields:
        if f in lookup:
            return True
    return None


class SumActivateDeviceProductResultAdmin(DiseditableAdminMixin,
                                          admin.ModelAdmin):

    list_display = ('productkey', 'cycle_type',
                    'start_date', 'end_date',
                    'total_reserve_count',
                    'reserve_count',
                    'active_count',
                    'open_count')
    list_filter = (
        'productkey',
        'cycle_type',
    )

    def lookup_allowed(self, lookup, value):
        if lookup_allowed_datedim(lookup, value):
            return True
        return super(SumActivateDeviceProductResultAdmin, self)\
            .lookup_allowed(lookup, value)


#admin.site.register(ActivateFact, ActivateFactAdmin)
#admin.site.register(UsinglogFact, UsinglogFactAdmin)
admin.site.register(SumActivateDeviceProductResult,
                    SumActivateDeviceProductResultAdmin)
admin.site.register(SumActivateDeviceProductPackageResult,
                    SumActivateDeviceProductResultAdmin)
admin.site.register(SumActivateDeviceProductPackageVersionResult,
                    SumActivateDeviceProductResultAdmin)


class PackageDimAdmin(DiseditableAdminMixin,
                      admin.ModelAdmin):

    list_display = ('package_name', 'version_name',)
    ordering = ('package_name', 'version_name', )

    def title(self, obj):
        from warehouse.models import Package
        try:
            return Package.objects.get(package_name=obj.package_name).title
        except Package.DoesNotExist:
            return ''

    def _fetch_cache_package_version(self, obj):
        from warehouse.models import Package, PackageVersion
        if not hasattr(obj, '_package'):
            try:
                package = Package.objects.get(package_name=obj.package_name)
                obj._package = package
            except Package.DoesNotExist:
                pass
        if not hasattr(obj, '_version') \
            and getattr(obj, '_package')\
            and obj.version_name != UNDEFINED:
            try:
                version = obj._package.versions\
                    .filter(version_name=obj.version_name)
                obj._version = version
            except PackageVersion.DoesNotExist:
                pass
        return obj

    def package_link(self, obj):
        url = ''
        from warehouse.models import Package
        obj = self._fetch_cache_package_version(obj)
        if hasattr(obj, '_package') and getattr(obj, '_package'):
            url = reverse_lazy('admin:%s_%s_edit' %(Package._meta.app_label,
                                                     Package._meta.module_name),
                                pk=obj._package.pk)
        if url:
            return '<a href="%s" target="_blank">%s</a>' % (url, obj.package_name)
        else:
            return obj.package_name
    package_link.allow_tags = True
    package_link.admin_order_field = 'package_name'

    def version_link(self, obj):
        url = ''
        from warehouse.models import PackageVersion
        obj = self._fetch_cache_package_version(obj)
        if hasattr(obj, '_version') and getattr(obj, '_version'):
            return reverse_lazy('admin:%s_%s_edit' %(PackageVersion._meta.app_label,
                                                     PackageVersion._meta.module_name),
                                pk=obj._package.pk)
        if url:
            return '<a href="%s" target="_blank">%s</a>' % (url, obj.version_name)
        else:
            return obj.package_name
    version_link.allow_tags = True
    version_link.admin_order_field = 'version_name'


#admin.site.register(PackageDim, PackageDimAdmin)


class SumDownloadProductResultAdmin(DiseditableAdminMixin, admin.ModelAdmin):

    list_display = ('productkey', 'cycle_type',
                    'start_date', 'end_date',
                    'download_count',
                    'downloaded_count',
                    'total_download_count',
                    'total_downloaded_count'
    )

    list_filter = ('productkey', 'cycle_type')

    ordering = ('cycle_type', 'productkey', '-start_date')


admin.site.register(SumDownloadProductResult, SumDownloadProductResultAdmin)
