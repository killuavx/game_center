# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IOSAppData.is_image_downloaded'
        db.add_column('crawler_iosappdata', 'is_image_downloaded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'IOSAppData.image_downloaded'
        db.add_column('crawler_iosappdata', 'image_downloaded',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True),
                      keep_default=False)

        # Adding index on 'IOSAppData', fields ['is_image_downloaded']
        db.create_index('crawler_iosappdata', ['is_image_downloaded'])

        # Adding index on 'IOSAppData', fields ['image_downloaded']
        db.create_index('crawler_iosappdata', ['image_downloaded'])

        # Adding index on 'IOSAppData', fields ['is_analysised']
        db.create_index('crawler_iosappdata', ['is_analysised'])


    def backwards(self, orm):
        # Removing index on 'IOSAppData', fields ['is_analysised']
        db.delete_index('crawler_iosappdata', ['is_analysised'])

        # Removing index on 'IOSAppData', fields ['image_downloaded']
        db.delete_index('crawler_iosappdata', ['image_downloaded'])

        # Removing index on 'IOSAppData', fields ['is_image_downloaded']
        db.delete_index('crawler_iosappdata', ['is_image_downloaded'])

        # Deleting field 'IOSAppData.is_image_downloaded'
        db.delete_column('crawler_iosappdata', 'is_image_downloaded')

        # Deleting field 'IOSAppData.image_downloaded'
        db.delete_column('crawler_iosappdata', 'image_downloaded')


    models = {
        'crawler.iosappdata': {
            'Meta': {'index_together': "(('is_free',), ('analysised',), ('is_analysised',), ('is_image_downloaded',), ('image_downloaded',), ('mainclass', 'subclass'))", 'object_name': 'IOSAppData', 'unique_together': "(('appid', 'package_name', 'version_name'),)"},
            'analysised': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'appid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_downloaded': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'is_image_downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mainclass': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'packageversion_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'version_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['crawler']