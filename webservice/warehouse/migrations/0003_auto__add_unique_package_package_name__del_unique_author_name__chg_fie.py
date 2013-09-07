# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Author', fields ['name']
        db.delete_unique('warehouse_author', ['name'])

        # Adding unique constraint on 'Package', fields ['package_name']
        db.create_unique('warehouse_package', ['package_name'])


        # Changing field 'PackageScreenshot.rotate'
        db.alter_column('warehouse_packagescreenshot', 'rotate', self.gf('django.db.models.fields.CharField')(max_length=4))

    def backwards(self, orm):
        # Removing unique constraint on 'Package', fields ['package_name']
        db.delete_unique('warehouse_package', ['package_name'])

        # Adding unique constraint on 'Author', fields ['name']
        db.create_unique('warehouse_author', ['name'])


        # Changing field 'PackageScreenshot.rotate'
        db.alter_column('warehouse_packagescreenshot', 'rotate', self.gf('django.db.models.fields.CharField')(max_length=3))

    models = {
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('name',)"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'no_check_for_status': 'True', 'default': "'draft'"})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'packages'", 'to': "orm['taxonomy.Category']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'no_check_for_status': 'True', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.packagescreenshot': {
            'Meta': {'object_name': 'PackageScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['warehouse.Package']"}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'})
        }
    }

    complete_apps = ['warehouse']