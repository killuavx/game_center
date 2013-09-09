# -*- encoding=utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from warehouse.models import Package, Author, PackageScreenshot, PackageVersion
from django.utils.safestring import mark_safe
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from reversion.admin import VersionAdmin

class MainAdmin(VersionAdmin):
    pass

class PackageScreenshotInlines(admin.TabularInline):

    model = PackageScreenshot
    def show_thumbnail(self, obj):
        try:
            return mark_safe(
                '<img src="%s" alt="%s"/>' % \
                (thumbnail_url(obj.image, 'screenshot_thumbnail' ), obj.alt))
        except ValueError:
            return ''
    show_thumbnail.short_description = _('Thumbnail')
    show_thumbnail.allow_tags = True
    classes = ('collapse', 'grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)

class PackageVersionInlines(admin.StackedInline):
    model = PackageVersion
    classes = ('collapse', 'grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-open',)
    fieldsets = (
        (_('File'), {
            'fields':( 'icon', 'download')
        }),
        (_('Version'), {
            'fields':('version_code', 'version_name', 'whatsnew')
        }),
        (_('Status'), {
            'fields':('status',
                      'released_datetime',
                      'updated_datetime',
                      'created_datetime'
            )
        }),
    )
    extra = 0
    readonly_fields = ( 'released_datetime', 'created_datetime', 'updated_datetime')
    ordering = ('-version_code',)

    def show_thumbnail(self, obj):
        try:
            return mark_safe(
                '<img src="%s" alt="%s"/>' % \
                (thumbnail_url(obj.image, 'screenshot_thumbnail' ), obj.alt))
        except ValueError:
            return ''
    show_thumbnail.short_description = _('Thumbnail')
    show_thumbnail.allow_tags = True

class PackageAdmin(MainAdmin):
    model = Package
    list_per_page = 15

    inlines = (PackageVersionInlines, PackageScreenshotInlines, )
    fieldsets = (
        (_('Basic Information'), {
            'fields': ( 'title', 'package_name', 'author',
                        'summary', 'description',
            )
        }),
        (_('Taxonomy'), {
            'classes': ('collapse','grp-collapse grp-closed'),
            'fields': ('tags', 'categories')
        }),
        (_('Release'), {
            'classes': ('collapse','grp-collapse grp-open'),
            'fields': ( 'released_datetime', 'status',
                        'created_datetime', 'updated_datetime'
            )
        }),
    )
    search_fields = ( 'title', 'package_name', '^author__name')
    list_display = ( 'show_icon', 'title', 'package_name', 'tags', 'released_datetime', 'was_published_recently', 'status')
    list_filter = ('author__name', 'released_datetime', 'status' )
    list_display_links = ('package_name',)
    list_editable = ('status', 'tags',)
    date_hierarchy = 'released_datetime'
    ordering = ('-released_datetime',)
    list_select_related = True
    filter_horizontal = ('categories', )
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }

    def show_icon(self, obj):
        try:
            version = obj.versions.latest('version_code')
            return mark_safe('<img src="%s" alt="%s"/>' % (version.icon.url, obj.title))
        except ValueError:
            return ''
    show_icon.short_description = _('Icon')
    show_icon.allow_tags = True

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

