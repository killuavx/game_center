# -*- coding: utf-8 -*-
from django.contrib import admin

from mezzanine.blog.admin import BlogCategoryAdmin
from mezzanine.blog.models import BlogCategory

class CustomBlogCategoryAdmin(BlogCategoryAdmin):

    list_display = ('title', 'slug')
    fieldsets = ((None, {"fields": ("title",
                                    "slug")}),)

try:
    admin.site.unregister(BlogCategory)
except admin.sites.NotRegistered:
    pass

admin.site.register(BlogCategory, CustomBlogCategoryAdmin)

