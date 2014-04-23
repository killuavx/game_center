# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Topic', fields ['name']
        db.delete_unique('taxonomy_topic', ['name'])

        # Removing unique constraint on 'Topic', fields ['slug']
        db.delete_unique('taxonomy_topic', ['slug'])

        # Removing unique constraint on 'Category', fields ['name']
        db.delete_unique('taxonomy_category', ['name'])

        # Removing unique constraint on 'Category', fields ['slug']
        db.delete_unique('taxonomy_category', ['slug'])

        # Adding field 'Category.site'
        db.add_column('taxonomy_category', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding index on 'Category', fields ['name']
        db.create_index('taxonomy_category', ['name'])

        # Adding unique constraint on 'Category', fields ['site', 'slug']
        db.create_unique('taxonomy_category', ['site_id', 'slug'])

        # Adding unique constraint on 'Category', fields ['site', 'name']
        db.create_unique('taxonomy_category', ['site_id', 'name'])

        # Adding field 'Topic.site'
        db.add_column('taxonomy_topic', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding index on 'Topic', fields ['name']
        db.create_index('taxonomy_topic', ['name'])

        # Adding unique constraint on 'Topic', fields ['site', 'slug']
        db.create_unique('taxonomy_topic', ['site_id', 'slug'])

        # Adding unique constraint on 'Topic', fields ['site', 'name']
        db.create_unique('taxonomy_topic', ['site_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Topic', fields ['site', 'name']
        db.delete_unique('taxonomy_topic', ['site_id', 'name'])

        # Removing unique constraint on 'Topic', fields ['site', 'slug']
        db.delete_unique('taxonomy_topic', ['site_id', 'slug'])

        # Removing index on 'Topic', fields ['name']
        db.delete_index('taxonomy_topic', ['name'])

        # Removing unique constraint on 'Category', fields ['site', 'name']
        db.delete_unique('taxonomy_category', ['site_id', 'name'])

        # Removing unique constraint on 'Category', fields ['site', 'slug']
        db.delete_unique('taxonomy_category', ['site_id', 'slug'])

        # Removing index on 'Category', fields ['name']
        db.delete_index('taxonomy_category', ['name'])

        # Deleting field 'Category.site'
        db.delete_column('taxonomy_category', 'site_id')

        # Adding unique constraint on 'Category', fields ['slug']
        db.create_unique('taxonomy_category', ['slug'])

        # Adding unique constraint on 'Category', fields ['name']
        db.create_unique('taxonomy_category', ['name'])

        # Deleting field 'Topic.site'
        db.delete_column('taxonomy_topic', 'site_id')

        # Adding unique constraint on 'Topic', fields ['slug']
        db.create_unique('taxonomy_topic', ['slug'])

        # Adding unique constraint on 'Topic', fields ['name']
        db.create_unique('taxonomy_topic', ['name'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
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
            'Meta': {'object_name': 'Category', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'children'", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "''", 'blank': 'True', 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['taxonomy.Topic']", 'related_name': "'children'", 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'object_name': 'TopicalItem', 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'index_together': "(('topic', 'content_type'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['taxonomy']