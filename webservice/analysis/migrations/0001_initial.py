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

        # Adding model 'ProductDim'
        db.create_table('dim_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrytype', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=50, db_index=True)),
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
            ('hour', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2, db_index=True)),
        ))
        db.send_create_signal('analysis', ['HourDim'])

        # Adding model 'PackageDim'
        db.create_table('dim_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('analysis', ['PackageDim'])

        # Adding unique constraint on 'PackageDim', fields ['package_name', 'version_name']
        db.create_unique('dim_package', ['package_name', 'version_name'])

        # Adding model 'SubscriberIdDim'
        db.create_table('dim_subscriberid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imsi', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=30, unique=True)),
            ('mnc', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10, db_index=True)),
        ))
        db.send_create_signal('analysis', ['SubscriberIdDim'])

        # Adding model 'DeviceDim'
        db.create_table('dim_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=20, db_index=True)),
            ('imei', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=25, unique=True)),
        ))
        db.send_create_signal('analysis', ['DeviceDim'])

        # Adding model 'DevicePlatformDim'
        db.create_table('dim_deviceplatform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=20, db_index=True)),
        ))
        db.send_create_signal('analysis', ['DevicePlatformDim'])

        # Adding model 'DeviceOSDim'
        db.create_table('dim_deviceos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('platform', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=20, db_index=True)),
            ('os_version', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=50)),
        ))
        db.send_create_signal('analysis', ['DeviceOSDim'])

        # Adding unique constraint on 'DeviceOSDim', fields ['platform', 'os_version']
        db.create_unique('dim_deviceos', ['platform', 'os_version'])

        # Adding model 'DeviceResolutionDim'
        db.create_table('dim_deviceresolution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=25, db_index=True)),
            ('orig_resolution', self.gf('django.db.models.fields.CharField')(unique=True, default='undefined', max_length=25, db_index=True)),
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
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=150, db_index=True)),
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
            ('country_code', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=10, db_index=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=128)),
        ))
        db.send_create_signal('analysis', ['DeviceSupplierDim'])

        # Adding model 'DeviceLanguageDim'
        db.create_table('dim_devicelanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=15, db_index=True)),
        ))
        db.send_create_signal('analysis', ['DeviceLanguageDim'])

        # Adding model 'NetworkDim'
        db.create_table('dim_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=20, db_index=True)),
        ))
        db.send_create_signal('analysis', ['NetworkDim'])

        # Adding model 'PageDim'
        db.create_table('dim_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('urlvalue', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=1024, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(default='', max_length=150, db_index=True)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('query', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('is_url', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('analysis', ['PageDim'])

        # Adding index on 'PageDim', fields ['host', 'path']
        db.create_index('dim_page', ['host', 'path'])

        # Adding model 'MediaUrlDim'
        db.create_table('dim_downloadurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('urlvalue', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=1024, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(default='', max_length=150, db_index=True)),
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
            ('country', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=60, db_index=True)),
            ('region', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=60, db_index=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=60, db_index=True)),
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
            ('channel_id', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=25, db_index=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=25, db_index=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(blank=True, default='undefined', max_length=25, db_index=True)),
        ))
        db.send_create_signal('analysis', ['BaiduPushDim'])

        # Adding unique constraint on 'BaiduPushDim', fields ['channel_id', 'user_id', 'app_id']
        db.create_unique('dim_baidupush', ['channel_id', 'user_id', 'app_id'])

        # Adding model 'UsinglogFact'
        db.create_table('fact_behaviour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.LocationDim'])),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.BaiduPushDim'])),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('analysis', ['UsinglogFact'])

        # Adding index on 'UsinglogFact', fields ['package', 'date']
        db.create_index('fact_behaviour', ['package_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['package', 'date', 'event']
        db.create_index('fact_behaviour', ['package_id', 'date_id', 'event_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'date']
        db.create_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'date_id'])

        # Adding index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'created_datetime']
        db.create_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'created_datetime'])

        # Adding model 'OpenCloseDailyFact'
        db.create_table('fact_openclose_daily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
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
            ('start_usinglog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogFact'], related_name='+', unique=True)),
            ('end_usinglog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogFact'], related_name='+', unique=True)),
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
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.LocationDim'])),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.BaiduPushDim'])),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('usinglog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogFact'], related_name='+', unique=True)),
            ('is_new_device', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_device_package', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_device_package_version', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('analysis', ['ActivateFact'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device']
        db.create_index('fact_activate', ['device_id', 'is_new_device'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device_package']
        db.create_index('fact_activate', ['device_id', 'is_new_device_package'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device_package_version']
        db.create_index('fact_activate', ['device_id', 'is_new_device_package_version'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device']
        db.create_index('fact_activate', ['date_id', 'is_new_device'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device_package']
        db.create_index('fact_activate', ['date_id', 'is_new_device_package'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device_package_version']
        db.create_index('fact_activate', ['date_id', 'is_new_device_package_version'])

        # Adding index on 'ActivateFact', fields ['device', 'date']
        db.create_index('fact_activate', ['device_id', 'date_id'])

        # Adding index on 'ActivateFact', fields ['package', 'date']
        db.create_index('fact_activate', ['package_id', 'date_id'])

        # Adding index on 'ActivateFact', fields ['device', 'package', 'date']
        db.create_index('fact_activate', ['device_id', 'package_id', 'date_id'])

        # Adding model 'DownloadFact'
        db.create_table('fact_download', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceDim'])),
            ('date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DateDim'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.HourDim'])),
            ('device_os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceOSDim'])),
            ('device_platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DevicePlatformDim'])),
            ('device_resolution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceResolutionDim'])),
            ('device_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceModelDim'])),
            ('device_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceLanguageDim'])),
            ('doc_id', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.EventDim'])),
            ('subscriberid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.SubscriberIdDim'])),
            ('device_supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DeviceSupplierDim'])),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PageDim'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.LocationDim'])),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.NetworkDim'])),
            ('baidu_push', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.BaiduPushDim'])),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('usinglog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.UsinglogFact'], related_name='+', unique=True)),
            ('download_package', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, related_name='+', to=orm['analysis.PackageDim'])),
            ('download_url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MediaUrlDim'], related_name='+')),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MediaUrlDim'], related_name='+')),
        ))
        db.send_create_signal('analysis', ['DownloadFact'])

        # Adding index on 'DownloadFact', fields ['download_package', 'date']
        db.create_index('fact_download', ['download_package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['package', 'date']
        db.create_index('fact_download', ['package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'package', 'date']
        db.create_index('fact_download', ['event_id', 'package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'date']
        db.create_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'created_datetime']
        db.create_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'created_datetime'])

        # Adding model 'DownloadBeginFinishFact'
        db.create_table('fact_downloadbeginfinish', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.ProductDim'])),
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
            ('download_package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.PackageDim'], related_name='+')),
            ('download_url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MediaUrlDim'], related_name='+')),
            ('redirect_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.MediaUrlDim'], related_name='+')),
            ('start_download', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DownloadFact'], related_name='+', unique=True)),
            ('end_download', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analysis.DownloadFact'], related_name='+', unique=True)),
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


    def backwards(self, orm):
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

        # Removing index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'created_datetime']
        db.delete_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'created_datetime'])

        # Removing index on 'DownloadFact', fields ['event', 'product', 'device', 'package', 'download_package', 'date']
        db.delete_index('fact_download', ['event_id', 'product_id', 'device_id', 'package_id', 'download_package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['event', 'package', 'date']
        db.delete_index('fact_download', ['event_id', 'package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['package', 'date']
        db.delete_index('fact_download', ['package_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['download_package', 'date']
        db.delete_index('fact_download', ['download_package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['device', 'package', 'date']
        db.delete_index('fact_activate', ['device_id', 'package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['package', 'date']
        db.delete_index('fact_activate', ['package_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['device', 'date']
        db.delete_index('fact_activate', ['device_id', 'date_id'])

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device_package_version']
        db.delete_index('fact_activate', ['date_id', 'is_new_device_package_version'])

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device_package']
        db.delete_index('fact_activate', ['date_id', 'is_new_device_package'])

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device']
        db.delete_index('fact_activate', ['date_id', 'is_new_device'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device_package_version']
        db.delete_index('fact_activate', ['device_id', 'is_new_device_package_version'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device_package']
        db.delete_index('fact_activate', ['device_id', 'is_new_device_package'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device']
        db.delete_index('fact_activate', ['device_id', 'is_new_device'])

        # Removing index on 'OpenCloseDailyFact', fields ['package', 'device', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['package_id', 'device_id', 'date_id', 'segment_id'])

        # Removing index on 'OpenCloseDailyFact', fields ['product', 'package', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['product_id', 'package_id', 'date_id', 'segment_id'])

        # Removing index on 'OpenCloseDailyFact', fields ['product', 'date', 'segment']
        db.delete_index('fact_openclose_daily', ['product_id', 'date_id', 'segment_id'])

        # Removing unique constraint on 'OpenCloseDailyFact', fields ['start_usinglog', 'end_usinglog']
        db.delete_unique('fact_openclose_daily', ['start_usinglog_id', 'end_usinglog_id'])

        # Removing index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'created_datetime']
        db.delete_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'created_datetime'])

        # Removing index on 'UsinglogFact', fields ['event', 'product', 'device', 'package', 'date']
        db.delete_index('fact_behaviour', ['event_id', 'product_id', 'device_id', 'package_id', 'date_id'])

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

        # Deleting model 'ProductDim'
        db.delete_table('dim_product')

        # Deleting model 'DateDim'
        db.delete_table('dim_date')

        # Deleting model 'HourDim'
        db.delete_table('dim_hour')

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

        # Deleting model 'DownloadFact'
        db.delete_table('fact_download')

        # Deleting model 'DownloadBeginFinishFact'
        db.delete_table('fact_downloadbeginfinish')


    models = {
        'analysis.activatefact': {
            'Meta': {'object_name': 'ActivateFact', 'index_together': "(('device', 'is_new_device'), ('device', 'is_new_device_package'), ('device', 'is_new_device_package_version'), ('date', 'is_new_device'), ('date', 'is_new_device_package'), ('date', 'is_new_device_package_version'), ('device', 'date'), ('package', 'date'), ('device', 'package', 'date'))", 'db_table': "'fact_activate'"},
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
            'is_new_device': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_device_package': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_device_package_version': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogFact']", 'related_name': "'+'", 'unique': 'True'})
        },
        'analysis.baidupushdim': {
            'Meta': {'object_name': 'BaiduPushDim', 'unique_together': "(('channel_id', 'user_id', 'app_id'),)", 'db_table': "'dim_baidupush'"},
            'app_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '25', 'db_index': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '25', 'db_index': 'True'})
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
            'platform': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '15', 'db_index': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'object_name': 'DeviceModelDim', 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)", 'db_table': "'dim_devicemodel'"},
            'device_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'module_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'analysis.deviceosdim': {
            'Meta': {'object_name': 'DeviceOSDim', 'unique_together': "(('platform', 'os_version'),)", 'db_table': "'dim_deviceos'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'object_name': 'DeviceResolutionDim', 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))", 'db_table': "'dim_deviceresolution'"},
            'height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10'}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '25', 'db_index': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'unknown'", 'max_length': '60'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'object_name': 'DownloadBeginFinishFact', 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))", 'unique_together': "(('start_download', 'end_download'),)", 'db_table': "'fact_downloadbeginfinish'"},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']", 'related_name': "'+'"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MediaUrlDim']", 'related_name': "'+'"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_download': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DownloadFact']", 'related_name': "'+'", 'unique': 'True'}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MediaUrlDim']", 'related_name': "'+'"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DownloadFact']", 'related_name': "'+'", 'unique': 'True'})
        },
        'analysis.downloadfact': {
            'Meta': {'object_name': 'DownloadFact', 'index_together': "(('download_package', 'date'), ('package', 'date'), ('event', 'package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'))", 'db_table': "'fact_download'"},
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
            'download_package': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PackageDim']"}),
            'download_url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MediaUrlDim']", 'related_name': "'+'"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.EventDim']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.LocationDim']"}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.NetworkDim']"}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.MediaUrlDim']", 'related_name': "'+'"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogFact']", 'related_name': "'+'", 'unique': 'True'})
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
            'Meta': {'object_name': 'LocationDim', 'unique_together': "(('country', 'region', 'city'),)", 'db_table': "'dim_location'"},
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
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '1024', 'unique': 'True'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '20', 'db_index': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'object_name': 'OpenCloseDailyFact', 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'db_table': "'fact_openclose_daily'"},
            'date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DateDim']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceDim']"}),
            'device_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceLanguageDim']"}),
            'device_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceModelDim']"}),
            'device_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceOSDim']"}),
            'device_platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DevicePlatformDim']"}),
            'device_resolution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.DeviceResolutionDim']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'end_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogFact']", 'related_name': "'+'", 'unique': 'True'}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.HourDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.PackageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_usinglog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogFact']", 'related_name': "'+'", 'unique': 'True'})
        },
        'analysis.packagedim': {
            'Meta': {'object_name': 'PackageDim', 'unique_together': "(('package_name', 'version_name'),)", 'db_table': "'dim_package'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.pagedim': {
            'Meta': {'object_name': 'PageDim', 'index_together': "(('host', 'path'),)", 'db_table': "'dim_page'"},
            'host': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '1024', 'unique': 'True'})
        },
        'analysis.productdim': {
            'Meta': {'object_name': 'ProductDim', 'unique_together': "(('entrytype', 'channel'),)", 'db_table': "'dim_product'"},
            'channel': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'undefined'", 'max_length': '50', 'db_index': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '30', 'unique': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '10', 'db_index': 'True'})
        },
        'analysis.usingcountsegmentdim': {
            'Meta': {'object_name': 'UsingcountSegmentDim', 'db_table': "'dim_usingcountsegment'"},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '50'}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'object_name': 'UsinglogFact', 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'))", 'db_table': "'fact_behaviour'"},
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
            'page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
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