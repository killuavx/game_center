# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ClientPackageVersion.resources_count'
        db.add_column('clientapp_clientpackageversion', 'resources_count',
                      self.gf('django.db.models.fields.IntegerField')(blank=True, default=0),
                      keep_default=False)

        # Adding field 'ClientPackageVersion.workspace'
        db.add_column('clientapp_clientpackageversion', 'workspace',
                      self.gf('mezzanine.core.fields.FileField')(blank=True, max_length=500, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ClientPackageVersion.resources_count'
        db.delete_column('clientapp_clientpackageversion', 'resources_count')

        # Deleting field 'ClientPackageVersion.workspace'
        db.delete_column('clientapp_clientpackageversion', 'workspace')


    models = {
        'clientapp.clientpackageversion': {
            'Meta': {'object_name': 'ClientPackageVersion', 'ordering': "('package_name', '-version_code')", 'unique_together': "(('site', 'package_name', 'version_code'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'download_size': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memorandum': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"})
        },
        'clientapp.loadingcover': {
            'Meta': {'index_together': "(('site', '_order'), ('site', 'status'), ('site', 'status', '_order'))", 'object_name': 'LoadingCover', 'ordering': "('site', '_order')"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['clientapp.ClientPackageVersion']", 'default': 'None', 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'toolkit.resource': {
            'Meta': {'db_table': "'common_resource'", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'object_name': 'Resource', 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))"},
            'alias': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "'default'"}),
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '40', 'default': 'None', 'null': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '6', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': 'None', 'null': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '6', 'default': '0'})
        }
    }

    complete_apps = ['clientapp']