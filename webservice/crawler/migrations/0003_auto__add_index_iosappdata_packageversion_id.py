# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'IOSAppData', fields ['packageversion_id']
        db.create_index('crawler_iosappdata', ['packageversion_id'])


    def backwards(self, orm):
        # Removing index on 'IOSAppData', fields ['packageversion_id']
        db.delete_index('crawler_iosappdata', ['packageversion_id'])


    models = {
        'crawler.iosappdata': {
            'Meta': {'index_together': "(('mainclass', 'subclass'),)", 'unique_together': "(('appid', 'package_name', 'version_name'),)", 'object_name': 'IOSAppData'},
            'appid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'mainclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'package_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'packageversion_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'version_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['crawler']