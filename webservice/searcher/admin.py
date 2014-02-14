# -*- encoding: utf-8-*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from searcher.models import TipsWord


class TipsWordAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'keyword',
                'weight',
            )
        }),
        (_('Status'), {
            'fields': (
                'status',
                'released_datetime',
                'updated_datetime',
                'created_datetime'
            )
        })
    )
    list_display = ('keyword', 'weight', 'status', 'released_datetime')
    readonly_fields = ('created_datetime', 'updated_datetime')
    list_editable = ('status', 'released_datetime', 'weight')
    search_fields = ('keyword',)
    list_filter = ('released_datetime', 'status')
    ordering = ('-weight', )

    sortable = 'weight'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_order = obj.__class__.objects.aggregate(
                models.Max(self.sortable))
            try:
                next_order = max_order['%s__max' % self.sortable] + 1
            except TypeError:
                next_order = 1
            setattr(obj, self.sortable, next_order)
        super(TipsWordAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields

        return self.readonly_fields + ('keyword', )

admin.site.register(TipsWord, TipsWordAdmin)
