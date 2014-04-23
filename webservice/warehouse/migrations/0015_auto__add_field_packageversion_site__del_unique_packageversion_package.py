# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Package', fields ['package_name']
        db.delete_unique('warehouse_package', ['package_name'])

        # Removing unique constraint on 'PackageVersion', fields ['package', 'version_code']
        db.delete_unique('warehouse_packageversion', ['package_id', 'version_code'])

        # Adding field 'PackageVersion.site'
        db.add_column('warehouse_packageversion', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'PackageVersion', fields ['site', 'package', 'version_code']
        db.create_unique('warehouse_packageversion', ['site_id', 'package_id', 'version_code'])

        # Adding field 'Package.site'
        db.add_column('warehouse_package', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding index on 'Package', fields ['package_name']
        db.create_index('warehouse_package', ['package_name'])

        # Adding index on 'Package', fields ['download_count']
        db.create_index('warehouse_package', ['download_count'])

        # Adding index on 'Package', fields ['updated_datetime']
        db.create_index('warehouse_package', ['updated_datetime'])

        # Adding unique constraint on 'Package', fields ['site', 'package_name']
        db.create_unique('warehouse_package', ['site_id', 'package_name'])

        # Adding field 'Author.site'
        db.add_column('warehouse_author', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'Author', fields ['site', 'name']
        db.create_unique('warehouse_author', ['site_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Author', fields ['site', 'name']
        db.delete_unique('warehouse_author', ['site_id', 'name'])

        # Removing unique constraint on 'Package', fields ['site', 'package_name']
        db.delete_unique('warehouse_package', ['site_id', 'package_name'])

        # Removing index on 'Package', fields ['updated_datetime']
        db.delete_index('warehouse_package', ['updated_datetime'])

        # Removing index on 'Package', fields ['download_count']
        db.delete_index('warehouse_package', ['download_count'])

        # Removing index on 'Package', fields ['package_name']
        db.delete_index('warehouse_package', ['package_name'])

        # Removing unique constraint on 'PackageVersion', fields ['site', 'package', 'version_code']
        db.delete_unique('warehouse_packageversion', ['site_id', 'package_id', 'version_code'])

        # Deleting field 'PackageVersion.site'
        db.delete_column('warehouse_packageversion', 'site_id')

        # Adding unique constraint on 'PackageVersion', fields ['package', 'version_code']
        db.create_unique('warehouse_packageversion', ['package_id', 'version_code'])

        # Deleting field 'Package.site'
        db.delete_column('warehouse_package', 'site_id')

        # Adding unique constraint on 'Package', fields ['package_name']
        db.create_unique('warehouse_package', ['package_name'])

        # Deleting field 'Author.site'
        db.delete_column('warehouse_author', 'site_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('ordering',)"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'children'", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'ordering': "('ordering',)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['taxonomy.Topic']", 'related_name': "'children'", 'null': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem', 'ordering': "('ordering',)", 'index_together': "(('topic', 'content_type'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '16'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'})
        },
        'warehouse.package': {
            'Meta': {'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'packages'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'max_length': '9', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '255'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'di_download': ('django.db.models.fields.files.FileField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'download': ('django.db.models.fields.files.FileField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'max_length': '9'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '4'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.PackageVersion']", 'related_name': "'screenshots'"})
        }
    }

    complete_apps = ['warehouse']