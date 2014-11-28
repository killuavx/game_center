# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LoadingCover.content_type'
        db.add_column('clientapp_loadingcover', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType'], blank=True),
                      keep_default=False)

        # Adding field 'LoadingCover.object_id'
        db.add_column('clientapp_loadingcover', 'object_id',
                      self.gf('django.db.models.fields.IntegerField')(blank=True, default=0),
                      keep_default=False)

        # Adding field 'LoadingCover.link'
        db.add_column('clientapp_loadingcover', 'link',
                      self.gf('django.db.models.fields.URLField')(blank=True, default='', max_length=1024),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LoadingCover.content_type'
        db.delete_column('clientapp_loadingcover', 'content_type_id')

        # Deleting field 'LoadingCover.object_id'
        db.delete_column('clientapp_loadingcover', 'object_id')

        # Deleting field 'LoadingCover.link'
        db.delete_column('clientapp_loadingcover', 'link')


    models = {
        'clientapp.clientpackageversion': {
            'Meta': {'object_name': 'ClientPackageVersion', 'ordering': "('package_name', '-version_code')", 'unique_together': "(('site', 'package_name', 'version_code'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '9'}),
            'download_size': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memorandum': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'default': "'draft'", 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'clientapp.loadingcover': {
            'Meta': {'object_name': 'LoadingCover', 'index_together': "(('site', '_order'), ('site', 'status'), ('site', 'status', '_order'))", 'ordering': "('site', '_order')"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'default': "''", 'max_length': '1024'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'package_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['clientapp.ClientPackageVersion']", 'default': 'None', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'toolkit.resource': {
            'Meta': {'object_name': 'Resource', 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'db_table': "'common_resource'", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)"},
            'alias': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'default'", 'max_length': '50'}),
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'default': 'None', 'max_length': '40'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'default': 'None', 'max_length': '100'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'})
        }
    }

    complete_apps = ['clientapp']