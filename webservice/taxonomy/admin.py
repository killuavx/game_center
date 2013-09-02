# -*- encoding=utf-8 -*-
from taxonomy.models import Category
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from tagging.models import Tag, TaggedItem
from easy_thumbnails.templatetags import thumbnail
from django.utils.safestring import mark_safe
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from warehouse.models import Package


class CategorizedPackageInline(admin.TabularInline):
    model = Package.categories.through

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('show_icon', 'name', 'subtitle', 'slug')
    list_display_links = ('name', )
    inlines = (CategorizedPackageInline,)

    def show_icon(self, obj):
        return mark_safe('<img src="%s" alt="%s"/>' % (obj.icon.url, obj.name))
    show_icon.short_description = _('Icon')
    show_icon.allow_tags = True

    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput}
    }

admin.site.register(Category, CategoryAdmin)

admin.site.unregister(Tag)

class TaggedPackageInline(admin.TabularInline):
    model = TaggedItem

class TagAdmin(admin.ModelAdmin):

    inlines = (TaggedPackageInline, )

admin.site.register(Tag, TagAdmin)
admin.site.unregister(TaggedItem)
