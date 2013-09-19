# -*- encoding: utf-8-*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from suit.admin import SortableModelAdmin
from searcher.models import TipsWord


class TipsWordAdmin(SortableModelAdmin, VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'keyword',
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
    readonly_fields = ('created_datetime', 'updated_datetime' )
    list_editable = ('status', 'released_datetime' )
    search_fields = ('keyword',)
    list_filter = ('released_datetime', 'status')
    sortable = 'weight'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields

        return self.readonly_fields + ( 'keyword', )

admin.site.register(TipsWord, TipsWordAdmin)
