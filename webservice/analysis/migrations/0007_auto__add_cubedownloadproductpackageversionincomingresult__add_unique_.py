# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CubeDownloadProductPackageVersionIncomingResult'
        db.create_table('result_cube_download_productpackageversionincoming', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2, db_index=True)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('total_downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('download_packagekey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageKeyDim'])),
            ('download_package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageDim'])),
        ))
        db.send_create_signal('analysis', ['CubeDownloadProductPackageVersionIncomingResult'])

        # Adding unique constraint on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package']
        db.create_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id'])

        # Adding index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type']
        db.create_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type'])

        # Adding index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date']
        db.create_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_download_productpackageversionincoming', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'CubeDownloadProductPackageIncomingResult'
        db.create_table('result_cube_download_productpackageincoming', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2, db_index=True)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('total_downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('download_packagekey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageKeyDim'])),
        ))
        db.send_create_signal('analysis', ['CubeDownloadProductPackageIncomingResult'])

        # Adding unique constraint on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey']
        db.create_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id'])

        # Adding index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type']
        db.create_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type'])

        # Adding index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date']
        db.create_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeDownloadProductPackageIncomingResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_download_productpackageincoming', ['cycle_type', 'start_date_id', 'end_date_id'])


    def backwards(self, orm):
        # Removing index on 'CubeDownloadProductPackageIncomingResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_download_productpackageincoming', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date']
        #db.delete_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type']
        #db.delete_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type'])

        # Removing index on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey']
        #db.delete_index('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id'])

        # Removing unique constraint on 'CubeDownloadProductPackageIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_cube_download_productpackageincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_download_productpackageversionincoming', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date']
        #db.delete_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type']
        #db.delete_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type'])

        # Removing index on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package']
        #db.delete_index('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id'])

        # Removing unique constraint on 'CubeDownloadProductPackageVersionIncomingResult', fields ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_cube_download_productpackageversionincoming', ['device_platform_id', 'productkey_id', 'download_packagekey_id', 'download_package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Deleting model 'CubeDownloadProductPackageVersionIncomingResult'
        db.delete_table('result_cube_download_productpackageversionincoming')

        # Deleting model 'CubeDownloadProductPackageIncomingResult'
        db.delete_table('result_cube_download_productpackageincoming')


    models = {
        'analysis.activatefact': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'ActivateFact', 'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'), ('device_platform', 'package', 'date'), ('device_platform', 'device', 'package', 'date'), ('device_platform', 'product', 'device'), ('device_platform', 'product', 'device', 'package'), ('device_platform', 'productkey', 'device'), ('device_platform', 'productkey', 'packagekey'), ('device_platform', 'productkey', 'device', 'packagekey'), ('device_platform', 'productkey', 'package'), ('device_platform', 'productkey', 'device', 'package'))", 'db_table': "'fact_activate'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']", 'blank': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']", 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'ActivateNewReserveFact', 'index_together': "(('platform', 'is_new_product'), ('platform', 'is_new_product_channel'), ('platform', 'is_new_product_channel_package'), ('platform', 'is_new_product_channel_package_version'), ('platform', 'is_new_product_package'), ('platform', 'is_new_product_package_version'), ('platform', 'is_new_package'), ('platform', 'is_new_package_version'))", '_ormbases': ['analysis.ActivateFact'], 'db_table': "'fact_activate_newreserve'"},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['analysis.ActivateFact']"}),
            'is_new_package': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_package_version': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_channel': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_channel_package': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_channel_package_version': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_package': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_package_version': ('analysis.models.ReserveBooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'})
        },
        'analysis.baidupushdim': {
            'Meta': {'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'object_name': 'BaiduPushDim', 'db_table': "'dim_baidupush'"},
            'app_id': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'db_index': 'True', 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.cubeactivatedeviceproductchannelpackageresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeActivateDeviceProductChannelPackageResult', 'index_together': "(['device_platform', 'productkey', 'product', 'packagekey'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_activate_productchannelpackage'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubeactivatedeviceproductchannelpackageversionresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeActivateDeviceProductChannelPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_activate_productchannelpackageversion'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubedownloadproductpackageincomingresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageIncomingResult', 'index_together': "(['device_platform', 'productkey', 'download_packagekey'], ['device_platform', 'productkey', 'download_packagekey', 'cycle_type'], ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'download_packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_download_productpackageincoming'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubedownloadproductpackageresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageResult', 'index_together': "(['device_platform', 'productkey', 'packagekey'], ['device_platform', 'productkey', 'packagekey', 'cycle_type'], ['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_download_productpackage'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubedownloadproductpackageversionincomingresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageVersionIncomingResult', 'index_together': "(['device_platform', 'productkey', 'download_packagekey', 'download_package'], ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type'], ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'download_packagekey', 'download_package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_download_productpackageversionincoming'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubedownloadproductpackageversionresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'packagekey', 'package'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_download_productpackageversion'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.cubedownloadproductresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_download_product'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
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
            'imei': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'unique': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'android'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '15', 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'object_name': 'DeviceModelDim', 'db_table': "'dim_devicemodel'"},
            'device_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.deviceosdim': {
            'Meta': {'unique_together': "(('platform', 'os_version'),)", 'object_name': 'DeviceOSDim', 'db_table': "'dim_deviceos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '300'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'android'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'android'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'object_name': 'DeviceResolutionDim', 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'db_table': "'dim_deviceresolution'"},
            'height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'unique': 'True', 'db_index': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'resolution': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'db_index': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'object_name': 'DeviceSupplierDim', 'db_table': "'dim_devicesupplier'"},
            'country_code': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10', 'db_index': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '16', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '60', 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'unique_together': "(('start_download', 'end_download'),)", 'object_name': 'DownloadBeginFinishFact', 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'db_table': "'fact_downloadbeginfinish'"},
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
            'end_download': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.DownloadFact']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.DownloadFact']"})
        },
        'analysis.downloadfact': {
            'Meta': {'object_name': 'DownloadFact', 'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'db_table': "'fact_download'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']", 'blank': 'True'}),
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageDim']", 'blank': 'True'}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']", 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.MediaUrlDim']", 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.eventdim': {
            'Meta': {'object_name': 'EventDim', 'db_table': "'dim_event'"},
            'eventtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.hourdim': {
            'Meta': {'object_name': 'HourDim', 'db_table': "'dim_hour'"},
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'unique_together': "(('country', 'region', 'city'),)", 'object_name': 'LocationDim', 'db_table': "'dim_location'"},
            'city': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '60', 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '60', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '60', 'db_index': 'True'})
        },
        'analysis.mediaurldim': {
            'Meta': {'object_name': 'MediaUrlDim', 'index_together': "(('host', 'path'),)", 'db_table': "'dim_downloadurl'"},
            'host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '1024', 'unique': 'True', 'blank': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '20', 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'object_name': 'OpenCloseDailyFact', 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'db_table': "'fact_openclose_daily'"},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.packagecategorydim': {
            'Meta': {'object_name': 'PackageCategoryDim', 'db_table': "'dim_packagecategory'"},
            'cid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'unique': 'True'})
        },
        'analysis.packagedim': {
            'Meta': {'unique_together': "(('platform', 'package_name', 'version_name'),)", 'object_name': 'PackageDim', 'index_together': "(('platform', 'package_name'),)", 'db_table': "'dim_package'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'android'", 'max_length': '20', 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'second_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vid': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'analysis.packagekeydim': {
            'Meta': {'unique_together': "(('platform', 'package_name'),)", 'object_name': 'PackageKeyDim', 'db_table': "'dim_packagekey'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'android'", 'max_length': '20', 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'second_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.pagedim': {
            'Meta': {'object_name': 'PageDim', 'index_together': "(('host', 'path'),)", 'db_table': "'dim_page'"},
            'host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '1024', 'unique': 'True', 'blank': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'unique_together': "(('entrytype', 'channel'),)", 'object_name': 'ProductDim', 'db_table': "'dim_product'"},
            'channel': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'object_name': 'ProductKeyDim', 'db_table': "'dim_productkey'"},
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'7b27c269ae9e54f10bd2b6f0ad5323ad'", 'max_length': '40', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30'})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30', 'unique': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10', 'db_index': 'True'})
        },
        'analysis.sumactivatedeviceproductchannelpackageresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannelpackage'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductchannelpackageversionresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannelpackageversion'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductchannelresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannel'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productpackage'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductpackageversionresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageVersionResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productpackageversion'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductresult': {
            'Meta': {'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_product'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumdownloadproductresult': {
            'Meta': {'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'object_name': 'SumDownloadProductResult', 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_download_product'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.usingcountsegmentdim': {
            'Meta': {'object_name': 'UsingcountSegmentDim', 'db_table': "'dim_usingcountsegment'"},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'UsinglogFact', 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'db_table': "'fact_behaviour'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.BaiduPushDim']", 'blank': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.LocationDim']", 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'object_name': 'UsinglogSegmentDim', 'db_table': "'dim_usinglogsegment'"},
            'effective_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']