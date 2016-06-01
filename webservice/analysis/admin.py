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

class BaseSumActivateDeviceProductResultAdmin(DiseditableAdminMixin,
                                       admin.ModelAdmin):

    list_display = [
                    'cycle_type',
                    'start_date', 'end_date',
                    'total_reserve_count',
                    'reserve_count',
                    'active_count',
                    'open_count']
    list_filter = [
        'cycle_type',
    ]

    def get_list_display(self, request):
        list_display = list(self.list_display)
        if 'pk' not in list_display:
            list_display.insert(0, 'pk')
        return list_display


def factory_sum_activate_result_admin(model, base_admin=BaseSumActivateDeviceProductResultAdmin):
    sorted_fields = [
        'device_platform',
        'productkey',
        'product',
        'packagekey',
        'package',
    ]
    fields_to_insert = list(set(sorted_fields).intersection(set(model._sum_field_names)))
    fields_to_insert = sorted(fields_to_insert, key=lambda x:sorted_fields.index(x))

    flag_field_name = model._flag_field_name
    base_name = "".join([name.capitalize() \
                         for name in flag_field_name.lstrip('is_new_').split('_')])
    class_name = "SumActivateDevice%sResultAdmin" % base_name
    class_attrs = {
        '__module__': base_admin.__module__,
    }
    new_admin = type(base_admin)(class_name, (base_admin,), class_attrs)

    list_filter = list(new_admin.list_filter)
    list_display = list(new_admin.list_display)
    for i, f in enumerate(fields_to_insert):
        if f not in list_display:
            list_display.insert(i, f)
        if f not in list_filter:
            list_filter.insert(i, f)
    new_admin.list_filter = list_filter
    new_admin.list_display = list_display
    return new_admin


def factory_register_admin(model, base_admin=BaseSumActivateDeviceProductResultAdmin):
    result_admin = factory_sum_activate_result_admin(model, base_admin=base_admin)
    admin.site.register(model, result_admin)

factory_register_admin(SumActivateDeviceProductResult)
factory_register_admin(SumActivateDeviceProductPackageResult)
factory_register_admin(SumActivateDeviceProductPackageVersionResult)
factory_register_admin(SumActivateDeviceProductChannelResult)
factory_register_admin(SumActivateDeviceProductChannelPackageResult)
factory_register_admin(SumActivateDeviceProductChannelPackageVersionResult)


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
