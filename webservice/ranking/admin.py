# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from ranking.models import *
from django.contrib import admin
from mezzanine.core.admin import (DisplayableAdmin,
                                  TabularDynamicInlineAdmin as TabularInline,
                                  StackedDynamicInlineAdmin as StackedInline)


class PackageRankingInline(TabularInline):
    model = PackageRanking
    fields = ['category',
              'cycle_type',
              'status',
              'publish_date',
              'expiry_date', 'created', 'updated' ]
    readonly_fields = ('created', 'updated')


class PackageRankingTypeAdmin(VersionAdmin, DisplayableAdmin):
    list_filter = ('status', )
    inlines = (PackageRankingInline, )


class PackageRankingItemInline(TabularInline):
    model = PackageRankingItem
    fields = ['package', 'created', '_order']
    raw_id_fields = ('package', )
    readonly_fields = ('created', )


class PackageRankingAdmin(VersionAdmin):

    list_display = ('pk', 'category',
                    'slug',
                    'title',
                    'cycle_type',
                    'status',
                    'updated',
                    '_order',
    )
    list_editable = ('_order',)
    list_filter = ('status',
                   'category',
                   'ranking_type__slug',
                   'cycle_type', )
    fieldsets = (
        (None, {
            "fields": [
                       'ranking_type', 'category', 'cycle_type',
                       ("publish_date", "expiry_date"),
                       "status", "in_sitemap"
                      ],
            }),
    )

    inlines = (PackageRankingItemInline, )


admin.site.register(PackageRankingType, PackageRankingTypeAdmin)
admin.site.register(PackageRanking, PackageRankingAdmin)
