# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SupportedLanguage'
        db.create_table('warehouse_supportedlanguage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('warehouse', ['SupportedLanguage'])

        # Adding model 'SupportedDevice'
        db.create_table('warehouse_supporteddevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, default='')),
        ))
        db.send_create_signal('warehouse', ['SupportedDevice'])

        # Adding unique constraint on 'SupportedDevice', fields ['site', 'code']
        db.create_unique('warehouse_supporteddevice', ['site_id', 'code'])

        # Adding model 'SupportedFeature'
        db.create_table('warehouse_supportedfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30, default='')),
        ))
        db.send_create_signal('warehouse', ['SupportedFeature'])

        # Adding unique constraint on 'SupportedFeature', fields ['site', 'code']
        db.create_unique('warehouse_supportedfeature', ['site_id', 'code'])

        # Adding M2M table for field supported_features on 'PackageVersion'
        m2m_table_name = db.shorten_name('warehouse_packageversion_supported_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packageversion', models.ForeignKey(orm['warehouse.packageversion'], null=False)),
            ('supportedfeature', models.ForeignKey(orm['warehouse.supportedfeature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['packageversion_id', 'supportedfeature_id'])

        # Adding M2M table for field supported_languages on 'PackageVersion'
        m2m_table_name = db.shorten_name('warehouse_packageversion_supported_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packageversion', models.ForeignKey(orm['warehouse.packageversion'], null=False)),
            ('supportedlanguage', models.ForeignKey(orm['warehouse.supportedlanguage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['packageversion_id', 'supportedlanguage_id'])

        # Adding M2M table for field supported_devices on 'PackageVersion'
        m2m_table_name = db.shorten_name('warehouse_packageversion_supported_devices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('packageversion', models.ForeignKey(orm['warehouse.packageversion'], null=False)),
            ('supporteddevice', models.ForeignKey(orm['warehouse.supporteddevice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['packageversion_id', 'supporteddevice_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SupportedFeature', fields ['site', 'code']
        db.delete_unique('warehouse_supportedfeature', ['site_id', 'code'])

        # Removing unique constraint on 'SupportedDevice', fields ['site', 'code']
        db.delete_unique('warehouse_supporteddevice', ['site_id', 'code'])

        # Deleting model 'SupportedLanguage'
        db.delete_table('warehouse_supportedlanguage')

        # Deleting model 'SupportedDevice'
        db.delete_table('warehouse_supporteddevice')

        # Deleting model 'SupportedFeature'
        db.delete_table('warehouse_supportedfeature')

        # Removing M2M table for field supported_features on 'PackageVersion'
        db.delete_table(db.shorten_name('warehouse_packageversion_supported_features'))

        # Removing M2M table for field supported_languages on 'PackageVersion'
        db.delete_table(db.shorten_name('warehouse_packageversion_supported_languages'))

        # Removing M2M table for field supported_devices on 'PackageVersion'
        db.delete_table(db.shorten_name('warehouse_packageversion_supported_devices'))


    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'db_table': "'django_comments'", 'ordering': "('submit_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_comments'", 'to': "orm['account.User']", 'null': 'True', 'blank': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'null': 'True', 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'object_name': 'ThreadedComment', 'ordering': "('submit_date',)", '_ormbases': ['comments.Comment']},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['comments.Comment']", 'primary_key': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'to': "orm['generic.Rating']", 'object_id_field': "'object_pk'"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'null': 'True', 'to': "orm['generic.ThreadedComment']"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'to': "orm['taxonomy.Category']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'to': "orm['taxonomy.Topic']", 'null': 'True', 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.ThreadedComment']", 'on_delete': 'models.DO_NOTHING', 'default': 'None', 'related_name': "'content_star'", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'default': 'True', 'related_name': "'stars'", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author', 'unique_together': "(('site', 'name'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '16'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package', 'unique_together': "(('site', 'package_name'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'to': "orm['taxonomy.Category']", 'blank': 'True', 'symmetrical': 'False'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '9', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'object_name': 'PackageVersion', 'unique_together': "(('site', 'package', 'version_code'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40', 'default': 'None'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40', 'default': 'None'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'stars': ('toolkit.fields.StarsField', [], {'to': "orm['toolkit.Star']", 'object_id_field': "'object_pk'"}),
            'stars_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_low_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_low_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_medium_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_medium_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128', 'default': "''"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedDevice']", 'symmetrical': 'False'}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedFeature']", 'symmetrical': 'False'}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedLanguage']", 'symmetrical': 'False'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'default': '1'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['warehouse.PackageVersion']"})
        },
        'warehouse.supporteddevice': {
            'Meta': {'object_name': 'SupportedDevice', 'unique_together': "(('site', 'code'),)"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "''"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedfeature': {
            'Meta': {'object_name': 'SupportedFeature', 'unique_together': "(('site', 'code'),)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30', 'default': "''"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedlanguage': {
            'Meta': {'object_name': 'SupportedLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['warehouse']