# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SumDownloadProductResult'
        db.create_table('result_sum_download_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=11, default=0)),
            ('downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=11, default=0)),
        ))
        db.send_create_signal('analysis', ['SumDownloadProductResult'])

        # Adding unique constraint on 'SumDownloadProductResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_download_product', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Adding index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumDownloadProductResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_download_product', ['cycle_type', 'start_date_id', 'end_date_id'])


    def backwards(self, orm):
        # Removing index on 'SumDownloadProductResult', fields ['cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_download_product', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'start_date']
        db.delete_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumDownloadProductResult', fields ['productkey', 'cycle_type', 'end_date']
        db.delete_index('result_sum_download_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumDownloadProductResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_download_product', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Deleting model 'SumDownloadProductResult'
        db.delete_table('result_sum_download_product')


    models = {
        'analysis.activatefact': {
            'Meta': {'db_table': "'fact_activate'", 'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'))", 'object_name': 'ActivateFact', 'ordering': "('-date',)"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'db_table': "'fact_activate_newreserve'", 'object_name': 'ActivateNewReserveFact', '_ormbases': ['analysis.ActivateFact'], 'ordering': "('-date',)"},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['analysis.ActivateFact']"}),
            'is_new_package': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_package_version': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package_version': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'})
        },
        'analysis.baidupushdim': {
            'Meta': {'db_table': "'dim_baidupush'", 'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'object_name': 'BaiduPushDim'},
            'app_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.datedim': {
            'Meta': {'db_table': "'dim_date'", 'index_together': "(('year', 'month', 'day'), ('year', 'week'))", 'object_name': 'DateDim'},
            'datevalue': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'day': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'dayofweek': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'week': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'analysis.devicedim': {
            'Meta': {'db_table': "'dim_device'", 'object_name': 'DeviceDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'db_table': "'dim_devicelanguage'", 'object_name': 'DeviceLanguageDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'db_table': "'dim_devicemodel'", 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'object_name': 'DeviceModelDim'},
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.deviceosdim': {
            'Meta': {'db_table': "'dim_deviceos'", 'unique_together': "(('platform', 'os_version'),)", 'object_name': 'DeviceOSDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'db_table': "'dim_deviceplatform'", 'object_name': 'DevicePlatformDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'db_table': "'dim_deviceresolution'", 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'object_name': 'DeviceResolutionDim'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '25', 'default': "'undefined'"}),
            'orig_width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'db_table': "'dim_devicesupplier'", 'object_name': 'DeviceSupplierDim'},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'default': "'undefined'"}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'default': "'unknown'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'default': "'undefined'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'unknown'", 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'db_table': "'fact_downloadbeginfinish'", 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'unique_together': "(('start_download', 'end_download'),)", 'object_name': 'DownloadBeginFinishFact'},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_download': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.DownloadFact']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.DownloadFact']"})
        },
        'analysis.downloadfact': {
            'Meta': {'db_table': "'fact_download'", 'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'))", 'object_name': 'DownloadFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.eventdim': {
            'Meta': {'db_table': "'dim_event'", 'object_name': 'EventDim'},
            'eventtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.hourdim': {
            'Meta': {'db_table': "'dim_hour'", 'object_name': 'HourDim'},
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'db_table': "'dim_location'", 'unique_together': "(('country', 'region', 'city'),)", 'object_name': 'LocationDim'},
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"})
        },
        'analysis.mediaurldim': {
            'Meta': {'db_table': "'dim_downloadurl'", 'index_together': "(('host', 'path'),)", 'object_name': 'MediaUrlDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'db_table': "'dim_network'", 'object_name': 'NetworkDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'db_table': "'fact_openclose_daily'", 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'object_name': 'OpenCloseDailyFact'},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.packagecategorydim': {
            'Meta': {'db_table': "'dim_packagecategory'", 'object_name': 'PackageCategoryDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'default': "'undefined'"})
        },
        'analysis.packagedim': {
            'Meta': {'db_table': "'dim_package'", 'unique_together': "(('package_name', 'version_name'),)", 'object_name': 'PackageDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.packagekeydim': {
            'Meta': {'db_table': "'dim_packagekey'", 'object_name': 'PackageKeyDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.pagedim': {
            'Meta': {'db_table': "'dim_page'", 'index_together': "(('host', 'path'),)", 'object_name': 'PageDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'db_table': "'dim_product'", 'unique_together': "(('entrytype', 'channel'),)", 'object_name': 'ProductDim'},
            'channel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'default': "'undefined'", 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'db_table': "'dim_productkey'", 'object_name': 'ProductKeyDim'},
            'entrytype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'default': "'48558f7b5064964644c9318196fee6e3'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'"})
        },
        'analysis.subscriberiddim': {
            'Meta': {'db_table': "'dim_subscriberid'", 'object_name': 'SubscriberIdDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'default': "'undefined'"}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'db_table': "'result_sum_activate_productpackage'", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'object_name': 'SumActivateDeviceProductPackageResult', 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductpackageversionresult': {
            'Meta': {'db_table': "'result_sum_activate_productpackageversion'", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'object_name': 'SumActivateDeviceProductPackageVersionResult', 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductresult': {
            'Meta': {'db_table': "'result_sum_activate_product'", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'object_name': 'SumActivateDeviceProductResult', 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumdownloadproductresult': {
            'Meta': {'db_table': "'result_sum_download_product'", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'object_name': 'SumDownloadProductResult', 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"})
        },
        'analysis.usingcountsegmentdim': {
            'Meta': {'db_table': "'dim_usingcountsegment'", 'object_name': 'UsingcountSegmentDim'},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'db_table': "'fact_behaviour'", 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'object_name': 'UsinglogFact', 'ordering': "('-date',)"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'db_table': "'dim_usinglogsegment'", 'object_name': 'UsinglogSegmentDim'},
            'effective_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']