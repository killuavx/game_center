# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Activity.workspace'
        db.add_column('activity_activity', 'workspace',
                      self.gf('mezzanine.core.fields.FileField')(max_length=500, default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Activity.workspace'
        db.delete_column('activity_activity', 'workspace')


    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'activity.activity': {
            'Meta': {'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Activity'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '500', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']"}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '2000'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activitys'", 'to': "orm['account.User']"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'activity.bulletin': {
            'Meta': {'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))", 'object_name': 'Bulletin', 'ordering': "('-publish_date',)"},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulletins'", 'to': "orm['account.User']"})
        },
        'activity.giftbag': {
            'Meta': {'index_together': "(('site', 'for_package'), ('site', 'for_package', 'for_version'), ('site', 'publish_date'), ('site', 'for_package', 'publish_date'), ('site', 'for_package', 'for_version', 'publish_date'), ('site', 'status', 'publish_date'), ('site', 'status', 'for_package', 'publish_date'), ('site', 'status', 'for_package', 'for_version', 'publish_date'))", 'object_name': 'GiftBag', 'ordering': "('-publish_date',)"},
            'cards_remaining_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cards_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'for_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'giftbags'", 'to': "orm['warehouse.Package']"}),
            'for_version': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'giftbags'", 'blank': 'True', 'to': "orm['warehouse.PackageVersion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issue_description': ('django.db.models.fields.TextField', [], {}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING'}),
            'short_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'usage_description': ('django.db.models.fields.TextField', [], {})
        },
        'activity.giftcard': {
            'Meta': {'index_together': "(('site', 'giftbag', 'owner'), ('site', 'giftbag', 'owner', 'took_date'), ('site', 'owner'))", 'unique_together': "(('site', 'giftbag', 'code'),)", 'object_name': 'GiftCard'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'giftbag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards'", 'to': "orm['activity.GiftBag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'took_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'activity.note': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Note'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'db_table': "'django_comments'", 'object_name': 'Comment', 'ordering': "('submit_date',)"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'comment_comments'", 'blank': 'True', 'to': "orm['account.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.assignedkeyword': {
            'Meta': {'object_name': 'AssignedKeyword', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '2000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'ratings'", 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'object_name': 'ThreadedComment', '_ormbases': ['comments.Comment'], 'ordering': "('submit_date',)"},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['comments.Comment']"}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.Rating']"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'comments'", 'to': "orm['generic.ThreadedComment']"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'ordering': "('ordering',)"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'ordering': "('ordering',)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Topic']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('site', 'topic'), ('site', 'topic', 'content_type'), ('site', 'topic', 'content_type', 'object_id'), ('site', 'topic', 'content_type', 'object_id', 'ordering'), ('topic', 'content_type'))", 'object_name': 'TopicalItem', 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'ordering': "('ordering',)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'auto_now': 'True', 'blank': 'True'})
        },
        'toolkit.resource': {
            'Meta': {'db_table': "'common_resource'", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'object_name': 'Resource', 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'ordering': "('site', 'content_type', 'object_pk', 'kind')"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'default'", 'blank': 'True'}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'default': 'None', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_star'", 'default': 'None', 'to': "orm['generic.ThreadedComment']", 'on_delete': 'models.DO_NOTHING', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stars'", 'default': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '16', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.package': {
            'Meta': {'index_together': "(('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))", 'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '9', 'default': '0', 'blank': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'default': 'None', 'to': "orm['warehouse.PackageVersion']"}),
            'main_category_names': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'primary_packages'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'root_packages'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'index_together': "(('site', 'package'), ('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'), ('has_award',), ('site', 'has_award'), ('site', 'award_coin'), ('site', 'reported'), ('site', 'reported', 'status'))", 'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion'},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('comment.fields.CommentsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.ThreadedComment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'reported': ('warehouse.models.PkgReportField', [], {'default': 'False'}),
            'reported_adv': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_gplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'stars': ('toolkit.fields.StarsField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Star']"}),
            'stars_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_low_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_low_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_medium_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_medium_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'", 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedDevice']"}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedFeature']"}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedLanguage']"}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'default': '1'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.supporteddevice': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedDevice'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedfeature': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedFeature'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "''", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedlanguage': {
            'Meta': {'object_name': 'SupportedLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['activity']