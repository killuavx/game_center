# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IOSBuyInfo'
        db.create_table('crawler_iosbuyinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True, auto_now_add=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('appdata', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['crawler.IOSAppData'], null=True)),
            ('appid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('buy_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('buy_info', self.gf('django.db.models.fields.TextField')(default=None, blank=True, null=True)),
            ('ipafile', self.gf('toolkit.fields.PkgFileField')(max_length=100)),
            ('ipafile_size', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('ipafile_md5', self.gf('django.db.models.fields.CharField')(default=None, blank=True, max_length=40, null=True)),
            ('version', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200, null=True)),
            ('short_version', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200, null=True)),
            ('account', self.gf('django.db.models.fields.CharField')(default=None, max_length=255)),
        ))
        db.send_create_signal('crawler', ['IOSBuyInfo'])

        # Adding index on 'IOSBuyInfo', fields ['appid']
        db.create_index('crawler_iosbuyinfo', ['appid'])

        # Adding index on 'IOSBuyInfo', fields ['buy_status']
        db.create_index('crawler_iosbuyinfo', ['buy_status'])

        # Adding index on 'IOSBuyInfo', fields ['updated']
        db.create_index('crawler_iosbuyinfo', ['updated'])

        # Adding index on 'IOSBuyInfo', fields ['buy_status', 'updated']
        db.create_index('crawler_iosbuyinfo', ['buy_status', 'updated'])


    def backwards(self, orm):
        # Removing index on 'IOSBuyInfo', fields ['buy_status', 'updated']
        db.delete_index('crawler_iosbuyinfo', ['buy_status', 'updated'])

        # Removing index on 'IOSBuyInfo', fields ['updated']
        db.delete_index('crawler_iosbuyinfo', ['updated'])

        # Removing index on 'IOSBuyInfo', fields ['buy_status']
        db.delete_index('crawler_iosbuyinfo', ['buy_status'])

        # Removing index on 'IOSBuyInfo', fields ['appid']
        db.delete_index('crawler_iosbuyinfo', ['appid'])

        # Deleting model 'IOSBuyInfo'
        db.delete_table('crawler_iosbuyinfo')


    models = {
        'crawler.iosappdata': {
            'Meta': {'unique_together': "(('appid', 'package_name', 'version_name'),)", 'object_name': 'IOSAppData', 'index_together': "(('is_free',), ('analysised',), ('is_analysised',), ('is_image_downloaded',), ('image_downloaded',), ('mainclass', 'subclass'))"},
            'analysised': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'appid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'content': ('django.db.models.fields.TextField', [], {'db_column': "'download_content'"}),
            'device': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_downloaded': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'is_analysised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_free': ('django.db.models.fields.IntegerField', [], {'db_column': "'isfree'"}),
            'is_image_downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mainclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'package_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'packageversion_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'version_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        },
        'crawler.iosbuyinfo': {
            'Meta': {'index_together': "(('appid',), ('buy_status',), ('updated',), ('buy_status', 'updated'))", 'object_name': 'IOSBuyInfo'},
            'account': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}),
            'appdata': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['crawler.IOSAppData']", 'null': 'True'}),
            'appid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'buy_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'buy_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipafile': ('toolkit.fields.PkgFileField', [], {'max_length': '100'}),
            'ipafile_md5': ('django.db.models.fields.CharField', [], {'default': 'None', 'blank': 'True', 'max_length': '40', 'null': 'True'}),
            'ipafile_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['crawler']