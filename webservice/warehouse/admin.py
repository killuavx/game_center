# -*- encoding=utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from django.utils.safestring import mark_safe
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from reversion.admin import VersionAdmin
from webservice.admin import AdminFieldBase, AdminField
from django.core.urlresolvers import reverse

class AdminIconField(AdminFieldBase):

    DEFAULT_FIELD = 'icon'

    @staticmethod
    def method(obj):
        try:
            return mark_safe('<img src="%s" />' % obj.url)
        except ValueError:
            return ''

class MainAdmin(VersionAdmin):
    pass

class PackageVersionScreenshotInlines(admin.StackedInline):

    model = PackageVersionScreenshot

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
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }

class PackageVersionAdmin(MainAdmin):
    model = PackageVersion
    inlines = (PackageVersionScreenshotInlines, )
    list_per_page = 15
    search_fields = ( 'version_name',
                      'package__package_name',
                      'package__title')
    list_display = ('show_icon', 'package', 'package_name',
                    'version_name', 'version_code', 'updated_datetime' )
    list_display_links = ('show_icon', 'version_name')
    actions = ['make_published' ]
    raw_id_fields = ('package', )
    fieldsets = (
        (_('Package'), {
            'fields':('package', )
        }),
        (_('File'), {
            'fields':('icon', 'download' )
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
    readonly_fields = ('package', 'created_datetime', 'updated_datetime',)
    ordering = ('-updated_datetime', '-version_code',)
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput},
    }

    show_icon = AdminIconField( allow_tags=True,
                                short_description=_('Icon') )
    def _package_link(p):
        link =  reverse('admin:%s_%s_change' % (p._meta.app_label, p._meta.module_name), args=[p.pk])
        return '<a href="%s" target="_blank">%s</a>' % (link, p.package_name )
    package_name = AdminField(name='package',
                              method=_package_link,
                              allow_tags=True,
                              short_description=_("Package Name"),
                              admin_order_field='package__package_name')

    def make_published(self, request, queryset):
        queryset.update(status=PackageVersion.STATUS.published)
    make_published.short_description = _('Make selected Packages as published')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PackageVersionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class PackageVersionInlines(admin.StackedInline):

    model = PackageVersion
    inlines = (PackageVersionScreenshotInlines, )

    classes = ('collapse', 'grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    fieldsets = (
        (None, {
            'fields':('icon', 'download' )
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
    readonly_fields = ( 'created_datetime', 'updated_datetime')
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
    inlines = (PackageVersionInlines, )
    list_per_page = 15

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
    def suit_row_attributes(self, obj, request):
        css_class = {
            'draft':'info',
            'published': 'success',
            'unpublished': 'warning',
            'reject':'error',
            }.get(obj.status)
        if css_class:
            return {'class': css_class, 'data': obj.package_name}

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
    def suit_row_attributes(self, obj, request):
        css_class = {
            'draft':'info',
            'activated': 'success',
            'unactivated': 'warning',
            'reject':'error',
            }.get(obj.status)
        if css_class:
            return {'class': css_class, 'data': obj.name}

admin.site.register(PackageVersion, PackageVersionAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Author, AuthorAdmin)

