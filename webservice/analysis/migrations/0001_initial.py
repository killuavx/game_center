# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventDim'
        db.create_table('dim_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eventtype', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('analysis', ['EventDim'])

        # Adding model 'ProductKeyDim'
        db.create_table('dim_productkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=30)),
            ('key', self.gf('django.db.models.fields.CharField')(default='8d273ecc239b721b24a3a455bdd5581c', max_length=40, unique=True)),
            ('entrytype', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('analysis', ['ProductKeyDim'])

        # Adding model 'ProductDim'
        db.create_table('dim_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrytype', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50)),
            ('channel', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=50, blank=True)),
        ))
        db.send_create_signal('analysis', ['ProductDim'])

        # Adding unique constraint on 'ProductDim', fields ['entrytype', 'channel']
        db.create_unique('dim_product', ['entrytype', 'channel'])

        # Adding model 'DateDim'
        db.create_table('dim_date', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datevalue', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=4)),
            ('week', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3)),
            ('month', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2)),
            ('dayofweek', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=1)),
            ('day', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2)),
        ))
        db.send_create_signal('analysis', ['DateDim'])

        # Adding index on 'DateDim', fields ['year', 'month', 'day']
        db.create_index('dim_date', ['year', 'month', 'day'])

        # Adding index on 'DateDim', fields ['year', 'week']
        db.create_index('dim_date', ['year', 'week'])

        # Adding model 'HourDim'
        db.create_table('dim_hour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
        ))
        db.send_create_signal('analysis', ['HourDim'])

        # Adding model 'PackageKeyDim'
        db.create_table('dim_packagekey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('package_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('analysis', ['PackageKeyDim'])

        # Adding model 'PackageCategoryDim'
        db.create_table('dim_packagecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=100, unique=True)),
        ))
        db.send_create_signal('analysis', ['PackageCategoryDim'])

        # Adding model 'PackageDim'
        db.create_table('dim_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('package_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('version_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('analysis', ['PackageDim'])

        # Adding unique constraint on 'PackageDim', fields ['package_name', 'version_name']
        db.create_unique('dim_package', ['package_name', 'version_name'])

        # Adding model 'SubscriberIdDim'
        db.create_table('dim_subscriberid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imsi', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=30, unique=True)),
            ('mnc', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=10)),
        ))
        db.send_create_signal('analysis', ['SubscriberIdDim'])

        # Adding model 'DeviceDim'
        db.create_table('dim_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=20)),
            ('imei', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=25, unique=True)),
        ))
        db.send_create_signal('analysis', ['DeviceDim'])

        # Adding model 'DevicePlatformDim'
        db.create_table('dim_deviceplatform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=20)),
        ))
        db.send_create_signal('analysis', ['DevicePlatformDim'])

        # Adding model 'DeviceOSDim'
        db.create_table('dim_deviceos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=20)),
            ('os_version', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=300)),
        ))
        db.send_create_signal('analysis', ['DeviceOSDim'])

        # Adding unique constraint on 'DeviceOSDim', fields ['platform', 'os_version']
        db.create_unique('dim_deviceos', ['platform', 'os_version'])

        # Adding model 'DeviceResolutionDim'
        db.create_table('dim_deviceresolution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=25)),
            ('orig_resolution', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=25, unique=True)),
            ('orig_width', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10)),
            ('orig_height', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10)),
            ('width', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10)),
            ('height', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10)),
        ))
        db.send_create_signal('analysis', ['DeviceResolutionDim'])

        # Adding index on 'DeviceResolutionDim', fields ['width', 'height']
        db.create_index('dim_deviceresolution', ['width', 'height'])

        # Adding index on 'DeviceResolutionDim', fields ['orig_width', 'orig_height']
        db.create_index('dim_deviceresolution', ['orig_width', 'orig_height'])

        # Adding model 'DeviceModelDim'
        db.create_table('dim_devicemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=300)),
            ('device_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('module_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('model_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('analysis', ['DeviceModelDim'])

        # Adding unique constraint on 'DeviceModelDim', fields ['manufacturer', 'device_name', 'module_name', 'model_name']
        db.create_unique('dim_devicemodel', ['manufacturer', 'device_name', 'module_name', 'model_name'])

        # Adding model 'DeviceSupplierDim'
        db.create_table('dim_devicesupplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, default='unknown', max_length=60)),
            ('mccmnc', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=16, unique=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=10)),
            ('country_name', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=128)),
        ))
        db.send_create_signal('analysis', ['DeviceSupplierDim'])

        # Adding model 'DeviceLanguageDim'
        db.create_table('dim_devicelanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=15, blank=True)),
        ))
        db.send_create_signal('analysis', ['DeviceLanguageDim'])

        # Adding model 'NetworkDim'
        db.create_table('dim_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=20, blank=True)),
        ))
        db.send_create_signal('analysis', ['NetworkDim'])

        # Adding model 'PageDim'
        db.create_table('dim_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('urlvalue', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=1024, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=150)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('query', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('is_url', self.gf('django.db.models.fields.BooleanField')(db_index=True, default=False)),
        ))
        db.send_create_signal('analysis', ['PageDim'])

        # Adding index on 'PageDim', fields ['host', 'path']
        db.create_index('dim_page', ['host', 'path'])

        # Adding model 'MediaUrlDim'
        db.create_table('dim_downloadurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('urlvalue', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=1024, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=150)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('query', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('is_static', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('analysis', ['MediaUrlDim'])

        # Adding index on 'MediaUrlDim', fields ['host', 'path']
        db.create_index('dim_downloadurl', ['host', 'path'])

        # Adding model 'LocationDim'
        db.create_table('dim_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=60)),
            ('region', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=60)),
            ('city', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=60)),
        ))
        db.send_create_signal('analysis', ['LocationDim'])

        # Adding unique constraint on 'LocationDim', fields ['country', 'region', 'city']
        db.create_unique('dim_location', ['country', 'region', 'city'])

        # Adding model 'UsinglogSegmentDim'
        db.create_table('dim_usinglogsegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=50)),
            ('startsecond', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
            ('endsecond', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
            ('effective_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
        ))
        db.send_create_signal('analysis', ['UsinglogSegmentDim'])

        # Adding model 'UsingcountSegmentDim'
        db.create_table('dim_usingcountsegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=50)),
            ('startcount', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
            ('endcount', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=10)),
        ))
        db.send_create_signal('analysis', ['UsingcountSegmentDim'])

        # Adding model 'BaiduPushDim'
        db.create_table('dim_baidupush', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel_id', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=25, blank=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=25, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(db_index=True, default='undefined', max_length=25, blank=True)),
        ))
        db.send_create_signal('analysis', ['BaiduPushDim'])

        # Adding unique constraint on 'BaiduPushDim', fields ['channel_id', 'user_id', 'app_id']
        db.create_unique('dim_baidupush', ['channel_id', 'user_id', 'app_id'])

        # Adding model 'UsinglogFact'
        db.create_table('fact_behaviour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.ProductKeyDim'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.PackageKeyDim'], null=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.LocationDim'], null=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.BaiduPushDim'], null=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('analysis', ['UsinglogFact'])

        # Adding index on 'UsinglogFact', fields ['package', 'date']
        db.create_index('fact_behaviour', ['package_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['package', 'date', 'event']
        db.create_index('fact_behaviour', ['package_id', 'date_id', 'event_id'])

        # Adding index on 'UsinglogFact', fields ['product', 'date']
        db.create_index('fact_behaviour', ['product_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['product', 'date', 'event']
        db.create_index('fact_behaviour', ['product_id', 'date_id', 'event_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'date']
        db.create_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'created_datetime']
        db.create_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'created_datetime'])

        # Adding index on 'UsinglogFact', fields ['packagekey', 'date']
        db.create_index('fact_behaviour', ['packagekey_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['packagekey', 'date', 'event']
        db.create_index('fact_behaviour', ['packagekey_id', 'date_id', 'event_id'])

        # Adding index on 'UsinglogFact', fields ['productkey', 'date']
        db.create_index('fact_behaviour', ['productkey_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['productkey', 'date', 'event']
        db.create_index('fact_behaviour', ['productkey_id', 'date_id', 'event_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'productkey', 'device', 'packagekey', 'date']
        db.create_index('fact_behaviour', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'productkey', 'device', 'packagekey', 'created_datetime']
        db.create_index('fact_behaviour', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'created_datetime'])

        # Adding model 'OpenCloseDailyFact'
        db.create_table('fact_openclose_daily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.ProductKeyDim'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.PackageKeyDim'], null=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('segment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogSegmentDim'])),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('start_usinglog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.UsinglogFact'], unique=True)),
            ('end_usinglog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.UsinglogFact'], unique=True)),
        ))
        db.send_create_signal('analysis', ['OpenCloseDailyFact'])

        # Adding unique constraint on 'OpenCloseDailyFact', fields ['start_usinglog', 'end_usinglog']
        db.create_unique('fact_openclose_daily', ['start_usinglog_id', 'end_usinglog_id'])

        # Adding index on 'OpenCloseDailyFact', fields ['product', 'date', 'segment']
        db.create_index('fact_openclose_daily', ['product_id', 'date_id', 'segment_id'])

        # Adding index on 'OpenCloseDailyFact', fields ['product', 'package', 'date', 'segment']
        db.create_index('fact_openclose_daily', ['product_id', 'package_id', 'date_id', 'segment_id'])

        # Adding index on 'OpenCloseDailyFact', fields ['package', 'device', 'date', 'segment']
        db.create_index('fact_openclose_daily', ['package_id', 'device_id', 'date_id', 'segment_id'])

        # Adding model 'ActivateFact'
        db.create_table('fact_activate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.ProductKeyDim'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.PackageKeyDim'], null=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.LocationDim'], null=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.BaiduPushDim'], null=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('usinglog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.UsinglogFact'], unique=True)),
        ))
        db.send_create_signal('analysis', ['ActivateFact'])

        # Adding index on 'ActivateFact', fields ['device', 'date']
        db.create_index('fact_activate', ['device_id', 'date_id'])

        # Adding index on 'ActivateFact', fields ['package', 'date']
        db.create_index('fact_activate', ['package_id', 'date_id'])

        # Adding index on 'ActivateFact', fields ['device', 'package', 'date']
        db.create_index('fact_activate', ['device_id', 'package_id', 'date_id'])

        # Adding index on 'ActivateFact', fields ['product', 'device']
        db.create_index('fact_activate', ['product_id', 'device_id'])

        # Adding index on 'ActivateFact', fields ['product', 'device', 'package']
        db.create_index('fact_activate', ['product_id', 'device_id', 'package_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device']
        db.create_index('fact_activate', ['productkey_id', 'device_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'packagekey']
        db.create_index('fact_activate', ['productkey_id', 'packagekey_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device', 'packagekey']
        db.create_index('fact_activate', ['productkey_id', 'device_id', 'packagekey_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'package']
        db.create_index('fact_activate', ['productkey_id', 'package_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device', 'package']
        db.create_index('fact_activate', ['productkey_id', 'device_id', 'package_id'])

        # Adding model 'ActivateNewReserveFact'
        db.create_table('fact_activate_newreserve', (
            ('activatefact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, to=orm['analysis.ActivateFact'], unique=True)),
            ('is_new_product', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
            ('is_new_product_channel', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
            ('is_new_product_package', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
            ('is_new_product_package_version', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
            ('is_new_package', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
            ('is_new_package_version', self.gf('analysis.models.ReserveBooleanField')(db_index=True, default=False)),
        ))
        db.send_create_signal('analysis', ['ActivateNewReserveFact'])

        # Adding model 'DownloadFact'
        db.create_table('fact_download', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.ProductKeyDim'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.PackageKeyDim'], null=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PageDim'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.LocationDim'], null=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.BaiduPushDim'], null=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('usinglog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.UsinglogFact'], unique=True)),
            ('download_package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PackageDim'], default=None, null=True)),
            ('download_packagekey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.PackageKeyDim'], default=None, null=True)),
            ('download_url', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.MediaUrlDim'])),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', blank=True, to=orm['analysis.MediaUrlDim'], default=None, null=True)),
        ))
        db.send_create_signal('analysis', ['DownloadFact'])

        # Adding index on 'DownloadFact', fields ['download_package', 'date']
        db.create_index('fact_download', ['download_package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['download_packagekey', 'date']
        db.create_index('fact_download', ['download_packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['package', 'date']
        db.create_index('fact_download', ['package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['packagekey', 'date']
        db.create_index('fact_download', ['packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'package', 'date']
        db.create_index('fact_download', ['event_id', 'package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'packagekey', 'date']
        db.create_index('fact_download', ['event_id', 'packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'date']
        db.create_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'created_datetime']
        db.create_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'created_datetime'])

        # Adding index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date']
        db.create_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime']
        db.create_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'created_datetime'])

        # Adding index on 'DownloadFact', fields ['event', 'productkey']
        db.create_index('fact_download', ['event_id', 'productkey_id'])

        # Adding index on 'DownloadFact', fields ['event', 'product']
        db.create_index('fact_download', ['event_id', 'product_id'])

        # Adding model 'DownloadBeginFinishFact'
        db.create_table('fact_downloadbeginfinish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.ProductKeyDim'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('packagekey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['analysis.PackageKeyDim'], null=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('segment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogSegmentDim'])),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('download_package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.PackageDim'])),
            ('download_url', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.MediaUrlDim'])),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.MediaUrlDim'])),
            ('start_download', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DownloadFact'], unique=True)),
            ('end_download', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DownloadFact'], unique=True)),
        ))
        db.send_create_signal('analysis', ['DownloadBeginFinishFact'])

        # Adding unique constraint on 'DownloadBeginFinishFact', fields ['start_download', 'end_download']
        db.create_unique('fact_downloadbeginfinish', ['start_download_id', 'end_download_id'])

        # Adding index on 'DownloadBeginFinishFact', fields ['download_package', 'date']
        db.create_index('fact_downloadbeginfinish', ['download_package_id', 'date_id'])

        # Adding index on 'DownloadBeginFinishFact', fields ['package', 'date']
        db.create_index('fact_downloadbeginfinish', ['package_id', 'date_id'])

        # Adding index on 'DownloadBeginFinishFact', fields ['product', 'device', 'package', 'download_package', 'date']
        db.create_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Adding index on 'DownloadBeginFinishFact', fields ['product', 'device', 'download_package', 'date']
        db.create_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'download_package_id', 'date_id'])

        # Adding index on 'DownloadBeginFinishFact', fields ['product', 'device', 'package', 'date']
        db.create_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'package_id', 'date_id'])

        # Adding model 'SumActivateDeviceProductResult'
        db.create_table('result_sum_activate_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductResult'])

        # Adding unique constraint on 'SumActivateDeviceProductResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_product', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_product', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'SumActivateDeviceProductPackageResult'
        db.create_table('result_sum_activate_productpackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductPackageResult'])

        # Adding unique constraint on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackage', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackage', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'SumActivateDeviceProductPackageVersionResult'
        db.create_table('result_sum_activate_productpackageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('total_reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('reserve_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('active_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('open_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
        ))
        db.send_create_signal('analysis', ['SumActivateDeviceProductPackageVersionResult'])

        # Adding unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'start_date', 'end_date']
        db.create_unique('result_sum_activate_productpackageversion', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Adding index on 'SumActivateDeviceProductPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        db.create_index('result_sum_activate_productpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Adding model 'SumDownloadProductResult'
        db.create_table('result_sum_download_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cycle_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, max_length=2)),
            ('start_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('end_date', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.DateDim'])),
            ('productkey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['analysis.ProductKeyDim'])),
            ('total_download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('total_downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
            ('downloaded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=11)),
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

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_productpackageversion', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'start_date']
        db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'cycle_type', 'end_date']
        db.delete_index('result_sum_activate_productpackageversion', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageVersionResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackageversion', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_productpackage', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'start_date']
        db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'cycle_type', 'end_date']
        db.delete_index('result_sum_activate_productpackage', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductPackageResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_productpackage', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_product', ['cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date', 'end_date']
        db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id', 'end_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'start_date']
        db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'start_date_id'])

        # Removing index on 'SumActivateDeviceProductResult', fields ['productkey', 'cycle_type', 'end_date']
        db.delete_index('result_sum_activate_product', ['productkey_id', 'cycle_type', 'end_date_id'])

        # Removing unique constraint on 'SumActivateDeviceProductResult', fields ['productkey', 'start_date', 'end_date']
        db.delete_unique('result_sum_activate_product', ['productkey_id', 'start_date_id', 'end_date_id'])

        # Removing index on 'DownloadBeginFinishFact', fields ['product', 'device', 'package', 'date']
        db.delete_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'package_id', 'date_id'])

        # Removing index on 'DownloadBeginFinishFact', fields ['product', 'device', 'download_package', 'date']
        db.delete_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'download_package_id', 'date_id'])

        # Removing index on 'DownloadBeginFinishFact', fields ['product', 'device', 'package', 'download_package', 'date']
        db.delete_index('fact_downloadbeginfinish', ['product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Removing index on 'DownloadBeginFinishFact', fields ['package', 'date']
        db.delete_index('fact_downloadbeginfinish', ['package_id', 'date_id'])

        # Removing index on 'DownloadBeginFinishFact', fields ['download_package', 'date']
        db.delete_index('fact_downloadbeginfinish', ['download_package_id', 'date_id'])

        # Removing unique constraint on 'DownloadBeginFinishFact', fields ['start_download', 'end_download']
        db.delete_unique('fact_downloadbeginfinish', ['start_download_id', 'end_download_id'])

        # Removing index on 'DownloadFact', fields ['event', 'product']
        db.delete_index('fact_download', ['event_id', 'product_id'])

        # Removing index on 'DownloadFact', fields ['event', 'productkey']
        db.delete_index('fact_download', ['event_id', 'productkey_id'])

        # Removing index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime']
        db.delete_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'created_datetime'])

        # Removing index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date']
        db.delete_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'created_datetime']
        db.delete_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'created_datetime'])

        # Removing index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'date']
        db.delete_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['event', 'packagekey', 'date']
        db.delete_index('fact_download', ['event_id', 'packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['event', 'package', 'date']
        db.delete_index('fact_download', ['event_id', 'package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['packagekey', 'date']
        db.delete_index('fact_download', ['packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['package', 'date']
        db.delete_index('fact_download', ['package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['download_packagekey', 'date']
        db.delete_index('fact_download', ['download_packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['download_package', 'date']
        db.delete_index('fact_download', ['download_package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'device', 'package']
        db.delete_index('fact_activate', ['productkey_id', 'device_id', 'package_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'package']
        db.delete_index('fact_activate', ['productkey_id', 'package_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'device', 'packagekey']
        db.delete_index('fact_activate', ['productkey_id', 'device_id', 'packagekey_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'packagekey']
        db.delete_index('fact_activate', ['productkey_id', 'packagekey_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'device']
        db.delete_index('fact_activate', ['productkey_id', 'device_id'])

        # Removing index on 'ActivateFact', fields ['product', 'device', 'package']
        db.delete_index('fact_activate', ['product_id', 'device_id', 'package_id'])

        # Removing index on 'ActivateFact', fields ['product', 'device']
        db.delete_index('fact_activate', ['product_id', 'device_id'])

        # Removing index on 'ActivateFact', fields ['device', 'package', 'date']
        db.delete_index('fact_activate', ['device_id', 'package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['package', 'date']
        db.delete_index('fact_activate', ['package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['device', 'date']
        db.delete_index('fact_activate', ['device_id', 'date_id'])

        # Removing index on 'OpenCloseDailyFact', fields ['package', 'device', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['package_id', 'device_id', 'date_id', 'segment_id'])

        # Removing index on 'OpenCloseDailyFact', fields ['product', 'package', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['product_id', 'package_id', 'date_id', 'segment_id'])

        # Removing index on 'OpenCloseDailyFact', fields ['product', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['product_id', 'date_id', 'segment_id'])

        # Removing unique constraint on 'OpenCloseDailyFact', fields ['start_usinglog', 'end_usinglog']
        db.delete_unique('fact_openclose_daily', ['start_usinglog_id', 'end_usinglog_id'])

        # Removing index on 'UsinglogFact', fields ['event', 'productkey', 'device', 'packagekey', 'created_datetime']
        db.delete_index('fact_behaviour', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'created_datetime'])

        # Removing index on 'UsinglogFact', fields ['event', 'productkey', 'device', 'packagekey', 'date']
        db.delete_index('fact_behaviour', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'date_id'])

        # Removing index on 'UsinglogFact', fields ['productkey', 'date', 'event']
        db.delete_index('fact_behaviour', ['productkey_id', 'date_id', 'event_id'])

        # Removing index on 'UsinglogFact', fields ['productkey', 'date']
        db.delete_index('fact_behaviour', ['productkey_id', 'date_id'])

        # Removing index on 'UsinglogFact', fields ['packagekey', 'date', 'event']
        db.delete_index('fact_behaviour', ['packagekey_id', 'date_id', 'event_id'])

        # Removing index on 'UsinglogFact', fields ['packagekey', 'date']
        db.delete_index('fact_behaviour', ['packagekey_id', 'date_id'])

        # Removing index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'created_datetime']
        db.delete_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'created_datetime'])

        # Removing index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'date']
        db.delete_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'date_id'])

        # Removing index on 'UsinglogFact', fields ['product', 'date', 'event']
        db.delete_index('fact_behaviour', ['product_id', 'date_id', 'event_id'])

        # Removing index on 'UsinglogFact', fields ['product', 'date']
        db.delete_index('fact_behaviour', ['product_id', 'date_id'])

        # Removing index on 'UsinglogFact', fields ['package', 'date', 'event']
        db.delete_index('fact_behaviour', ['package_id', 'date_id', 'event_id'])

        # Removing index on 'UsinglogFact', fields ['package', 'date']
        db.delete_index('fact_behaviour', ['package_id', 'date_id'])

        # Removing unique constraint on 'BaiduPushDim', fields ['channel_id', 'user_id', 'app_id']
        db.delete_unique('dim_baidupush', ['channel_id', 'user_id', 'app_id'])

        # Removing unique constraint on 'LocationDim', fields ['country', 'region', 'city']
        db.delete_unique('dim_location', ['country', 'region', 'city'])

        # Removing index on 'MediaUrlDim', fields ['host', 'path']
        db.delete_index('dim_downloadurl', ['host', 'path'])

        # Removing index on 'PageDim', fields ['host', 'path']
        db.delete_index('dim_page', ['host', 'path'])

        # Removing unique constraint on 'DeviceModelDim', fields ['manufacturer', 'device_name', 'module_name', 'model_name']
        db.delete_unique('dim_devicemodel', ['manufacturer', 'device_name', 'module_name', 'model_name'])

        # Removing index on 'DeviceResolutionDim', fields ['orig_width', 'orig_height']
        db.delete_index('dim_deviceresolution', ['orig_width', 'orig_height'])

        # Removing index on 'DeviceResolutionDim', fields ['width', 'height']
        db.delete_index('dim_deviceresolution', ['width', 'height'])

        # Removing unique constraint on 'DeviceOSDim', fields ['platform', 'os_version']
        db.delete_unique('dim_deviceos', ['platform', 'os_version'])

        # Removing unique constraint on 'PackageDim', fields ['package_name', 'version_name']
        db.delete_unique('dim_package', ['package_name', 'version_name'])

        # Removing index on 'DateDim', fields ['year', 'week']
        db.delete_index('dim_date', ['year', 'week'])

        # Removing index on 'DateDim', fields ['year', 'month', 'day']
        db.delete_index('dim_date', ['year', 'month', 'day'])

        # Removing unique constraint on 'ProductDim', fields ['entrytype', 'channel']
        db.delete_unique('dim_product', ['entrytype', 'channel'])

        # Deleting model 'EventDim'
        db.delete_table('dim_event')

        # Deleting model 'ProductKeyDim'
        db.delete_table('dim_productkey')

        # Deleting model 'ProductDim'
        db.delete_table('dim_product')

        # Deleting model 'DateDim'
        db.delete_table('dim_date')

        # Deleting model 'HourDim'
        db.delete_table('dim_hour')

        # Deleting model 'PackageKeyDim'
        db.delete_table('dim_packagekey')

        # Deleting model 'PackageCategoryDim'
        db.delete_table('dim_packagecategory')

        # Deleting model 'PackageDim'
        db.delete_table('dim_package')

        # Deleting model 'SubscriberIdDim'
        db.delete_table('dim_subscriberid')

        # Deleting model 'DeviceDim'
        db.delete_table('dim_device')

        # Deleting model 'DevicePlatformDim'
        db.delete_table('dim_deviceplatform')

        # Deleting model 'DeviceOSDim'
        db.delete_table('dim_deviceos')

        # Deleting model 'DeviceResolutionDim'
        db.delete_table('dim_deviceresolution')

        # Deleting model 'DeviceModelDim'
        db.delete_table('dim_devicemodel')

        # Deleting model 'DeviceSupplierDim'
        db.delete_table('dim_devicesupplier')

        # Deleting model 'DeviceLanguageDim'
        db.delete_table('dim_devicelanguage')

        # Deleting model 'NetworkDim'
        db.delete_table('dim_network')

        # Deleting model 'PageDim'
        db.delete_table('dim_page')

        # Deleting model 'MediaUrlDim'
        db.delete_table('dim_downloadurl')

        # Deleting model 'LocationDim'
        db.delete_table('dim_location')

        # Deleting model 'UsinglogSegmentDim'
        db.delete_table('dim_usinglogsegment')

        # Deleting model 'UsingcountSegmentDim'
        db.delete_table('dim_usingcountsegment')

        # Deleting model 'BaiduPushDim'
        db.delete_table('dim_baidupush')

        # Deleting model 'UsinglogFact'
        db.delete_table('fact_behaviour')

        # Deleting model 'OpenCloseDailyFact'
        db.delete_table('fact_openclose_daily')

        # Deleting model 'ActivateFact'
        db.delete_table('fact_activate')

        # Deleting model 'ActivateNewReserveFact'
        db.delete_table('fact_activate_newreserve')

        # Deleting model 'DownloadFact'
        db.delete_table('fact_download')

        # Deleting model 'DownloadBeginFinishFact'
        db.delete_table('fact_downloadbeginfinish')

        # Deleting model 'SumActivateDeviceProductResult'
        db.delete_table('result_sum_activate_product')

        # Deleting model 'SumActivateDeviceProductPackageResult'
        db.delete_table('result_sum_activate_productpackage')

        # Deleting model 'SumActivateDeviceProductPackageVersionResult'
        db.delete_table('result_sum_activate_productpackageversion')

        # Deleting model 'SumDownloadProductResult'
        db.delete_table('result_sum_download_product')


    models = {
        'analysis.activatefact': {
            'Meta': {'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'), ('productkey', 'package'), ('productkey', 'device', 'package'))", 'ordering': "('-date',)", 'db_table': "'fact_activate'", 'object_name': 'ActivateFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']", 'null': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']", 'null': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'_ormbases': ['analysis.ActivateFact'], 'ordering': "('-date',)", 'db_table': "'fact_activate_newreserve'", 'object_name': 'ActivateNewReserveFact'},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['analysis.ActivateFact']", 'unique': 'True'}),
            'is_new_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_channel': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_new_product_package_version': ('analysis.models.ReserveBooleanField', [], {'db_index': 'True', 'default': 'False'})
        },
        'analysis.baidupushdim': {
            'Meta': {'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'db_table': "'dim_baidupush'", 'object_name': 'BaiduPushDim'},
            'app_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25', 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25', 'blank': 'True'})
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
            'imei': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '25', 'unique': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'db_table': "'dim_devicelanguage'", 'object_name': 'DeviceLanguageDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '15', 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'db_table': "'dim_devicemodel'", 'object_name': 'DeviceModelDim'},
            'device_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.deviceosdim': {
            'Meta': {'unique_together': "(('platform', 'os_version'),)", 'db_table': "'dim_deviceos'", 'object_name': 'DeviceOSDim'},
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
            'orig_resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25', 'unique': 'True'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'resolution': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '25'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'db_table': "'dim_devicesupplier'", 'object_name': 'DeviceSupplierDim'},
            'country_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'}),
            'country_name': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '16', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'unknown'", 'max_length': '60'})
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
            'Meta': {'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'), ('event', 'productkey'), ('event', 'product'))", 'db_table': "'fact_download'", 'object_name': 'DownloadFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']", 'null': 'True'}),
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PackageDim']", 'default': 'None', 'null': 'True'}),
            'download_packagekey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'default': 'None', 'null': 'True'}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']", 'null': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.MediaUrlDim']", 'default': 'None', 'null': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']", 'unique': 'True'})
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
            'Meta': {'unique_together': "(('country', 'region', 'city'),)", 'db_table': "'dim_location'", 'object_name': 'LocationDim'},
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
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '1024', 'unique': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'db_table': "'dim_network'", 'object_name': 'NetworkDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '20', 'blank': 'True'})
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
            'Meta': {'db_table': "'dim_packagecategory'", 'object_name': 'PackageCategoryDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '100', 'unique': 'True'})
        },
        'analysis.packagedim': {
            'Meta': {'unique_together': "(('package_name', 'version_name'),)", 'db_table': "'dim_package'", 'object_name': 'PackageDim'},
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
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '1024', 'unique': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'unique_together': "(('entrytype', 'channel'),)", 'db_table': "'dim_product'", 'object_name': 'ProductDim'},
            'channel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '50', 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'db_table': "'dim_productkey'", 'object_name': 'ProductKeyDim'},
            'entrytype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'4b349220724328ca46c37189813da1c2'", 'max_length': '40', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30'})
        },
        'analysis.subscriberiddim': {
            'Meta': {'db_table': "'dim_subscriberid'", 'object_name': 'SubscriberIdDim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30', 'unique': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'default': "'undefined'", 'max_length': '10'})
        },
        'analysis.sumactivatedeviceproductpackageresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')", 'db_table': "'result_sum_activate_productpackage'", 'object_name': 'SumActivateDeviceProductPackageResult'},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductpackageversionresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')", 'db_table': "'result_sum_activate_productpackageversion'", 'object_name': 'SumActivateDeviceProductPackageVersionResult'},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumactivatedeviceproductresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')", 'db_table': "'result_sum_activate_product'", 'object_name': 'SumActivateDeviceProductResult'},
            'active_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
            'end_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.ProductKeyDim']"}),
            'reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'}),
            'start_date': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.DateDim']"}),
            'total_reserve_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'analysis.sumdownloadproductresult': {
            'Meta': {'index_together': "(('productkey', 'cycle_type', 'end_date'), ('productkey', 'cycle_type', 'start_date'), ('productkey', 'cycle_type', 'start_date', 'end_date'), ('cycle_type', 'start_date', 'end_date'))", 'unique_together': "(('productkey', 'start_date', 'end_date'),)", 'ordering': "('-start_date', 'productkey')", 'db_table': "'result_sum_download_product'", 'object_name': 'SumDownloadProductResult'},
            'cycle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'max_length': '2'}),
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
            'Meta': {'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('product', 'date'), ('product', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'), ('packagekey', 'date'), ('packagekey', 'date', 'event'), ('productkey', 'date'), ('productkey', 'date', 'event'), ('event', 'productkey', 'device', 'packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'created_datetime'))", 'ordering': "('-date',)", 'db_table': "'fact_behaviour'", 'object_name': 'UsinglogFact'},
            'baidu_push': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.BaiduPushDim']", 'null': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.LocationDim']", 'null': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.PackageKeyDim']", 'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['analysis.ProductKeyDim']", 'null': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']", 'null': 'True'}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'db_table': "'dim_usinglogsegment'", 'object_name': 'UsinglogSegmentDim'},
            'effective_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']