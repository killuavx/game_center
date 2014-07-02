# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'SumActivateDeviceProductResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_product', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackageversion', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackage', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Adding model 'SumActivateDeviceProductChannelPackageResult'
        db.create_table('result_sum_activate_productchannelpackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductChannelPackageResult'])

        # Adding unique constraint on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product']
        db.create_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        db.create_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Adding index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannelpackage', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'SumActivateDeviceProductChannelPackageVersionResult'
        db.create_table('result_sum_activate_productchannelpackageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductChannelPackageVersionResult'])

        # Adding unique constraint on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product']
        db.create_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        db.create_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Adding index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannelpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'SumActivateDeviceProductChannelResult'
        db.create_table('result_sum_activate_productchannel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductChannelResult'])

        # Adding unique constraint on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product']
        db.create_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id'])

        # Adding index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        db.create_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Adding index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductChannelResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productchannel', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding field 'SumActivateDeviceProductPackageResult.device_platform'
        db.add_column('result_sum_activate_productpackage', 'device_platform',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True),
                      keep_default=False)

        # Adding unique constraint on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'end_date']
        #db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey']
        db.create_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type']
        db.create_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type'])

        # Adding field 'SumDownloadProductResult.device_platform'
        db.add_column('result_sum_download_product', 'device_platform',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True),
                      keep_default=False)

        # Adding field 'SumActivateDeviceProductPackageVersionResult.device_platform'
        db.add_column('result_sum_activate_productpackageversion', 'device_platform',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True),
                      keep_default=False)

        # Adding unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'end_date']
        #db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey']
        db.create_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type']
        db.create_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type'])

        # Adding field 'SumActivateDeviceProductResult.device_platform'
        db.add_column('result_sum_activate_product', 'device_platform',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'], null=True),
                      keep_default=False)

        # Adding unique constraint on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'end_date']
        #db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey']
        db.create_index('result_sum_activate_product', ['device_platform_id', 'productkey_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type']
        db.create_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type'])


    def backwards(self, orm):
        # Removing index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type']
        #db.delete_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey']
        #db.delete_index('result_sum_activate_product', ['device_platform_id', 'productkey_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_unique('result_sum_activate_product', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type']
        #db.delete_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey']
        #db.delete_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackageversion', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type']
        #db.delete_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey']
        #db.delete_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageResult', fields ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackage', ['device_platform_id', 'productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannel', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        #db.delete_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product']
        #db.delete_index('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id'])

        # Removing unique constraint on 'SumActivateDeviceProductChannelResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productchannel', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannelpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        #db.delete_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product']
        #db.delete_index('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id'])

        # Removing unique constraint on 'SumActivateDeviceProductChannelPackageVersionResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productchannelpackageversion', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannelpackage', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        #db.delete_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date']
        #db.delete_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type']
        #db.delete_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type'])

        # Removing index on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product']
        #db.delete_index('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id'])

        # Removing unique constraint on 'SumActivateDeviceProductChannelPackageResult', fields ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productchannelpackage', ['device_platform_id', 'productkey_id', 'product_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Deleting model 'SumActivateDeviceProductChannelPackageResult'
        db.delete_table('result_sum_activate_productchannelpackage')

        # Deleting model 'SumActivateDeviceProductChannelPackageVersionResult'
        db.delete_table('result_sum_activate_productchannelpackageversion')

        # Deleting model 'SumActivateDeviceProductChannelResult'
        db.delete_table('result_sum_activate_productchannel')

        # Deleting field 'SumActivateDeviceProductPackageResult.device_platform'
        db.delete_column('result_sum_activate_productpackage', 'device_platform_id')

        # Adding unique constraint on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackage', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Deleting field 'SumDownloadProductResult.device_platform'
        db.delete_column('result_sum_download_product', 'device_platform_id')

        # Deleting field 'SumActivateDeviceProductPackageVersionResult.device_platform'
        db.delete_column('result_sum_activate_productpackageversion', 'device_platform_id')

        # Adding unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackageversion', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Deleting field 'SumActivateDeviceProductResult.device_platform'
        db.delete_column('result_sum_activate_product', 'device_platform_id')

        # Adding unique constraint on 'SumActivateDeviceProductResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_product', ['productkey_id', 'start_date_id', 'end_date_id'])


    models = {
        'analysis.activatefact': {
            'Meta': {'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'), ('device_platform', 'package', 'date'), ('device_platform', 'device', 'package', 'date'), ('device_platform', 'product', 'device'), ('device_platform', 'product', 'device', 'package'), ('device_platform', 'productkey', 'device'), ('device_platform', 'productkey', 'packagekey'), ('device_platform', 'productkey', 'device', 'packagekey'), ('device_platform', 'productkey', 'package'), ('device_platform', 'productkey', 'device', 'package'))", 'ordering': "('-date',)", 'object_name': 'ActivateFact', 'db_table': "'fact_activate'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.BaiduPushDim']"}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'_ormbases': ['analysis.ActivateFact'], 'index_together': "(('platform', 'is_new_product'), ('platform', 'is_new_product_channel'), ('platform', 'is_new_product_channel_package'), ('platform', 'is_new_product_channel_package_version'), ('platform', 'is_new_product_package'), ('platform', 'is_new_product_package_version'), ('platform', 'is_new_package'), ('platform', 'is_new_package_version'))", 'ordering': "('-date',)", 'object_name': 'ActivateNewReserveFact', 'db_table': "'fact_activate_newreserve'"},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['analysis.ActivateFact']", 'unique': 'True'}),
            'is_new_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']", 'null': 'True'})
        },
        'analysis.baidupushdim': {
            'Meta': {'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'object_name': 'BaiduPushDim', 'db_table': "'dim_baidupush'"},
            'app_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '25'})
        },
        'analysis.datedim': {
            'Meta': {'index_together': "(('year', 'month', 'day'), ('year', 'week'))", 'object_name': 'DateDim', 'db_table': "'dim_date'"},
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
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'unique': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '15'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'object_name': 'DeviceModelDim', 'db_table': "'dim_devicemodel'"},
            'device_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.deviceosdim': {
            'Meta': {'unique_together': "(('platform', 'os_version'),)", 'object_name': 'DeviceOSDim', 'db_table': "'dim_deviceos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '300'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'object_name': 'DeviceResolutionDim', 'db_table': "'dim_deviceresolution'"},
            'height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True', 'unique': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'object_name': 'DeviceSupplierDim', 'db_table': "'dim_devicesupplier'"},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'}),
            'country_name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'default': "'undefined'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'unknown'", 'max_length': '60'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'unique_together': "(('start_download', 'end_download'),)", 'object_name': 'DownloadBeginFinishFact', 'db_table': "'fact_downloadbeginfinish'"},
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
            'end_download': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DownloadFact']", 'unique': 'True'}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DownloadFact']", 'unique': 'True'})
        },
        'analysis.downloadfact': {
            'Meta': {'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'object_name': 'DownloadFact', 'db_table': "'fact_download'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.BaiduPushDim']"}),
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'related_name': "'+'", 'to': "orm['analysis.PackageKeyDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'})
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
            'Meta': {'unique_together': "(('country', 'region', 'city'),)", 'object_name': 'LocationDim', 'db_table': "'dim_location'"},
            'city': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '60'})
        },
        'analysis.mediaurldim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'object_name': 'MediaUrlDim', 'db_table': "'dim_downloadurl'"},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1024', 'default': "'undefined'", 'unique': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'object_name': 'OpenCloseDailyFact', 'db_table': "'fact_openclose_daily'"},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'})
        },
        'analysis.packagecategorydim': {
            'Meta': {'object_name': 'PackageCategoryDim', 'db_table': "'dim_packagecategory'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "'undefined'", 'unique': 'True'})
        },
        'analysis.packagedim': {
            'Meta': {'unique_together': "(('package_name', 'version_name'),)", 'object_name': 'PackageDim', 'db_table': "'dim_package'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.packagekeydim': {
            'Meta': {'object_name': 'PackageKeyDim', 'db_table': "'dim_packagekey'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.pagedim': {
            'Meta': {'index_together': "(('host', 'path'),)", 'object_name': 'PageDim', 'db_table': "'dim_page'"},
            'host': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "''", 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1024', 'default': "'undefined'", 'unique': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'unique_together': "(('entrytype', 'channel'),)", 'object_name': 'ProductDim', 'db_table': "'dim_product'"},
            'channel': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'default': "'undefined'", 'max_length': '50'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'object_name': 'ProductKeyDim', 'db_table': "'dim_productkey'"},
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': "'4090bb1f1481f6b3feeb9cfbe344fa45'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30'})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'", 'unique': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.sumactivatedeviceproductchannelpackageresult': {
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageResult', 'db_table': "'result_sum_activate_productchannelpackage'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelPackageVersionResult', 'db_table': "'result_sum_activate_productchannelpackageversion'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey', 'product'], ['device_platform', 'productkey', 'product', 'cycle_type'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'product', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductChannelResult', 'db_table': "'result_sum_activate_productchannel'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageResult', 'db_table': "'result_sum_activate_productpackage'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductPackageVersionResult', 'db_table': "'result_sum_activate_productpackageversion'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(['device_platform', 'productkey'], ['device_platform', 'productkey', 'cycle_type'], ['device_platform', 'productkey', 'cycle_type', 'start_date'], ['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'], ['cycle_type', 'start_date', 'end_date'])", 'unique_together': "(['device_platform', 'productkey', 'cycle_type', 'start_date', 'end_date'],)", 'object_name': 'SumActivateDeviceProductResult', 'db_table': "'result_sum_activate_product'"},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'ordering': "('-start_date', 'productkey')", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'object_name': 'SumDownloadProductResult', 'db_table': "'result_sum_download_product'"},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'ordering': "('-date',)", 'object_name': 'UsinglogFact', 'db_table': "'fact_behaviour'"},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.BaiduPushDim']"}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'object_name': 'UsinglogSegmentDim', 'db_table': "'dim_usinglogsegment'"},
            'effective_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']