# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CubeActivateDeviceProductChannelPackageVersionResult'
        db.create_table('result_cube_activate_productchannelpackageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.DevicePlatformDim'])),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageKeyDim'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductDim'])),
        ))
        db.send_create_signal('analysis', ['CubeActivateDeviceProductChannelPackageVersionResult'])

        # Adding unique constraint on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package']
        db.create_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type']
        db.create_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date']
        db.create_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_activate_productchannelpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'CubeActivateDeviceProductChannelPackageResult'
        db.create_table('result_cube_activate_productchannelpackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.DevicePlatformDim'])),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageKeyDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductDim'])),
        ))
        db.send_create_signal('analysis', ['CubeActivateDeviceProductChannelPackageResult'])

        # Adding unique constraint on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey']
        db.create_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type']
        db.create_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date']
        db.create_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'CubeActivateDeviceProductChannelPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_cube_activate_productchannelpackage', ['cycle_type', 'start_date_id', 'end_date_id'])


    def backwards(self, orm):
        # Removing index on 'CubeActivateDeviceProductChannelPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_activate_productchannelpackage', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date']
        #db.delete_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type']
        #db.delete_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey']
        #db.delete_index('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id'])

        # Removing unique constraint on 'CubeActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_unique('result_cube_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_activate_productchannelpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date']
        #db.delete_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type']
        #db.delete_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type'])

        # Removing index on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package']
        #db.delete_index('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id'])

        # Removing unique constraint on 'CubeActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_cube_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'packagekey_id', 'package_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Deleting model 'CubeActivateDeviceProductChannelPackageVersionResult'
        db.delete_table('result_cube_activate_productchannelpackageversion')

        # Deleting model 'CubeActivateDeviceProductChannelPackageResult'
        db.delete_table('result_cube_activate_productchannelpackage')


    models = {
        'analysis.activatefact': {
            'Meta': {'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'), ('device_platform', 'package', 'date'), ('device_platform', 'device', 'package', 'date'), ('device_platform', 'product', 'device'), ('device_platform', 'product', 'device', 'package'), ('device_platform', 'productkey', 'device'), ('device_platform', 'productkey', 'packagekey'), ('device_platform', 'productkey', 'device', 'packagekey'), ('device_platform', 'productkey', 'package'), ('device_platform', 'productkey', 'device', 'package'))", 'db_table': "'fact_activate'", 'ordering': "('-date',)", 'object_name': 'ActivateFact'},
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
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'index_together': "(('platform', 'is_new_product'), ('platform', 'is_new_product_channel'), ('platform', 'is_new_product_channel_package'), ('platform', 'is_new_product_channel_package_version'), ('platform', 'is_new_product_package'), ('platform', 'is_new_product_package_version'), ('platform', 'is_new_package'), ('platform', 'is_new_package_version'))", 'db_table': "'fact_activate_newreserve'", 'ordering': "('-date',)", 'object_name': 'ActivateNewReserveFact', '_ormbases': ['analysis.ActivateFact']},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['analysis.ActivateFact']", 'primary_key': 'True'}),
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
            'Meta': {'db_table': "'dim_baidupush'", 'object_name': 'BaiduPushDim', 'unique_together': "(('channel_id', 'user_id', 'app_id'),)"},
            'app_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '25'})
        },
        'analysis.cubeactivatedeviceproductchannelpackageresult': {
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product', 'packagekey'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_activate_productchannelpackage'", 'object_name': 'CubeActivateDeviceProductChannelPackageResult', 'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_cube_activate_productchannelpackageversion'", 'object_name': 'CubeActivateDeviceProductChannelPackageVersionResult', 'unique_together': "(['device_platform', 'productkey', 'product', 'packagekey', 'package', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'db_table': "'dim_device'", 'object_name': 'DeviceDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'db_table': "'dim_devicelanguage'", 'object_name': 'DeviceLanguageDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '15'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'db_table': "'dim_devicemodel'", 'object_name': 'DeviceModelDim', 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)"},
            'device_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.deviceosdim': {
            'Meta': {'db_table': "'dim_deviceos'", 'object_name': 'DeviceOSDim', 'unique_together': "(('platform', 'os_version'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '300'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'db_table': "'dim_deviceplatform'", 'object_name': 'DevicePlatformDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'db_table': "'dim_deviceresolution'", 'object_name': 'DeviceResolutionDim'},
            'height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'db_table': "'dim_devicesupplier'", 'object_name': 'DeviceSupplierDim'},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'}),
            'country_name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'unknown'", 'max_length': '60'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'db_table': "'fact_downloadbeginfinish'", 'object_name': 'DownloadBeginFinishFact', 'unique_together': "(('start_download', 'end_download'),)"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.DownloadFact']"})
        },
        'analysis.downloadfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'db_table': "'fact_download'", 'object_name': 'DownloadFact'},
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'default': 'None', 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'default': 'None', 'to': "orm['analysis.PackageKeyDim']"}),
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
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'default': 'None', 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
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
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'db_table': "'dim_location'", 'object_name': 'LocationDim', 'unique_together': "(('country', 'region', 'city'),)"},
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'})
        },
        'analysis.mediaurldim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'db_table': "'dim_downloadurl'", 'object_name': 'MediaUrlDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '1024'})
        },
        'analysis.networkdim': {
            'Meta': {'db_table': "'dim_network'", 'object_name': 'NetworkDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'db_table': "'fact_openclose_daily'", 'object_name': 'OpenCloseDailyFact', 'unique_together': "(('start_usinglog', 'end_usinglog'),)"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['analysis.ProductKeyDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.packagecategorydim': {
            'Meta': {'db_table': "'dim_packagecategory'", 'object_name': 'PackageCategoryDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '100'})
        },
        'analysis.packagedim': {
            'Meta': {'db_table': "'dim_package'", 'object_name': 'PackageDim', 'unique_together': "(('package_name', 'version_name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.packagekeydim': {
            'Meta': {'db_table': "'dim_packagekey'", 'object_name': 'PackageKeyDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.pagedim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'db_table': "'dim_page'", 'object_name': 'PageDim'},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '1024'})
        },
        'analysis.productdim': {
            'Meta': {'db_table': "'dim_product'", 'object_name': 'ProductDim', 'unique_together': "(('entrytype', 'channel'),)"},
            'channel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True', 'default': "'undefined'", 'max_length': '50'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'db_table': "'dim_productkey'", 'object_name': 'ProductKeyDim'},
            'entrytype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'ddb0fc5fcd4b3aab8b0bdb13e6c3546f'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30'})
        },
        'analysis.subscriberiddim': {
            'Meta': {'db_table': "'dim_subscriberid'", 'object_name': 'SubscriberIdDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '30'}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.sumactivatedeviceproductchannelpackageresult': {
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannelpackage'", 'object_name': 'SumActivateDeviceProductChannelPackageResult', 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannelpackageversion'", 'object_name': 'SumActivateDeviceProductChannelPackageVersionResult', 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productchannel'", 'object_name': 'SumActivateDeviceProductChannelResult', 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productpackage'", 'object_name': 'SumActivateDeviceProductPackageResult', 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductpackageversionresult': {
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_productpackageversion'", 'object_name': 'SumActivateDeviceProductPackageVersionResult', 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductresult': {
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'db_table': "'result_sum_activate_product'", 'object_name': 'SumActivateDeviceProductResult', 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumdownloadproductresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'db_table': "'result_sum_download_product'", 'ordering': "('-start_date', 'productkey')", 'object_name': 'SumDownloadProductResult', 'unique_together': "(('productkey', 'start_date', 'end_date'),)"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.DevicePlatformDim']"}),
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
            'Meta': {'db_table': "'dim_usingcountsegment'", 'object_name': 'UsingcountSegmentDim'},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'db_table': "'fact_behaviour'", 'ordering': "('-date',)", 'object_name': 'UsinglogFact'},
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
            'Meta': {'db_table': "'dim_usinglogsegment'", 'object_name': 'UsinglogSegmentDim'},
            'effective_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']