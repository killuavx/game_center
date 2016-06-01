# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'IOSBuyInfo.ipafile'
        db.alter_column('crawler_iosbuyinfo', 'ipafile', self.gf('toolkit.fields.PkgFileField')(null=True, max_length=100))

    def backwards(self, orm):

        # Changing field 'IOSBuyInfo.ipafile'
        db.alter_column('crawler_iosbuyinfo', 'ipafile', self.gf('toolkit.fields.PkgFileField')(default=None, max_length=100))

    models = {
        'crawler.iosappdata': {
            'Meta': {'index_together': "(('is_free',), ('analysised',), ('is_analysised',), ('is_image_downloaded',), ('image_downloaded',), ('mainclass', 'subclass'))", 'unique_together': "(('appid', 'package_name', 'version_name'),)", 'object_name': 'IOSAppData'},
            'analysised': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_downloaded': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'is_image_downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mainclass': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'packageversion_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'version_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'})
        },
        'crawler.iosbuyinfo': {
            'Meta': {'index_together': "(('appid',), ('buy_status',), ('updated',), ('buy_status', 'updated'))", 'object_name': 'IOSBuyInfo'},
            'account': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'appdata': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['crawler.IOSAppData']"}),
            'appid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'buy_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'buy_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipafile': ('toolkit.fields.PkgFileField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'ipafile_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'default': 'None', 'max_length': '40'}),
            'ipafile_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['crawler']