# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PackageDim', fields ['package_name', 'version_name']
        db.delete_unique('dim_package', ['package_name', 'version_name'])

        # Removing unique constraint on 'PackageKeyDim', fields ['package_name']
        db.delete_unique('dim_packagekey', ['package_name'])

        # Adding field 'PackageKeyDim.platform'
        db.add_column('dim_packagekey', 'platform',
                      self.gf('django.db.models.fields.CharField')(max_length=20, default='android', db_index=True),
                      keep_default=False)

        # Adding field 'PackageKeyDim.root_category'
        db.add_column('dim_packagekey', 'root_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageKeyDim.primary_category'
        db.add_column('dim_packagekey', 'primary_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageKeyDim.second_category'
        db.add_column('dim_packagekey', 'second_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageKeyDim.pid'
        db.add_column('dim_packagekey', 'pid',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding index on 'PackageKeyDim', fields ['package_name']
        db.create_index('dim_packagekey', ['package_name'])

        # Adding unique constraint on 'PackageKeyDim', fields ['platform', 'package_name']
        db.create_unique('dim_packagekey', ['platform', 'package_name'])

        # Adding field 'PackageDim.platform'
        db.add_column('dim_package', 'platform',
                      self.gf('django.db.models.fields.CharField')(max_length=20, default='android', db_index=True),
                      keep_default=False)

        # Adding field 'PackageDim.root_category'
        db.add_column('dim_package', 'root_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageDim.primary_category'
        db.add_column('dim_package', 'primary_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageDim.second_category'
        db.add_column('dim_package', 'second_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', to=orm['analysis.PackageCategoryDim']),
                      keep_default=False)

        # Adding field 'PackageDim.pid'
        db.add_column('dim_package', 'pid',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'PackageDim.vid'
        db.add_column('dim_package', 'vid',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding unique constraint on 'PackageDim', fields ['platform', 'package_name', 'version_name']
        db.create_unique('dim_package', ['platform', 'package_name', 'version_name'])

        # Adding index on 'PackageDim', fields ['platform', 'package_name']
        db.create_index('dim_package', ['platform', 'package_name'])

        # Adding field 'PackageCategoryDim.cid'
        db.add_column('dim_packagecategory', 'cid',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing index on 'PackageDim', fields ['platform', 'package_name']
        #db.delete_index('dim_package', ['platform', 'package_name'])

        # Removing unique constraint on 'PackageDim', fields ['platform', 'package_name', 'version_name']
        db.delete_unique('dim_package', ['platform', 'package_name', 'version_name'])

        # Removing unique constraint on 'PackageKeyDim', fields ['platform', 'package_name']
        db.delete_unique('dim_packagekey', ['platform', 'package_name'])

        # Removing index on 'PackageKeyDim', fields ['package_name']
        #db.delete_index('dim_packagekey', ['package_name'])

        # Deleting field 'PackageKeyDim.platform'
        db.delete_column('dim_packagekey', 'platform')

        # Deleting field 'PackageKeyDim.root_category'
        db.delete_column('dim_packagekey', 'root_category_id')

        # Deleting field 'PackageKeyDim.primary_category'
        db.delete_column('dim_packagekey', 'primary_category_id')

        # Deleting field 'PackageKeyDim.second_category'
        db.delete_column('dim_packagekey', 'second_category_id')

        # Deleting field 'PackageKeyDim.pid'
        db.delete_column('dim_packagekey', 'pid')

        # Adding unique constraint on 'PackageKeyDim', fields ['package_name']
        db.create_unique('dim_packagekey', ['package_name'])

        # Deleting field 'PackageDim.platform'
        db.delete_column('dim_package', 'platform')

        # Deleting field 'PackageDim.root_category'
        db.delete_column('dim_package', 'root_category_id')

        # Deleting field 'PackageDim.primary_category'
        db.delete_column('dim_package', 'primary_category_id')

        # Deleting field 'PackageDim.second_category'
        db.delete_column('dim_package', 'second_category_id')

        # Deleting field 'PackageDim.pid'
        db.delete_column('dim_package', 'pid')

        # Deleting field 'PackageDim.vid'
        db.delete_column('dim_package', 'vid')

        # Adding unique constraint on 'PackageDim', fields ['package_name', 'version_name']
        db.create_unique('dim_package', ['package_name', 'version_name'])

        # Deleting field 'PackageCategoryDim.cid'
        db.delete_column('dim_packagecategory', 'cid')


    models = {
        'analysis.activatefact': {
            'Meta': {'db_table': "'fact_activate'", 'ordering': "('-date',)", 'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'), ('device_platform', 'package', 'date'), ('device_platform', 'device', 'package', 'date'), ('device_platform', 'product', 'device'), ('device_platform', 'product', 'device', 'package'), ('device_platform', 'productkey', 'device'), ('device_platform', 'productkey', 'packagekey'), ('device_platform', 'productkey', 'device', 'packagekey'), ('device_platform', 'productkey', 'package'), ('device_platform', 'productkey', 'device', 'package'))", 'object_name': 'ActivateFact'},
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
            'Meta': {'db_table': "'fact_activate_newreserve'", 'ordering': "('-date',)", '_ormbases': ['analysis.ActivateFact'], 'index_together': "(('platform', 'is_new_product'), ('platform', 'is_new_product_channel'), ('platform', 'is_new_product_channel_package'), ('platform', 'is_new_product_channel_package_version'), ('platform', 'is_new_product_package'), ('platform', 'is_new_product_package_version'), ('platform', 'is_new_package'), ('platform', 'is_new_package_version'))", 'object_name': 'ActivateNewReserveFact'},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['analysis.ActivateFact']"}),
            'is_new_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"})
        },
        'analysis.baidupushdim': {
            'Meta': {'db_table': "'dim_baidupush'", 'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'object_name': 'BaiduPushDim'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.cubeactivatedeviceproductchannelpackageresult': {
            'Meta': {'db_table': "'result_cube_activate_productchannelpackage'", 'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeActivateDeviceProductChannelPackageResult', 'index_together': "(['device_platform', 'productkey', 'product', 'packagekey'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.cubeactivatedeviceproductchannelpackageversionresult': {
            'Meta': {'db_table': "'result_cube_activate_productchannelpackageversion'", 'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeActivateDeviceProductChannelPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.cubedownloadproductpackageresult': {
            'Meta': {'db_table': "'result_cube_download_productpackage'", 'unique_together': "(['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageResult', 'index_together': "(['device_platform', 'productkey', 'packagekey'], ['device_platform', 'productkey', 'packagekey', 'cycle_type'], ['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.cubedownloadproductpackageversionresult': {
            'Meta': {'db_table': "'result_cube_download_productpackageversion'", 'unique_together': "(['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'packagekey', 'package'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.cubedownloadproductresult': {
            'Meta': {'db_table': "'result_cube_download_product'", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'CubeDownloadProductResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'total_downloaded_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
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
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'unique': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'db_table': "'dim_devicelanguage'", 'object_name': 'DeviceLanguageDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'db_table': "'dim_devicemodel'", 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'object_name': 'DeviceModelDim'},
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.deviceosdim': {
            'Meta': {'db_table': "'dim_deviceos'", 'unique_together': "(('platform', 'os_version'),)", 'object_name': 'DeviceOSDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '300', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'db_table': "'dim_deviceplatform'", 'object_name': 'DevicePlatformDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'db_table': "'dim_deviceresolution'", 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'object_name': 'DeviceResolutionDim'},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'unique': 'True', 'db_index': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'db_table': "'dim_devicesupplier'", 'object_name': 'DeviceSupplierDim'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'", 'db_index': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'default': "'unknown'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'default': "'undefined'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'unknown'", 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'db_table': "'fact_downloadbeginfinish'", 'unique_together': "(('start_download', 'end_download'),)", 'object_name': 'DownloadBeginFinishFact', 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))"},
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
            'Meta': {'db_table': "'fact_download'", 'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'object_name': 'DownloadFact'},
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageDim']", 'default': 'None', 'blank': 'True'}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'default': 'None', 'blank': 'True'}),
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
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.MediaUrlDim']", 'default': 'None', 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['analysis.PageDim']", 'blank': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.eventdim': {
            'Meta': {'db_table': "'dim_event'", 'object_name': 'EventDim'},
            'eventtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.hourdim': {
            'Meta': {'db_table': "'dim_hour'", 'object_name': 'HourDim'},
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'db_table': "'dim_location'", 'unique_together': "(('country', 'region', 'city'),)", 'object_name': 'LocationDim'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.mediaurldim': {
            'Meta': {'db_table': "'dim_downloadurl'", 'index_together': "(('host', 'path'),)", 'object_name': 'MediaUrlDim'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150', 'default': "''", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "'undefined'", 'unique': 'True', 'blank': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'db_table': "'dim_network'", 'object_name': 'NetworkDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'db_table': "'fact_openclose_daily'", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'object_name': 'OpenCloseDailyFact', 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))"},
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
            'Meta': {'db_table': "'dim_packagecategory'", 'object_name': 'PackageCategoryDim'},
            'cid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'", 'unique': 'True'})
        },
        'analysis.packagedim': {
            'Meta': {'db_table': "'dim_package'", 'unique_together': "(('platform', 'package_name', 'version_name'),)", 'object_name': 'PackageDim', 'index_together': "(('platform', 'package_name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'second_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vid': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'analysis.packagekeydim': {
            'Meta': {'db_table': "'dim_packagekey'", 'unique_together': "(('platform', 'package_name'),)", 'object_name': 'PackageKeyDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'second_category': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageCategoryDim']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.pagedim': {
            'Meta': {'db_table': "'dim_page'", 'index_together': "(('host', 'path'),)", 'object_name': 'PageDim'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150', 'default': "''", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': "'undefined'", 'unique': 'True', 'blank': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'db_table': "'dim_product'", 'unique_together': "(('entrytype', 'channel'),)", 'object_name': 'ProductDim'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True', 'default': "'undefined'", 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'db_table': "'dim_productkey'", 'object_name': 'ProductKeyDim'},
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': "'b7329f04291db2fe95933d85f59d2f50'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'"})
        },
        'analysis.subscriberiddim': {
            'Meta': {'db_table': "'dim_subscriberid'", 'object_name': 'SubscriberIdDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'", 'unique': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.sumactivatedeviceproductchannelpackageresult': {
            'Meta': {'db_table': "'result_sum_activate_productchannelpackage'", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductchannelpackageversionresult': {
            'Meta': {'db_table': "'result_sum_activate_productchannelpackageversion'", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageVersionResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductchannelresult': {
            'Meta': {'db_table': "'result_sum_activate_productchannel'", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelResult', 'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'db_table': "'result_sum_activate_productpackage'", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductpackageversionresult': {
            'Meta': {'db_table': "'result_sum_activate_productpackageversion'", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageVersionResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumactivatedeviceproductresult': {
            'Meta': {'db_table': "'result_sum_activate_product'", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductResult', 'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'default': '0'})
        },
        'analysis.sumdownloadproductresult': {
            'Meta': {'db_table': "'result_sum_download_product'", 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'object_name': 'SumDownloadProductResult', 'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'db_table': "'dim_usingcountsegment'", 'object_name': 'UsingcountSegmentDim'},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'db_table': "'fact_behaviour'", 'ordering': "('-date',)", 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'object_name': 'UsinglogFact'},
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