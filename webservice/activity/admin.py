# -*- coding: utf-8 -*-
from django.contrib import admin
from toolkit.admin import admin_edit_linktag
from activity.models import GiftBag, GiftCardResource, Note, Bulletin, Activity
from import_export.admin import ImportMixin
from reversion.admin import VersionAdmin
from toolkit.helpers import sync_status_summary, sync_status_actions


def _(s):
    return s


class GiftBagAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = GiftCardResource

    search_fields = ('for_package__package_name',
                     'for_package__title',
    )

    list_display = ('pk', 'title', 'package', 'version', 'total_remaining', 'status',  'publish_date', 'expiry_date', )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                ('for_package', 'for_version', ),
                'summary',
                'usage_description',
                'issue_description',
            ),
        }),
        ('Issue', {
            'fields': (
                ('cards_total_count', 'cards_remaining_count',),
            )
        }),
        ('Status', {
            'fields': (
                'status',
                ('publish_date', 'expiry_date',),
                ('created', 'updated', ),
            ),
        }),
    )
    #list_editable = ('status', )
    raw_id_fields = ('for_package', 'for_version', )
    readonly_fields = ('created', 'updated', 'cards_total_count', 'cards_remaining_count',)
    ordering = ('-publish_date', )

    def package(self, obj):
        return admin_edit_linktag(obj.for_package, obj.for_package.title)
    package.allow_tags = True

    def version(self, obj):
        if obj.for_version:
            return admin_edit_linktag(obj.for_version, obj.for_version.version_name)
        return None
    version.allow_tags = True

    def total_remaining(self, obj):
        return "%s/%s" % (obj.cards_total_count, obj.cards_remaining_count)
    total_remaining.short_description = '总/剩余'

    def get_readonly_fields(self, request, obj=None):
        fields = list(self.readonly_fields)
        if obj and obj.pk:
            fields = fields + ['for_package', 'for_version']
        if not obj or (obj and not obj.cards_total_count):
            fields += ['status']
        return fields


admin.site.register(GiftBag, GiftBagAdmin)


class NoteAdmin(VersionAdmin):

    list_display = ('pk', 'slug', 'title', )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return self.readonly_fields + ('slug', )
        return self.readonly_fields


admin.site.register(Note, NoteAdmin)


class BulletinAdmin(VersionAdmin):

    search_fields = ('title', )

    list_filter = ('status', )

    date_hierarchy = 'publish_date'

    list_display = ('pk', 'title', 'status', 'publish_date', )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'content',
            ),
            }),
        ('Status', {
            'fields': (
                'user',
                'status',
                ('publish_date', 'expiry_date',),
                ('created', 'updated', ),
            ),
        }),
    )

    readonly_fields = ('created', 'updated', 'user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Bulletin, BulletinAdmin)


from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin


class ActivityAdmin(VersionAdmin,
                    DisplayableAdmin,
                    OwnableAdmin):

    search_fields = ('title', )
    list_filter = ('status', )
    date_hierarchy = 'publish_date'
    radio_fields = {"status": admin.HORIZONTAL}
    fieldsets = (
        (None, {
            "fields": ["title",
                       "slug",
                       "workspace",
                       "cover",
                       "content",
                       ]
            }),
        (_("Status"), {
            "fields": [
                'user',
                ("status", 'is_active'),
                ("publish_date", "expiry_date"),
                ("created", "updated"),
            ],
        }),
        (_("Meta data"), {
            "fields": ["_meta_title",
                       ("description", "gen_description"),
                       "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )
    list_display = ('pk', 'title', 'slug', 'status', 'is_active', 'publish_date',
                    'sync_file_action',
    )
    readonly_fields = ('created', 'updated', 'user', 'workspace',)

    def sync_file_action(self, obj):
        return sync_status_summary(obj) + " | " + sync_status_actions(obj)
    sync_file_action.allow_tags = True
    sync_file_action.short_description = _('Sync Status')

    class Media:
        static_url = '/static/'
        js = [static_url+'js/syncfile.action.js', ]


admin.site.register(Activity, ActivityAdmin)

from toolkit.models import CONTENT_STATUS_PUBLISHED
from activity.models import Lottery, LotteryPrize, LotteryWinning
from mezzanine.core.admin import TabularDynamicInlineAdmin as TabularInline


class LotteryPrizeInline(TabularInline):
    model = LotteryPrize
    fields = ('group', 'level',
              'title', 'win_prompt',
              'total_count', 'award_coin',
              'win_count',
              'status',
    )
    readonly_fields = ('win_count', 'status')
    ordering = ('-level',)
    extra = 5
    max_num = 5

    def get_readonly_fields(self, request, obj=None):
        #if obj and obj.status == CONTENT_STATUS_PUBLISHED:
        #    return self.fields
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False


class LotteryWinningInline(TabularInline):
    model = LotteryWinning
    fields = ('user', 'prize', 'status', 'win_date', 'accept_date')
    raw_id_fields = ('user', )
    ordering = ('-win_date',)
    max_num = 100

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == CONTENT_STATUS_PUBLISHED:
            return False
        return True


class LotteryAdmin(VersionAdmin):
    search_fields = ('title', )
    list_filter = ('status', )
    #date_hierarchy = 'publish_date',
    #radio_fields = {'status', admin.HORIZONTAL}
    fieldsets = (
        (None, {
            "fields": ["title",
                       "description",
                       "cost_coin",
                       ]
        }),
        (_("Status"), {
            "fields": [
                "status",
                ("publish_date", "expiry_date"),
                ("created", "updated"),
                ("takepartin_times", "takepartin_count"),
                ],
        }),
    )
    list_display = ('pk', 'title', 'status', 'publish_date', 'expiry_date')
    list_display_links = ('title', )
    ordering = ('status', '-publish_date', )
    readonly_fields = ('created', 'updated',
                       'takepartin_times', 'takepartin_count',
    )

    def get_inline_instances(self, request, obj=None):
        if obj and obj.pk and obj.prizes.count():
            inlines = (LotteryPrizeInline, LotteryWinningInline)
        else:
            inlines = (LotteryPrizeInline, )
        self.inlines = inlines
        return super(LotteryAdmin, self).get_inline_instances(request=request,
                                                              obj=obj)

admin.site.register(Lottery, LotteryAdmin)
