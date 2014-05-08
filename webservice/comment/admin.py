# -*- coding: utf-8 -*-
from mezzanine.conf import settings
from django.contrib import admin
from django.contrib.admin import site
from django.contrib.admin.sites import NotRegistered
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin as TabularInline
from mezzanine.generic.admin import ThreadedCommentAdmin
from mezzanine.utils.urls import admin_url
from copy import deepcopy
from django.contrib.comments import get_model as get_comment_model
from comment.models import FeedbackType, Feedback, Petition, PetitionPackageVersion
from django.contrib.contenttypes import generic
from toolkit.admin import admin_edit_linktag


class CommentReplyInline(TabularInline):
    fk_name = 'replied_to'
    fields = ('comment', 'submit_date')
    readonly_fields = ('submit_date',)
    model = get_comment_model()


class CommentAdmin(ThreadedCommentAdmin):
    inlines = (CommentReplyInline, )

    list_display = ('object_title', 'content_type', ) + deepcopy(ThreadedCommentAdmin.list_display)
    search_fields = ('object_pk', ) + deepcopy(ThreadedCommentAdmin.search_fields)

    def object_title(self, obj):
        content = obj.content_object
        try:
            return admin_edit_linktag(content,
                                      ("%s[%s, %s]" %(content.package,
                                                      content.version_name,
                                                      content.version_code
                                      )))
        except: pass
        return admin_edit_linktag(content)
    object_title.allow_tags = True
    object_title.short_description = _('Object Title')

    def save_model(self, request, obj, form, change):
        if not obj.ip_address:
            obj.ip_address = request.get_client_ip()
        super(CommentAdmin, self).save_model(request, obj, form, change)

generic_comments = getattr(settings, "COMMENTS_APP", "") == "mezzanine.generic"
if generic_comments and not settings.COMMENTS_DISQUS_SHORTNAME:
    try:
        site.unregister(get_comment_model())
    except NotRegistered:
        pass
    site.register(get_comment_model(), CommentAdmin)

try:
    site.unregister(get_comment_model())
except NotRegistered:
    pass
else:
    site.register(get_comment_model(), CommentAdmin)


class MainAdmin(VersionAdmin):
    pass


class FeedbackReplyInline(TabularInline,
                          generic.GenericTabularInline):
    ct_field = "content_type"
    ct_fk_field = "object_pk"
    fields = ('comment', 'user', 'submit_date')
    readonly_fields = ('submit_date', 'user')
    model = get_comment_model()


class AdminSaveFormsetCommentMixin(object):

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        Comment = get_comment_model()
        for instance in instances:
            if isinstance(instance, Comment):
                instance.user = request.user
            instance.save()
        formset.save_m2m()


class FeedbackAdmin(AdminSaveFormsetCommentMixin,
                    MainAdmin):

    inlines = (FeedbackReplyInline,)

    fieldsets = (
        (None, {
            'fields': [
                ('content_type', 'object_pk',),
                'kind',
                'comment',
                ('created', 'updated'),
            ]
        }),
        (None, {
            'fields': [
                'status',
                'is_owner_ignored'
            ]
        })
    )
    list_display = (
        'pk', 'kind', 'status', 'comment', 'content_link', 'created'
    )
    list_filter = ('kind', 'status')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'updated')

    def content_link(self, obj):
        try:
            return admin_edit_linktag(obj.content_object)
        except:
            return None
    content_link.allow_tags = True

    def save_formset(self, **kwargs):
        super(FeedbackAdmin, self).save_formset(**kwargs)


class FeedbackTypeAdmin(MainAdmin):

    fields = (
        'title', 'slug', 'level'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_action(self, action):
        return ()

    def get_readonly_fields(self, request, obj=None):
        fields = ()
        if obj is not None and obj.pk:
            fields = obj.__class__._meta.get_all_field_names()
        return fields

    list_display = ('pk', 'title', 'slug', 'level')


site.register(Feedback, FeedbackAdmin)
site.register(FeedbackType, FeedbackTypeAdmin)


class PetitionPackageVersionAdmin(MainAdmin):

    list_display = ('pk', 'title', 'url', 'package_name', 'version_name', )
    fields = [
        'url', 'title', 'package_name', 'version_name',
    ]
    readonly_fields = ()

    def has_delete_permission(self, request, obj=None):
        return False

    #def has_add_permission(self, request):
    #    return False

    def get_action(self, action):
        return ()


class PetitionAdmin(AdminSaveFormsetCommentMixin,
                    MainAdmin):
    inlines = (FeedbackReplyInline, )
    list_display = ('pk', 'petition_for_link', 'packageversion_link',
                    'comment',
                    'status',
                    'created', 'updated', )
    #readonly_fields = ('petition_for', 'verifier', 'user', 'comment')
    fields = (
        'petition_for', 'packageversion',
        'comment',
        'status',
        'created',
        'updated',
        'confirmed_at',
        'finished_at',
        'rejected_at',
        'deleted_at',
    )
    readonly_fields = ('created', 'updated',
                       'confirmed_at',
                       'finished_at',
                       'rejected_at',
                       'deleted_at')
    list_editable = ('status',)
    list_filter = ('status', )
    date_hierarchy = 'created'
    raw_id_fields = ('packageversion',)

    def packageversion_link(self, obj):
        if not obj.packageversion:
            return None
        return '<a href="%s" target="_blank">%s</a>' % \
               (admin_url(obj.packageversion, "change", obj.packageversion.pk),
                str(obj.packageversion))
    packageversion_link.short_description = 'Package Version'
    packageversion_link.allow_tags = True

    def petition_for_link(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % \
               (admin_url(obj.petition_for, "change", obj.petition_for.pk),
                str(obj.petition_for))
    petition_for_link.short_description = Petition._meta.verbose_name
    petition_for_link.allow_tags = True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_action(self, action):
        return ()


admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionPackageVersion, PetitionPackageVersionAdmin)
