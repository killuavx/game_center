# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('taxonomy_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=32, unique=True)),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, default=0, db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['taxonomy.Category'], blank=True, related_name='children')),
            ('subtitle', self.gf('django.db.models.fields.CharField')(null=True, blank=True, default='', max_length=200)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(blank=True, default='', max_length=100)),
            ('mptt_lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_rgt', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('taxonomy', ['Category'])

        # Adding model 'Topic'
        db.create_table('taxonomy_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=32, unique=True)),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, default=0, db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['taxonomy.Topic'], blank=True, related_name='children')),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(blank=True, default='', max_length=100)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(blank=True, default='', max_length=100)),
            ('summary', self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=255)),
            ('status', self.gf('model_utils.fields.StatusField')(blank=True, default='draft', no_check_for_status=True, max_length=100)),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True, db_index=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('mptt_lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_rgt', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('taxonomy', ['Topic'])

        # Adding model 'TopicalItem'
        db.create_table('taxonomy_topicalitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taxonomy.Topic'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], related_name='topic_content_type')),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('taxonomy', ['TopicalItem'])

        # Adding unique constraint on 'TopicalItem', fields ['topic', 'content_type', 'object_id']
        db.create_unique('taxonomy_topicalitem', ['topic_id', 'content_type_id', 'object_id'])

        # Adding index on 'TopicalItem', fields ['topic', 'content_type']
        db.create_index('taxonomy_topicalitem', ['topic_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing index on 'TopicalItem', fields ['topic', 'content_type']
        db.delete_index('taxonomy_topicalitem', ['topic_id', 'content_type_id'])

        # Removing unique constraint on 'TopicalItem', fields ['topic', 'content_type', 'object_id']
        db.delete_unique('taxonomy_topicalitem', ['topic_id', 'content_type_id', 'object_id'])

        # Deleting model 'Category'
        db.delete_table('taxonomy_category')

        # Deleting model 'Topic'
        db.delete_table('taxonomy_topic')

        # Deleting model 'TopicalItem'
        db.delete_table('taxonomy_topicalitem')


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
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['taxonomy.Category']", 'blank': 'True', 'related_name': "'children'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'default': "''", 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['taxonomy.Topic']", 'blank': 'True', 'related_name': "'children'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']"})
        }
    }

    complete_apps = ['taxonomy']