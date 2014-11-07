# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('video_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos', to=orm['account.User'])),
            ('preview', self.gf('django.db.models.fields.files.ImageField')(max_length=500, default='', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('workspace', self.gf('mezzanine.core.fields.FileField')(max_length=500, default='videos', blank=True)),
            ('file', self.gf('video.fields.VideoFileField')(max_length=500)),
            ('file_size', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('file_md5', self.gf('django.db.models.fields.CharField')(null=True, max_length=40, default=None, blank=True)),
        ))
        db.send_create_signal('video', ['Video'])

        # Adding index on 'Video', fields ['created']
        db.create_index('video_video', ['created'])

        # Adding index on 'Video', fields ['user', 'created']
        db.create_index('video_video', ['user_id', 'created'])


    def backwards(self, orm):
        # Removing index on 'Video', fields ['user', 'created']
        db.delete_index('video_video', ['user_id', 'created'])

        # Removing index on 'Video', fields ['created']
        db.delete_index('video_video', ['created'])

        # Deleting model 'Video'
        db.delete_table('video_video')


    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'video.video': {
            'Meta': {'index_together': "(('user',), ('created',), ('user', 'created'))", 'object_name': 'Video'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'file': ('video.fields.VideoFileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['account.User']"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "'videos'", 'blank': 'True'})
        }
    }

    complete_apps = ['video']