# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClientPackageVersion'
        db.create_table('clientapp_clientpackageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, default='', blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, default='', blank=True)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('download', self.gf('django.db.models.fields.files.FileField')(max_length=100, default='', blank=True)),
            ('download_size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=9, default=0, blank=True)),
            ('version_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('version_code', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, default='', blank=True)),
            ('memorandum', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('whatsnew', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(no_check_for_status=True, max_length=100, default='draft', blank=True)),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('clientapp', ['ClientPackageVersion'])

        # Adding unique constraint on 'ClientPackageVersion', fields ['package_name', 'version_code']
        db.create_unique('clientapp_clientpackageversion', ['package_name', 'version_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'ClientPackageVersion', fields ['package_name', 'version_code']
        db.delete_unique('clientapp_clientpackageversion', ['package_name', 'version_code'])

        # Deleting model 'ClientPackageVersion'
        db.delete_table('clientapp_clientpackageversion')


    models = {
        'clientapp.clientpackageversion': {
            'Meta': {'object_name': 'ClientPackageVersion', 'unique_together': "(('package_name', 'version_code'),)", 'ordering': "('package_name', '-version_code')"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True'}),
            'download_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memorandum': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        }
    }

    complete_apps = ['clientapp']