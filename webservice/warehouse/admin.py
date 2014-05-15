# -*- encoding=utf-8 -*-
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from easy_thumbnails.widgets import ImageClearableFileInput as _ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from mezzanine.core.admin import (TabularDynamicInlineAdmin as TabularInline,
                                  StackedDynamicInlineAdmin as StackedInline)
from reversion.admin import VersionAdmin
from django.core.urlresolvers import reverse
from easy_thumbnails.exceptions import InvalidImageFormatError
from toolkit.helpers import sync_status_summary, sync_status_actions

from warehouse.models import Package, Author, PackageVersion, PackageVersionScreenshot
from warehouse.models import IOSPackage, IOSAuthor, IOSPackageVersion
from webservice.admin import AdminFieldBase, AdminField
from toolkit.admin import ResourceInlines


class ImageClearableFileInput(_ImageClearableFileInput):
    def render(self, name, value, attrs=None):
        try:
            return super(ImageClearableFileInput, self).render(
                name, value, attrs)
        except InvalidImageFormatError:
            pass

        try:
            return super(_ImageClearableFileInput, self).render(
                name, value, attrs)
        except InvalidImageFormatError:
            pass

        return super(_ImageClearableFileInput, self).render(
            name, None, attrs)


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
    extra = 4

    def get_fieldsets(self, request, obj=None):
        form = self.get_formset(request, obj).form
        fields = list(form.base_fields) + list(self.get_readonly_fields(request, obj))

        if isinstance(obj, IOSPackageVersion):
            return [(None, {'fields': fields})]
        try:
            iospackageversion = obj.iospackageversion
            return [(None, {'fields': fields})]
        except ObjectDoesNotExist:
            pass

        try:
            fields.pop(fields.index('kind'))
        except:
            pass
        return [(None, {'fields': fields})]

    def show_thumbnail(self, obj):
        try:
            return mark_safe(
                '<img src="%s" alt="%s"/>' % \
                (thumbnail_url(obj.image, 'screenshot_thumbnail'), obj.alt))
        except ValueError:
            return ''

    show_thumbnail.short_description = _('Thumbnail')
    show_thumbnail.allow_tags = True
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }


class PackageVersionAdmin(MainAdmin):
    model = PackageVersion
    inlines = (ResourceInlines,
               PackageVersionScreenshotInlines,
    )
    list_per_page = 15
    search_fields = ('version_name',
                     'package__package_name',
                     'package__title')
    list_display = ('show_icon',
                    'id',
                    'package',
                    'package_name',
                    'version_name',
                    'version_code',
                    'status',
                    'updated_datetime',
                    'is_data_integration',
                    'download_count',
                    'sync_file_action',
    )
    list_display_links = ('show_icon', 'version_name')
    actions = ['make_published']
    raw_id_fields = ('package', )
    fieldsets = (
        (_('Package'), {
            'fields': ('package', )
        }),
        (_('Version'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': (
                'subtitle',
                ('version_code', 'version_name',),
                'summary',
                'tags_text',
                'whatsnew',
                'description',
            )
        }),
        (_('File'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': (
                'icon', 'cover',
                ('download', 'download_size', 'download_md5'),
                ('di_download', 'di_download_size', 'di_download_md5'),
            )
        }),
        (_('Supported'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': (
                'supported_languages',
                'supported_devices',
                'supported_features',
            )
        }),
        (_('Version Statistics'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': (
                'download_count',
                ('stars_count', 'stars_sum', 'stars_average',),
                ('stars_good_rate', 'stars_good_count',),
                ('stars_medium_rate', 'stars_medium_count',),
                ('stars_low_rate', 'stars_low_count'),
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
    readonly_fields = ('created_datetime',
                       'updated_datetime',
                       'di_download_size',
                       'di_download_md5',
                       'download_size',
                       'download_md5',
                       'stars_count', 'stars_sum', 'stars_average',
                       'stars_good_rate', 'stars_good_count',
                       'stars_medium_rate', 'stars_medium_count',
                       'stars_low_rate', 'stars_low_count',
    )
    filter_horizontal = ("supported_languages",
                         "supported_devices",
                         "supported_features")
    list_filter = ('status',)
    date_hierarchy = 'released_datetime'
    ordering = ('-updated_datetime', '-version_code',)
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput},
    }

    show_icon = AdminIconField(allow_tags=True,
                               short_description=_('Icon'))

    def _check_packageversion_download_data_integration(self, version):
        try:
            url = version.di_download.url
            return True
        except (AttributeError, ValueError):
            return False

    def is_data_integration(self, obj):
        return self._check_packageversion_download_data_integration(obj)
    is_data_integration.short_description = _('is data integration download?')
    is_data_integration.boolean = True

    def _package_link(p):
        link = reverse(
            'admin:%s_%s_change' % (p._meta.app_label, p._meta.module_name),
            args=[p.pk])
        return '<a href="%s" target="_blank">%s</a>' % (link, p.package_name )

    package_name = AdminField(name='package',
                              method=_package_link,
                              allow_tags=True,
                              short_description=_("Package Name"),
                              admin_order_field='package__package_name')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('package', )

        return self.readonly_fields

    def make_published(self, request, queryset):
        queryset.update(status=PackageVersion.STATUS.published)
    make_published.short_description = _('Make selected Packages as published')

    def get_actions(self, request):
        actions = super(PackageVersionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def sync_file_action(self, obj):
        return sync_status_summary(obj) + " | " + sync_status_actions(obj)
    sync_file_action.allow_tags = True
    sync_file_action.short_description = _('Sync Status')

    def publish_path_check_links(self, obj):
        from django.conf import settings
        from os.path import basename
        def _model_file_publish_link(filefield, name):
            mask = """<a href="%s" target="_blank" title="%s">%s</a>"""
            default_base_url = filefield.storage.base_url
            filefield.storage.base_url = settings.PUBLISH_MEDIA_URL
            link = mask %(filefield.url, filefield.url, name)
            filefield.storage.base_url = default_base_url
            return link

        links = []
        links.append(_model_file_publish_link(obj.icon, 'icon'))
        if obj.download:
            download = _model_file_publish_link(obj.download, 'download')
            links.append(download)
        if obj.di_download:
            di_download = _model_file_publish_link(obj.download, 'di_download')
            links.append(di_download)
        screenshots = []
        for s in obj.screenshots.all():
            _s = _model_file_publish_link(s.image, basename(s.image.name))
            screenshots.append(_s)
        if screenshots:
            links.append("screenshots[%s%s%s]" % ("<br/>", ",<br/>".join(screenshots), "<br/>"))
        return "<br/>".join(links)
    sync_file_action.allow_tags = True
    publish_path_check_links.allow_tags = True
    publish_path_check_links.short_description = _('Sync Links')

    class Media:
        #from django.conf import settings
        #static_url = getattr(settings, 'STATIC_URL', '/static')
        static_url = '/static/'
        js = [static_url+'js/syncfile.action.js', ]


class PackageVersionInlines(admin.StackedInline):
    model = PackageVersion
    fieldsets = (
        (None, {
            'fields': (
                'subtitle',
                'summary',
                'tags_text',
                'description',
                'version_code', 'version_name',
                'whatsnew')
        }),
        (_('File'), {
            'fields': (
                       'icon', 'cover',
                       ('download', 'download_size', 'download_md5'),
                       ('di_download', 'di_download_size', 'di_download_md5'),
            )
        }),
        (_('Version Statistics'), {
            'fields': (
                'download_count',
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
    #extra = 1
    max_num = 100
    readonly_fields = ('created_datetime',
                       'updated_datetime',
                       'di_download_size',
                       'di_download_md5',
                       'download_size',
                       'download_md5',
    )
    ordering = ('-version_code',)

    def show_thumbnail(self, obj):
        try:
            return mark_safe(
                '<img src="%s" alt="%s"/>' % \
                (thumbnail_url(obj.image, 'screenshot_thumbnail'), obj.alt))
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
            'classes': ('suit-tab suit-tab-general', ),
            'fields': (
                'title',
                'package_name',
                'author',
                'summary',
                'description',
            )
        }),
        (_('Package Statistics'), {
            'classes': ('suit-tab suit-tab-statistics',),
            'fields': (
                'download_count',
            )
        }),
        (_('Taxonomy'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': ('tags_text', 'categories')
        }),
        (_('Release'), {
            'classes': ('suit-tab suit-tab-general',
                        'grp-collapse collapse-closed'),
            'fields': ( 'released_datetime', 'status',
                        'created_datetime', 'updated_datetime'
            )
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
        ('versions', _('Versions')),
        ('statistics', _('Statistics')),
    )
    search_fields = ( 'title', 'package_name', '^author__name')
    list_display = ( 'pk', 'show_icon',
                     'title',
                     'package_name',
                     'tags_text',
                     'released_datetime',
                     'was_published_recently',
                     'status',
                     'download_count',
                     'is_data_integration',
                     'download_url',
    )
    raw_id_fields = ('author', )
    list_filter = ('categories', 'released_datetime', 'status')
    list_display_links = ('title', 'package_name',)
    list_editable = ('status', 'tags_text',)
    date_hierarchy = 'released_datetime'
    ordering = ('-released_datetime',)
    filter_horizontal = ("categories",)
    list_select_related = True
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }

    def _get_packageversion_download_url(self, version):
        try:
            return version.get_download_static_url()
        except (AttributeError, ValueError):
            return '#'

    def download_url(self, obj):
        try:
            a = '<a href="{url}" target="_blank">下载地址</a>'
            return a.format(url=self._get_packageversion_download_url(
                obj.versions.latest_version()),
            )
        except:
            pass
        return None

    download_url.short_description = _('download url')
    download_url.allow_tags = True

    def _check_packageversion_download_data_integration(self, version):
        try:
            url = version.di_download.url
            return True
        except (AttributeError, ValueError):
            return False

    def is_data_integration(self, obj):
        latest_version = obj.versions.latest_version()
        return self._check_packageversion_download_data_integration(
            latest_version
        )

    is_data_integration.short_description = _('is data integration download?')
    is_data_integration.boolean = True

    def show_icon(self, obj):
        try:
            version = obj.versions.latest('version_code')
            return mark_safe(
                '<img src="%s" alt="%s"/>' % (version.icon.url, obj.title))
        except ValueError:
            return ''

    show_icon.short_description = _('Icon')
    show_icon.allow_tags = True

    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(status=Package.STATUS.published)

    make_published.short_description = _('Make selected Packages as published')

    def make_unpublished(self, request, queryset):
        queryset.update(status=Package.STATUS.unpublished)

    make_unpublished.short_description = _(
        'Make selected Packages as unpublished')

    readonly_fields = (
        'download_count', 'created_datetime', 'updated_datetime',)

    def suit_row_attributes(self, obj, request):
        css_class = {
            'draft': 'info',
            'published': 'success',
            'unpublished': 'warning',
            'reject': 'error',
        }.get(obj.status)
        if css_class:
            return {'class': css_class, 'data': obj.package_name}


class PackageInline(TabularInline):
    model = Package
    #extra = 1
    max_num = 100
    fields = ('title', 'package_name', 'released_datetime', 'status' )
    readonly_fields = ('title', 'package_name', 'released_datetime' )


class AuthorAdmin(MainAdmin):
    model = Author
    list_display = ( 'pk', 'show_icon', 'name', 'email', 'phone')
    search_fields = ( 'name', 'email', 'phone')
    list_display_links = ('name', 'show_icon',)
    list_filter = ('status', )
    ordering = ('name',)

    show_icon = AdminIconField(allow_tags=True,
                               short_description=_('Icon'))
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput},
    }

    inlines = (PackageInline, )

    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(status=Author.STATUS.activated)

    make_published.short_description = _('Make selected Authors as activated')

    def make_unpublished(self, request, queryset):
        queryset.update(status=Author.STATUS.unactivated)

    make_unpublished.short_description = _(
        'Make selected Authors as unactivated')


    def suit_row_attributes(self, obj, request):
        css_class = {
            'draft': 'info',
            'activated': 'success',
            'unactivated': 'warning',
            'reject': 'error',
        }.get(obj.status)
        if css_class:
            return {'class': css_class, 'data': obj.name}

    def get_form(self, request, obj=None, **kwargs):
        form = super(AuthorAdmin, self).get_form(request, obj, **kwargs)
        # FIXME 简化author.email数据填充,自动生成处理
        email = "%s@testcase.com" % now().strftime('%Y%m%d-%H%M%S')
        form.base_fields['email'].initial = email
        return form


admin.site.register(PackageVersion, PackageVersionAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Author, AuthorAdmin)

