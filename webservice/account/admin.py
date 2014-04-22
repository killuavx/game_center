# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from account.models import User, Profile
from mezzanine.accounts.admin import *

from guardian.admin import GuardedModelAdmin

if ProfileInline in UserProfileAdmin.inlines:
    idx = UserProfileAdmin.inlines.index(ProfileInline)
    inlines = list(UserProfileAdmin.inlines)
    inlines.pop(idx)
    UserProfileAdmin.inlines = inlines


class UserAdmin(UserProfileAdmin, VersionAdmin, GuardedModelAdmin):

    def has_profile(self, obj):
        try:
            profile = obj.profile
            return True
        except Profile.DoesNotExist:
            return False
    has_profile.boolean = True
    has_profile.short_description = _('has profile?')

    def get_list_display(self, request):
        #list_display = list(self.list_display)
        return self.list_display + ('has_profile', )


class ProfileAdmin(VersionAdmin, GuardedModelAdmin):
    raw_id_fields = ('user',)
    fields = (
        'user',
        'mugshot',
        'cover',
        'email',
        'phone',
        'privacy',
    )
    list_display = ('user', 'signup_date', )
    search_fields = ('user__username',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return ('user', ) + self.readonly_fields
        return self.readonly_fields

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
