# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table('common_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.IntegerField')()),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True, default='default')),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=100, default='')),
            ('file', self.gf('mezzanine.core.fields.FileField')(max_length=500)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(null=True, max_length=100, blank=True, default=None)),
            ('file_md5', self.gf('django.db.models.fields.CharField')(null=True, max_length=40, blank=True, default=None)),
            ('file_size', self.gf('django.db.models.fields.IntegerField')(blank=True, default=0)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True, default=0)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True, default=0)),
        ))
        db.send_create_signal('toolkit', ['Resource'])

        # Adding unique constraint on 'Resource', fields ['site', 'content_type', 'object_pk', 'kind', 'alias']
        db.create_unique('common_resource', ['site_id', 'content_type_id', 'object_pk', 'kind', 'alias'])

        # Adding index on 'Resource', fields ['site', 'content_type']
        db.create_index('common_resource', ['site_id', 'content_type_id'])

        # Adding index on 'Resource', fields ['site', 'content_type', 'object_pk']
        db.create_index('common_resource', ['site_id', 'content_type_id', 'object_pk'])

        # Adding index on 'Resource', fields ['site', 'content_type', 'object_pk', 'kind']
        db.create_index('common_resource', ['site_id', 'content_type_id', 'object_pk', 'kind'])


    def backwards(self, orm):
        # Removing index on 'Resource', fields ['site', 'content_type', 'object_pk', 'kind']
        db.delete_index('common_resource', ['site_id', 'content_type_id', 'object_pk', 'kind'])

        # Removing index on 'Resource', fields ['site', 'content_type', 'object_pk']
        db.delete_index('common_resource', ['site_id', 'content_type_id', 'object_pk'])

        # Removing index on 'Resource', fields ['site', 'content_type']
        db.delete_index('common_resource', ['site_id', 'content_type_id'])

        # Removing unique constraint on 'Resource', fields ['site', 'content_type', 'object_pk', 'kind', 'alias']
        db.delete_unique('common_resource', ['site_id', 'content_type_id', 'object_pk', 'kind', 'alias'])

        # Deleting model 'Resource'
        db.delete_table('common_resource')


    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'db_table': "'django_comments'", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'null': 'True', 'blank': 'True', 'related_name': "'comment_comments'"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'ratings'", 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'ThreadedComment', '_ormbases': ['comments.Comment']},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['comments.Comment']", 'unique': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'to': "orm['generic.Rating']", 'object_id_field': "'object_pk'"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'comments'", 'to': "orm['generic.ThreadedComment']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'toolkit.resource': {
            'Meta': {'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'db_table': "'common_resource'", 'object_name': 'Resource', 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True', 'default': "'default'"}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'blank': 'True', 'default': 'None'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True', 'default': 'None'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True', 'default': '0'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_star'", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'to': "orm['generic.ThreadedComment']", 'default': 'None', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stars'", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'to': "orm['account.User']", 'default': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['toolkit']