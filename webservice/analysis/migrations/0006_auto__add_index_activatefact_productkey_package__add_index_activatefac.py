# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'ActivateFact', fields ['productkey', 'package']
        db.create_index('fact_activate', ['productkey_id', 'package_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device', 'package']
        db.create_index('fact_activate', ['productkey_id', 'device_id', 'package_id'])


    def backwards(self, orm):
        # Removing index on 'ActivateFact', fields ['productkey', 'device', 'package']
        db.delete_index('fact_activate', ['productkey_id', 'device_id', 'package_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'package']
        db.delete_index('fact_activate', ['productkey_id', 'package_id'])


    models = {
        'analysis.activatefact': {
            'Meta': {'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'))", 'ordering': "('-date',)", 'db_table': "'fact_activate'", 'object_name': 'ActivateFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'object_name': 'ActivateNewReserveFact', 'ordering': "('-date',)", 'db_table': "'fact_activate_newreserve'", '_ormbases': ['analysis.ActivateFact']},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['analysis.ActivateFact']"}),
            'is_new_package': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_package_version': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package_version': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'})
        },
        'analysis.baidupushdim': {
            'Meta': {'object_name': 'BaiduPushDim', 'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'db_table': "'dim_baidupush'"},
            'app_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.datedim': {
            'Meta': {'index_together': "(('year', 'month', 'day'), ('year', 'week'))", 'db_table': "'dim_date'", 'object_name': 'DateDim'},
            'datevalue': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'day': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'dayofweek': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            'week': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'analysis.devicedim': {
            'Meta': {'object_name': 'DeviceDim', 'db_table': "'dim_device'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'object_name': 'DeviceModelDim', 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'db_table': "'dim_devicemodel'"},
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.deviceosdim': {
            'Meta': {'object_name': 'DeviceOSDim', 'unique_together': "(('platform', 'os_version'),)", 'db_table': "'dim_deviceos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'"})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'db_table': "'dim_deviceresolution'", 'object_name': 'DeviceResolutionDim'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'", 'unique': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'default': "'undefined'"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'object_name': 'DeviceSupplierDim', 'db_table': "'dim_devicesupplier'"},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'default': "'undefined'"}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'default': "'unknown'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'default': "'undefined'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'unknown'", 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'unique_together': "(('start_download', 'end_download'),)", 'db_table': "'fact_downloadbeginfinish'", 'object_name': 'DownloadBeginFinishFact'},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.DownloadFact']"})
        },
        'analysis.downloadfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'))", 'db_table': "'fact_download'", 'object_name': 'DownloadFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.eventdim': {
            'Meta': {'object_name': 'EventDim', 'db_table': "'dim_event'"},
            'eventtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.hourdim': {
            'Meta': {'object_name': 'HourDim', 'db_table': "'dim_hour'"},
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'object_name': 'LocationDim', 'unique_together': "(('country', 'region', 'city'),)", 'db_table': "'dim_location'"},
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'default': "'undefined'"})
        },
        'analysis.mediaurldim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'db_table': "'dim_downloadurl'", 'object_name': 'MediaUrlDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'unique': 'True', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'db_table': "'fact_openclose_daily'", 'object_name': 'OpenCloseDailyFact'},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.packagecategorydim': {
            'Meta': {'object_name': 'PackageCategoryDim', 'db_table': "'dim_packagecategory'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'default': "'undefined'"})
        },
        'analysis.packagedim': {
            'Meta': {'object_name': 'PackageDim', 'unique_together': "(('package_name', 'version_name'),)", 'db_table': "'dim_package'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.packagekeydim': {
            'Meta': {'object_name': 'PackageKeyDim', 'db_table': "'dim_packagekey'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.pagedim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'db_table': "'dim_page'", 'object_name': 'PageDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'unique': 'True', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'object_name': 'ProductDim', 'unique_together': "(('entrytype', 'channel'),)", 'db_table': "'dim_product'"},
            'channel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'default': "'undefined'", 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'object_name': 'ProductKeyDim', 'db_table': "'dim_productkey'"},
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True', 'default': "'d72f9cf27effb8566d0e578f7ac93945'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'"})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'default': "'undefined'"}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'db_table': "'result_sum_activate_productpackage'", 'object_name': 'SumActivateDeviceProductPackageResult'},
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
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'db_table': "'result_sum_activate_productpackageversion'", 'object_name': 'SumActivateDeviceProductPackageVersionResult'},
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
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'db_table': "'result_sum_activate_product'", 'object_name': 'SumActivateDeviceProductResult'},
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
        'analysis.usingcountsegmentdim': {
            'Meta': {'object_name': 'UsingcountSegmentDim', 'db_table': "'dim_usingcountsegment'"},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'ordering': "('-date',)", 'db_table': "'fact_behaviour'", 'object_name': 'UsinglogFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'device_supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceSupplierDim']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'object_name': 'UsinglogSegmentDim', 'db_table': "'dim_usinglogsegment'"},
            'effective_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']