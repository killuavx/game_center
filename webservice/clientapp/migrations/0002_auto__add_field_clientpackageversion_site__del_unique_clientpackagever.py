# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ClientPackageVersion', fields ['package_name', 'version_code']
        db.delete_unique('clientapp_clientpackageversion', ['package_name', 'version_code'])

        # Adding field 'ClientPackageVersion.site'
        db.add_column('clientapp_clientpackageversion', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'ClientPackageVersion', fields ['site', 'package_name', 'version_code']
        db.create_unique('clientapp_clientpackageversion', ['site_id', 'package_name', 'version_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'ClientPackageVersion', fields ['site', 'package_name', 'version_code']
        db.delete_unique('clientapp_clientpackageversion', ['site_id', 'package_name', 'version_code'])

        # Deleting field 'ClientPackageVersion.site'
        db.delete_column('clientapp_clientpackageversion', 'site_id')

        # Adding unique constraint on 'ClientPackageVersion', fields ['package_name', 'version_code']
        db.create_unique('clientapp_clientpackageversion', ['package_name', 'version_code'])


    models = {
        'clientapp.clientpackageversion': {
            'Meta': {'object_name': 'ClientPackageVersion', 'unique_together': "(('site', 'package_name', 'version_code'),)", 'ordering': "('package_name', '-version_code')"},
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
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'draft'", 'max_length': '100', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['clientapp']