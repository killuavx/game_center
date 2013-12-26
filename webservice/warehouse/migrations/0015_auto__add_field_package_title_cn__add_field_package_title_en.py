# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    no_dry_run = True

    def forwards(self, orm):
        # Adding field 'Package.title_cn'
        db.add_column('warehouse_package', 'title_cn',
                      self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=128),
                      keep_default=False)

        # Adding field 'Package.title_en'
        db.add_column('warehouse_package', 'title_en',
                      self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=128),
                      keep_default=False)

        step = '/'
        pkgs=orm['warehouse.Package'].objects.all()
        self._rewrite_title(pkgs=pkgs, step=step)

    def _rewrite_title(self, pkgs, step):
        for pkg in pkgs:
            titles = pkg.title.split(step)
            pkg.title_cn, pkg.title_en = titles[0], titles[1] if len(titles) > 1 else '-- sorry, no translation provided --'
            pkg.save()


    def backwards(self, orm):
        # Deleting field 'Package.title_cn'
        db.delete_column('warehouse_package', 'title_cn')

        # Deleting field 'Package.title_en'
        db.delete_column('warehouse_package', 'title_en')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('ordering',)"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['taxonomy.Category']", 'null': 'True', 'related_name': "'children'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': "''", 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'ordering': "('ordering',)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['taxonomy.Topic']", 'null': 'True', 'related_name': "'children'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'object_name': 'TopicalItem', 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '16'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['taxonomy.Category']", 'related_name': "'packages'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_cn': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '128'}),
            'title_en': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'object_name': 'PackageVersion', 'unique_together': "(('package', 'version_code'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'di_download': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'download': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'auto_now_add': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.PackageVersion']", 'related_name': "'screenshots'"})
        }
    }

    complete_apps = ['warehouse']