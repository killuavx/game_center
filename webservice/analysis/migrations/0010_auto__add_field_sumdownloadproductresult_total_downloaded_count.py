# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SumDownloadProductResult.total_downloaded_count'
        db.add_column('result_sum_download_product', 'total_downloaded_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(max_length=11, default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SumDownloadProductResult.total_downloaded_count'
        db.delete_column('result_sum_download_product', 'total_downloaded_count')


    models = {
        'analysis.activatefact': {
            'Meta': {'object_name': 'ActivateFact', 'ordering': "('-date',)", 'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'))", 'db_table': "'fact_activate'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
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
            'app_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '25'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '25'})
        },
        'analysis.datedim': {
            'Meta': {'object_name': 'DateDim', 'index_together': "(('year', 'month', 'day'), ('year', 'week'))", 'db_table': "'dim_date'"},
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
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '15'})
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
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'object_name': 'DeviceResolutionDim', 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'db_table': "'dim_deviceresolution'"},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '25', 'db_index': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'object_name': 'DeviceSupplierDim', 'db_table': "'dim_devicesupplier'"},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'default': "'unknown'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'unknown'", 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'object_name': 'DownloadBeginFinishFact', 'unique_together': "(('start_download', 'end_download'),)", 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'db_table': "'fact_downloadbeginfinish'"},
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
            'Meta': {'object_name': 'DownloadFact', 'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'db_table': "'fact_download'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
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
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'})
        },
        'analysis.mediaurldim': {
            'Meta': {'object_name': 'MediaUrlDim', 'index_together': "(('host', 'path'),)", 'db_table': "'dim_downloadurl'"},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '1024'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '20'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'object_name': 'OpenCloseDailyFact', 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'db_table': "'fact_openclose_daily'"},
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
            'Meta': {'object_name': 'PackageCategoryDim', 'db_table': "'dim_packagecategory'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '100'})
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
            'package_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.pagedim': {
            'Meta': {'object_name': 'PageDim', 'index_together': "(('host', 'path'),)", 'db_table': "'dim_page'"},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '1024'})
        },
        'analysis.productdim': {
            'Meta': {'object_name': 'ProductDim', 'unique_together': "(('entrytype', 'channel'),)", 'db_table': "'dim_product'"},
            'channel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '50'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'object_name': 'ProductKeyDim', 'db_table': "'dim_productkey'"},
            'entrytype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'a738bbc2dd237d2bc8a1dbf268dd54d6'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'"})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '30'}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'object_name': 'SumActivateDeviceProductPackageResult', 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_activate_productpackage'"},
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
            'Meta': {'object_name': 'SumActivateDeviceProductPackageVersionResult', 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_activate_productpackageversion'"},
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
            'Meta': {'object_name': 'SumActivateDeviceProductResult', 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_activate_product'"},
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
            'Meta': {'object_name': 'SumDownloadProductResult', 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_download_product'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.usingcountsegmentdim': {
            'Meta': {'object_name': 'UsingcountSegmentDim', 'db_table': "'dim_usingcountsegment'"},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'object_name': 'UsinglogFact', 'ordering': "('-date',)", 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'db_table': "'fact_behaviour'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']"}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
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