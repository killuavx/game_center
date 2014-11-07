# -*- coding: utf-8 -*-
from django.contrib import admin
from video.models import Video


class VideoAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title', 'user', 'created',)
    readonly_fields = ('created', 'updated', 'file_size', 'file_md5', )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'user',
            ),
        }),
        ('File', {
            'fields': (
                'workspace',
                'file',
                ('file_size', 'file_md5'),
            ),
        }),
        ('Status', {
            'fields': (
                ('created', 'updated',),
            ),
        }),
    )

    raw_id_fields = ('user',)
    ordering = ('-created', )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj and obj.pk:
            return readonly_fields + ['workspace', ]
        return readonly_fields


admin.site.register(Video, VideoAdmin)