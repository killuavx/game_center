# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PackageVersion.di_download'
        db.add_column('warehouse_packageversion', 'di_download',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PackageVersion.di_download'
        db.delete_column('warehouse_packageversion', 'di_download')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Topic']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'unique_together': "(('package', 'version_code'), ('package', 'released_datetime'))", 'object_name': 'PackageVersion'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'di_download': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['warehouse.PackageVersion']"})
        }
    }

    complete_apps = ['warehouse']