# -*- encoding=utf-8 -*-
from django.core.urlresolvers import reverse, NoReverseMatch
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

class TopicalItemAdmin(admin.ModelAdmin):
    model = TopicalItem
    search_fields = ('topic', )
    search_fields = ('^topic__name', '^topic__slug')
    list_display = ('pk', 'topic_link', 'content_object_link', 'ordering')
    list_filter = ('topic', 'content_type')
    list_editable = ('ordering', )
    sortable = 'ordering'

    def content_object_link(self, obj):
        try:
            link = reverse(
                'admin:%s_%s_change' % (obj.content_object._meta.app_label,
                                        obj.content_object._meta.module_name),
                args=[obj.content_object.pk])
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (link, obj.content_object))
        except (ValueError, AttributeError, NoReverseMatch):
            return obj.content_object

    content_object_link.short_description = _('content object')
    content_object_link.allow_tags = True

    def topic_link(self, obj):
        try:
            link = reverse(
                'admin:%s_%s_change' % (obj.topic._meta.app_label,
                                        obj.topic._meta.module_name),
                args=[obj.topic.pk])
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (link, obj.topic))
        except (ValueError, AttributeError, NoReverseMatch):
            return obj.topic

    topic_link.short_description = _('topic')
    topic_link.allow_tags = True
    topic_link.admin_order_field = 'topic__name'


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

try:
    admin.site.unregister(Tag)
except admin.sites.NotRegistered:
    pass
else:
    admin.site.register(Tag, TagAdmin)

try:
    admin.site.unregister(TaggedItem)
except admin.sites.NotRegistered:
    pass
