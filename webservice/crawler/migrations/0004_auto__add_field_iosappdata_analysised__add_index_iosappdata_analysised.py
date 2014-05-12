# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IOSAppData.analysised'
        db.add_column('crawler_iosappdata', 'analysised',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding index on 'IOSAppData', fields ['analysised']
        db.create_index('crawler_iosappdata', ['analysised'])

        # Adding index on 'IOSAppData', fields ['is_free']
        db.create_index('crawler_iosappdata', ['isfree'])


    def backwards(self, orm):
        # Removing index on 'IOSAppData', fields ['is_free']
        db.delete_index('crawler_iosappdata', ['isfree'])

        # Removing index on 'IOSAppData', fields ['analysised']
        db.delete_index('crawler_iosappdata', ['analysised'])

        # Deleting field 'IOSAppData.analysised'
        db.delete_column('crawler_iosappdata', 'analysised')


    models = {
        'crawler.iosappdata': {
            'Meta': {'object_name': 'IOSAppData', 'unique_together': "(('appid', 'package_name', 'version_name'),)", 'index_together': "(('is_free',), ('analysised',), ('mainclass', 'subclass'))"},
            'analysised': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'mainclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'packageversion_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['crawler']