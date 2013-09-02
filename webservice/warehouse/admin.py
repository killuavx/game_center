# -*- encoding=utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from warehouse.models import Package, Author

class MainAdmin(admin.ModelAdmin):
    pass

class PackageAdmin(MainAdmin):
    model = Package

    fieldsets = (
        (None, {
            'fields': ( 'title', 'package_name', 'author',
                        'summary', 'description',
            )
        }),
        (_('Taxonomy'), {
            'classes': ('collapse',),
            'fields': ('tags', 'categories')
        }),
        (_('Release'), {
            'classes': ('collapse',),
            'fields': ( 'released_datetime', 'status',
                        'created_datetime', 'updated_datetime'
            )
        }),
    )
    search_fields = ( 'title', 'package_name', '^author__name')
    list_display = ( 'title', 'package_name', 'tags', 'released_datetime', 'was_published_recently', 'status')
    list_filter = ('author__name', 'released_datetime', 'status' )
    list_display_links = ('package_name',)
    list_editable = ('status', 'tags',)
    date_hierarchy = 'released_datetime'
    ordering = ('-released_datetime',)
    list_select_related = True
    filter_horizontal = ('categories', )
    actions = ['make_published' ]

    def make_published(self, request, queryset):
        queryset.update(status=Package.STATUS.published)
    make_published.short_description = _('Make selected Packages as published')

    readonly_fields = ('created_datetime', 'updated_datetime',)


class PackageInline(admin.TabularInline):
    model = Package
    fields = ( 'title', 'package_name', 'released_datetime', 'status' )
    readonly_fields = ('title', 'package_name', 'released_datetime' )


class AuthorAdmin(MainAdmin):
    model = Author
    list_display = ( 'name', 'email', 'phone')
    search_fields = ( 'name', 'email', 'phone')
    list_filter = ('status', )
    ordering = ('name',)

    inlines = (PackageInline, )

admin.site.register(Package, PackageAdmin)
admin.site.register(Author, AuthorAdmin)
