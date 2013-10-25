# -*- encoding=utf-8 -*-
from taxonomy.models import Category, Topic, TopicalItem
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from tagging.models import Tag, TaggedItem
from django.utils.safestring import mark_safe
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from warehouse.models import Package
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin, SortableTabularInline
from reversion.admin import VersionAdmin

from easy_thumbnails.exceptions import InvalidImageFormatError
class EmptySupportImageClearableFileInput(ImageClearableFileInput):

    def render(self, name, value, attrs=None):
        try:
            return super(EmptySupportImageClearableFileInput, self).render(
                name, value, attrs)
        except InvalidImageFormatError:
            return super(ImageClearableFileInput, self).render(
                name, value, attrs)

class CategorizedPackageInline(admin.TabularInline):
    model = Package.categories.through

class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin, VersionAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'show_icon', 'subtitle', 'slug', 'is_hidden', 'ordering',)
    list_display_links = ('name', )
    list_editable = ('is_hidden',)
    list_filter = ('is_hidden',)
    #inlines = (CategorizedPackageInline,)

    mptt_level_indent = 20
    sortable = 'ordering'

    def show_icon(self, obj):
        try:
            return mark_safe('<img src="%s" alt="%s"/>' % \
                             (obj.icon.url, obj.name))
        except ValueError:
            return obj.name
    show_icon.short_description = _('Icon')
    show_icon.allow_tags = True

    formfield_overrides = {
        ThumbnailerImageField: {'widget': EmptySupportImageClearableFileInput}
    }

class TaggedPackageInline(admin.TabularInline):
    model = TaggedItem

class TagAdmin(VersionAdmin):

    inlines = (TaggedPackageInline, )

class TopicalItemAdmin(SortableModelAdmin):
    model = TopicalItem
    search_fields = ('topic', )
    search_fields = ('^topic__name', '^topic__slug')
    list_filter = ('topic', 'content_type')
    sortable = 'ordering'

class TopicInline(SortableTabularInline):
    model = Topic
    fields = ('name', 'slug', 'ordering', 'status', 'released_datetime' )
    #readonly_fields = ('name', 'slug',)
    sortable = 'ordering'
    extra = 0

class TopicAdmin(MPTTModelAdmin, SortableModelAdmin, VersionAdmin):

    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'show_icon_or_cover', 'slug', 'status', 'is_hidden')
    list_display_links = ('name', )
    search_fields = ('^name', '^slug', )
    list_filter = ('parent', 'status')
    list_editable = ('status', 'is_hidden')
    mptt_level_indent = 20
    sortable = 'ordering'

    def show_icon_or_cover(self, obj):
        try:
            return mark_safe('<img src="%s" alt="%s"/>' % \
                             (obj.icon.url, obj.name))
        except ValueError:
            pass

        try:
            return mark_safe('<img src="%s" alt="%s"/>' % \
                             (obj.cover.url, obj.name))
        except ValueError:
            pass

        return obj.name
    show_icon_or_cover.short_description = _('Icon/Cover')
    show_icon_or_cover.allow_tags = True

    inlines = (TopicInline,)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicalItem, TopicalItemAdmin)

admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(TaggedItem)
