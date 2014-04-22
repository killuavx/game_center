# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductKeyDim'
        db.create_table('dim_productkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, default='undefined')),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, default='d408c3ae130b803a63ea1456b59a681f', max_length=40)),
            ('entrytype', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('analysis', ['ProductKeyDim'])

        # Adding model 'PackageKeyDim'
        db.create_table('dim_packagekey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, default='')),
            ('package_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('analysis', ['PackageKeyDim'])

        # Adding M2M table for field categories on 'PackageKeyDim'
        m2m_table_name = db.shorten_name('dim_packagekey_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packagekeydim', models.ForeignKey(orm['analysis.packagekeydim'], null=False)),
            ('packagecategorydim', models.ForeignKey(orm['analysis.packagecategorydim'], null=False))
        ))
        db.create_unique(m2m_table_name, ['packagekeydim_id', 'packagecategorydim_id'])

        # Adding model 'ActivateNewReserveFact'
        db.create_table('fact_activate_newreserve', (
            ('activatefact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['analysis.ActivateFact'], primary_key=True)),
            ('is_new_product', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_product_channel', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_product_package', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_product_package_version', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_package', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_new_package_version', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('analysis', ['ActivateNewReserveFact'])

        # Adding model 'PackageCategoryDim'
        db.create_table('dim_packagecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, default='undefined')),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, default='undefined', max_length=100)),
        ))
        db.send_create_signal('analysis', ['PackageCategoryDim'])

        # Adding field 'OpenCloseDailyFact.productkey'
        db.add_column('fact_openclose_daily', 'productkey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.ProductKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'OpenCloseDailyFact.packagekey'
        db.add_column('fact_openclose_daily', 'packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.PackageKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'DownloadBeginFinishFact.productkey'
        db.add_column('fact_downloadbeginfinish', 'productkey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.ProductKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'DownloadBeginFinishFact.packagekey'
        db.add_column('fact_downloadbeginfinish', 'packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.PackageKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'DownloadFact.productkey'
        db.add_column('fact_download', 'productkey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.ProductKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'DownloadFact.packagekey'
        db.add_column('fact_download', 'packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.PackageKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'DownloadFact.download_packagekey'
        db.add_column('fact_download', 'download_packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='+', blank=True, to=orm['analysis.PackageKeyDim']),
                      keep_default=False)

        # Adding index on 'DownloadFact', fields ['download_packagekey', 'date']
        db.create_index('fact_download', ['download_packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date']
        db.create_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['packagekey', 'date']
        db.create_index('fact_download', ['packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'packagekey', 'date']
        db.create_index('fact_download', ['event_id', 'packagekey_id', 'date_id'])

        # Adding index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime']
        db.create_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'created_datetime'])

        # Adding index on 'PackageDim', fields ['package_name']
        db.create_index('dim_package', ['package_name'])

        # Adding field 'UsinglogFact.productkey'
        db.add_column('fact_behaviour', 'productkey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.ProductKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'UsinglogFact.packagekey'
        db.add_column('fact_behaviour', 'packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.PackageKeyDim'], blank=True),
                      keep_default=False)

        # Deleting field 'ActivateFact.is_new_device_package'
        db.delete_column('fact_activate', 'is_new_device_package')

        # Deleting field 'ActivateFact.is_new_device_package_version'
        db.delete_column('fact_activate', 'is_new_device_package_version')

        # Deleting field 'ActivateFact.is_new_device'
        db.delete_column('fact_activate', 'is_new_device')

        # Adding field 'ActivateFact.productkey'
        db.add_column('fact_activate', 'productkey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.ProductKeyDim'], blank=True),
                      keep_default=False)

        # Adding field 'ActivateFact.packagekey'
        db.add_column('fact_activate', 'packagekey',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['analysis.PackageKeyDim'], blank=True),
                      keep_default=False)

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device']
        #db.delete_index('fact_activate', ['date_id', 'is_new_device'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device_package']
        #db.delete_index('fact_activate', ['device_id', 'is_new_device_package'])

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device_package_version']
        #db.delete_index('fact_activate', ['date_id', 'is_new_device_package_version'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device']
        #db.delete_index('fact_activate', ['device_id', 'is_new_device'])

        # Removing index on 'ActivateFact', fields ['date', 'is_new_device_package']
        #db.delete_index('fact_activate', ['date_id', 'is_new_device_package'])

        # Removing index on 'ActivateFact', fields ['device', 'is_new_device_package_version']
        #db.delete_index('fact_activate', ['device_id', 'is_new_device_package_version'])

        # Adding index on 'ActivateFact', fields ['productkey', 'packagekey']
        db.create_index('fact_activate', ['productkey_id', 'packagekey_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device', 'packagekey']
        db.create_index('fact_activate', ['productkey_id', 'device_id', 'packagekey_id'])

        # Adding index on 'ActivateFact', fields ['product', 'device']
        db.create_index('fact_activate', ['product_id', 'device_id'])

        # Adding index on 'ActivateFact', fields ['product', 'device', 'package']
        db.create_index('fact_activate', ['product_id', 'device_id', 'package_id'])

        # Adding index on 'ActivateFact', fields ['productkey', 'device']
        db.create_index('fact_activate', ['productkey_id', 'device_id'])


    def backwards(self, orm):
        # Removing index on 'ActivateFact', fields ['productkey', 'device']
        db.delete_index('fact_activate', ['productkey_id', 'device_id'])

        # Removing index on 'ActivateFact', fields ['product', 'device', 'package']
        db.delete_index('fact_activate', ['product_id', 'device_id', 'package_id'])

        # Removing index on 'ActivateFact', fields ['product', 'device']
        db.delete_index('fact_activate', ['product_id', 'device_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'device', 'packagekey']
        db.delete_index('fact_activate', ['productkey_id', 'device_id', 'packagekey_id'])

        # Removing index on 'ActivateFact', fields ['productkey', 'packagekey']
        db.delete_index('fact_activate', ['productkey_id', 'packagekey_id'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device_package_version']
        db.create_index('fact_activate', ['device_id', 'is_new_device_package_version'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device_package']
        db.create_index('fact_activate', ['date_id', 'is_new_device_package'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device']
        db.create_index('fact_activate', ['device_id', 'is_new_device'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device_package_version']
        db.create_index('fact_activate', ['date_id', 'is_new_device_package_version'])

        # Adding index on 'ActivateFact', fields ['device', 'is_new_device_package']
        db.create_index('fact_activate', ['device_id', 'is_new_device_package'])

        # Adding index on 'ActivateFact', fields ['date', 'is_new_device']
        db.create_index('fact_activate', ['date_id', 'is_new_device'])

        # Removing index on 'PackageDim', fields ['package_name']
        db.delete_index('dim_package', ['package_name'])

        # Removing index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime']
        db.delete_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'created_datetime'])

        # Removing index on 'DownloadFact', fields ['event', 'packagekey', 'date']
        db.delete_index('fact_download', ['event_id', 'packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['packagekey', 'date']
        db.delete_index('fact_download', ['packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date']
        db.delete_index('fact_download', ['event_id', 'productkey_id', 'device_id', 'packagekey_id', 'download_packagekey_id', 'date_id'])

        # Removing index on 'DownloadFact', fields ['download_packagekey', 'date']
        db.delete_index('fact_download', ['download_packagekey_id', 'date_id'])

        # Deleting model 'ProductKeyDim'
        db.delete_table('dim_productkey')

        # Deleting model 'PackageKeyDim'
        db.delete_table('dim_packagekey')

        # Removing M2M table for field categories on 'PackageKeyDim'
        db.delete_table(db.shorten_name('dim_packagekey_categories'))

        # Deleting model 'ActivateNewReserveFact'
        db.delete_table('fact_activate_newreserve')

        # Deleting model 'PackageCategoryDim'
        db.delete_table('dim_packagecategory')

        # Deleting field 'OpenCloseDailyFact.productkey'
        db.delete_column('fact_openclose_daily', 'productkey_id')

        # Deleting field 'OpenCloseDailyFact.packagekey'
        db.delete_column('fact_openclose_daily', 'packagekey_id')

        # Deleting field 'DownloadBeginFinishFact.productkey'
        db.delete_column('fact_downloadbeginfinish', 'productkey_id')

        # Deleting field 'DownloadBeginFinishFact.packagekey'
        db.delete_column('fact_downloadbeginfinish', 'packagekey_id')

        # Deleting field 'DownloadFact.productkey'
        db.delete_column('fact_download', 'productkey_id')

        # Deleting field 'DownloadFact.packagekey'
        db.delete_column('fact_download', 'packagekey_id')

        # Deleting field 'DownloadFact.download_packagekey'
        db.delete_column('fact_download', 'download_packagekey_id')

        # Deleting field 'UsinglogFact.productkey'
        db.delete_column('fact_behaviour', 'productkey_id')

        # Deleting field 'UsinglogFact.packagekey'
        db.delete_column('fact_behaviour', 'packagekey_id')

        # Adding field 'ActivateFact.is_new_device_package'
        db.add_column('fact_activate', 'is_new_device_package',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        # Adding field 'ActivateFact.is_new_device_package_version'
        db.add_column('fact_activate', 'is_new_device_package_version',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        # Adding field 'ActivateFact.is_new_device'
        db.add_column('fact_activate', 'is_new_device',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        # Deleting field 'ActivateFact.productkey'
        db.delete_column('fact_activate', 'productkey_id')

        # Deleting field 'ActivateFact.packagekey'
        db.delete_column('fact_activate', 'packagekey_id')


    models = {
        'analysis.activatefact': {
            'Meta': {'object_name': 'ActivateFact', 'db_table': "'fact_activate'", 'ordering': "('-date',)", 'index_together': "(('device', 'date'), ('package', 'date'), ('device', 'package', 'date'), ('product', 'device'), ('product', 'device', 'package'), ('productkey', 'device'), ('productkey', 'packagekey'), ('productkey', 'device', 'packagekey'))"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"}),
            'usinglog': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.UsinglogFact']"})
        },
        'analysis.activatenewreservefact': {
            'Meta': {'object_name': 'ActivateNewReserveFact', 'db_table': "'fact_activate_newreserve'", 'ordering': "('-date',)", '_ormbases': ['analysis.ActivateFact']},
            'activatefact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['analysis.ActivateFact']", 'primary_key': 'True'}),
            'is_new_package': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_package_version': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_channel': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_package': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_new_product_package_version': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'analysis.baidupushdim': {
            'Meta': {'object_name': 'BaiduPushDim', 'db_table': "'dim_baidupush'", 'unique_together': "(('channel_id', 'user_id', 'app_id'),)"},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.datedim': {
            'Meta': {'object_name': 'DateDim', 'db_table': "'dim_date'", 'index_together': "(('year', 'month', 'day'), ('year', 'week'))"},
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
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.devicelanguagedim': {
            'Meta': {'object_name': 'DeviceLanguageDim', 'db_table': "'dim_devicelanguage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.devicemodeldim': {
            'Meta': {'object_name': 'DeviceModelDim', 'db_table': "'dim_devicemodel'", 'unique_together': "(('manufacturer', 'device_name', 'module_name', 'model_name'),)"},
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.deviceosdim': {
            'Meta': {'object_name': 'DeviceOSDim', 'db_table': "'dim_deviceos'", 'unique_together': "(('platform', 'os_version'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.deviceplatformdim': {
            'Meta': {'object_name': 'DevicePlatformDim', 'db_table': "'dim_deviceplatform'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.deviceresolutiondim': {
            'Meta': {'object_name': 'DeviceResolutionDim', 'db_table': "'dim_deviceresolution'", 'index_together': "(('width', 'height'), ('orig_width', 'orig_height'))"},
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'orig_resolution': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'db_index': 'True', 'max_length': '25'}),
            'orig_width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '25', 'default': "'undefined'", 'db_index': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'"})
        },
        'analysis.devicesupplierdim': {
            'Meta': {'object_name': 'DeviceSupplierDim', 'db_table': "'dim_devicesupplier'"},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'", 'db_index': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'default': "'unknown'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mccmnc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'unknown'", 'blank': 'True'})
        },
        'analysis.downloadbeginfinishfact': {
            'Meta': {'object_name': 'DownloadBeginFinishFact', 'db_table': "'fact_downloadbeginfinish'", 'unique_together': "(('start_download', 'end_download'),)", 'index_together': "(('download_package', 'date'), ('package', 'date'), ('product', 'device', 'package', 'download_package', 'date'), ('product', 'device', 'download_package', 'date'), ('product', 'device', 'package', 'date'))"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.UsinglogSegmentDim']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'start_download': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'related_name': "'+'", 'to': "orm['analysis.DownloadFact']"})
        },
        'analysis.downloadfact': {
            'Meta': {'object_name': 'DownloadFact', 'db_table': "'fact_download'", 'index_together': "(('download_package', 'date'), ('download_packagekey', 'date'), ('package', 'date'), ('packagekey', 'date'), ('event', 'package', 'date'), ('event', 'packagekey', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'date'), ('event', 'product', 'device', 'package', 'download_package', 'created_datetime'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'date'), ('event', 'productkey', 'device', 'packagekey', 'download_packagekey', 'created_datetime'))"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'redirect_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['analysis.MediaUrlDim']"}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
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
            'hour': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.locationdim': {
            'Meta': {'object_name': 'LocationDim', 'db_table': "'dim_location'", 'unique_together': "(('country', 'region', 'city'),)"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '60', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.mediaurldim': {
            'Meta': {'object_name': 'MediaUrlDim', 'db_table': "'dim_downloadurl'", 'index_together': "(('host', 'path'),)"},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150', 'default': "''", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '1024'})
        },
        'analysis.networkdim': {
            'Meta': {'object_name': 'NetworkDim', 'db_table': "'dim_network'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'})
        },
        'analysis.openclosedailyfact': {
            'Meta': {'object_name': 'OpenCloseDailyFact', 'db_table': "'fact_openclose_daily'", 'unique_together': "(('start_usinglog', 'end_usinglog'),)", 'index_together': "(('product', 'date', 'segment'), ('product', 'package', 'date', 'segment'), ('package', 'device', 'date', 'segment'))"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
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
            'Meta': {'object_name': 'PackageDim', 'db_table': "'dim_package'", 'unique_together': "(('package_name', 'version_name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'analysis.packagekeydim': {
            'Meta': {'object_name': 'PackageKeyDim', 'db_table': "'dim_packagekey'"},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'default': 'None', 'symmetrical': 'False', 'blank': 'True', 'to': "orm['analysis.PackageCategoryDim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''"})
        },
        'analysis.pagedim': {
            'Meta': {'object_name': 'PageDim', 'db_table': "'dim_page'", 'index_together': "(('host', 'path'),)"},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150', 'default': "''", 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_url': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'urlvalue': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'blank': 'True', 'max_length': '1024'})
        },
        'analysis.productdim': {
            'Meta': {'object_name': 'ProductDim', 'db_table': "'dim_product'", 'unique_together': "(('entrytype', 'channel'),)"},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'", 'db_index': 'True', 'blank': 'True'}),
            'entrytype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'analysis.productkeydim': {
            'Meta': {'object_name': 'ProductKeyDim', 'db_table': "'dim_productkey'"},
            'entrytype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'7c5df60697540294a436cf20674830db'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "'undefined'"})
        },
        'analysis.subscriberiddim': {
            'Meta': {'object_name': 'SubscriberIdDim', 'db_table': "'dim_subscriberid'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imsi': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'undefined'", 'max_length': '30'}),
            'mnc': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'undefined'", 'db_index': 'True'})
        },
        'analysis.usingcountsegmentdim': {
            'Meta': {'object_name': 'UsingcountSegmentDim', 'db_table': "'dim_usingcountsegment'"},
            'endcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startcount': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        },
        'analysis.usinglogfact': {
            'Meta': {'object_name': 'UsinglogFact', 'db_table': "'fact_behaviour'", 'ordering': "('-date',)", 'index_together': "(('package', 'date'), ('package', 'date', 'event'), ('event', 'product', 'device', 'package', 'date'), ('event', 'product', 'device', 'package', 'created_datetime'))"},
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
            'packagekey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.PackageKeyDim']", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.ProductDim']"}),
            'productkey': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['analysis.ProductKeyDim']", 'blank': 'True'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['analysis.PageDim']"}),
            'subscriberid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analysis.SubscriberIdDim']"})
        },
        'analysis.usinglogsegmentdim': {
            'Meta': {'object_name': 'UsinglogSegmentDim', 'db_table': "'dim_usinglogsegment'"},
            'effective_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'endsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'undefined'"}),
            'startsecond': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['analysis']