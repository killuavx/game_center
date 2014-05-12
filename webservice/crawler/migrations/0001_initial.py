# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IOSAppData'
        db.create_table('crawler_iosappdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('package_name', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=200)),
            ('version_name', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=200)),
            ('mainclass', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50)),
            ('subclass', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50)),
            ('device', self.gf('django.db.models.fields.IntegerField')()),
            ('is_free', self.gf('django.db.models.fields.IntegerField')(db_column='isfree')),
            ('is_analysised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content', self.gf('django.db.models.fields.TextField')(db_column='download_content')),
        ))
        db.send_create_signal('crawler', ['IOSAppData'])

        # Adding unique constraint on 'IOSAppData', fields ['appid', 'package_name', 'version_name']
        db.create_unique('crawler_iosappdata', ['appid', 'package_name', 'version_name'])

        # Adding index on 'IOSAppData', fields ['mainclass', 'subclass']
        db.create_index('crawler_iosappdata', ['mainclass', 'subclass'])


    def backwards(self, orm):
        # Removing index on 'IOSAppData', fields ['mainclass', 'subclass']
        db.delete_index('crawler_iosappdata', ['mainclass', 'subclass'])

        # Removing unique constraint on 'IOSAppData', fields ['appid', 'package_name', 'version_name']
        db.delete_unique('crawler_iosappdata', ['appid', 'package_name', 'version_name'])

        # Deleting model 'IOSAppData'
        db.delete_table('crawler_iosappdata')


    models = {
        'crawler.iosappdata': {
            'Meta': {'index_together': "(('mainclass', 'subclass'),)", 'object_name': 'IOSAppData', 'unique_together': "(('appid', 'package_name', 'version_name'),)"},
            'appid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'mainclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'package_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'subclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'version_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['crawler']