# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoadingCover'
        db.create_table('clientapp_loadingcover', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['clientapp.ClientPackageVersion'], blank=True, null=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('clientapp', ['LoadingCover'])

        # Adding index on 'LoadingCover', fields ['site', '_order']
        db.create_index('clientapp_loadingcover', ['site_id', '_order'])

        # Adding index on 'LoadingCover', fields ['site', 'status']
        db.create_index('clientapp_loadingcover', ['site_id', 'status'])

        # Adding index on 'LoadingCover', fields ['site', 'status', '_order']
        db.create_index('clientapp_loadingcover', ['site_id', 'status', '_order'])


    def backwards(self, orm):
        # Removing index on 'LoadingCover', fields ['site', 'status', '_order']
        db.delete_index('clientapp_loadingcover', ['site_id', 'status', '_order'])

        # Removing index on 'LoadingCover', fields ['site', 'status']
        db.delete_index('clientapp_loadingcover', ['site_id', 'status'])

        # Removing index on 'LoadingCover', fields ['site', '_order']
        db.delete_index('clientapp_loadingcover', ['site_id', '_order'])

        # Deleting model 'LoadingCover'
        db.delete_table('clientapp_loadingcover')


    models = {
        'clientapp.clientpackageversion': {
            'Meta': {'unique_together': "(('site', 'package_name', 'version_code'),)", 'ordering': "('package_name', '-version_code')", 'object_name': 'ClientPackageVersion'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '9', 'blank': 'True'}),
            'download_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memorandum': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'clientapp.loadingcover': {
            'Meta': {'ordering': "('site', '_order')", 'object_name': 'LoadingCover', 'index_together': "(('site', '_order'), ('site', 'status'), ('site', 'status', '_order'))"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['clientapp.ClientPackageVersion']", 'blank': 'True', 'null': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['clientapp']