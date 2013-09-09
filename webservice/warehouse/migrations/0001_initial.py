# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('warehouse_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=16, null=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
        ))
        db.send_create_signal('warehouse', ['Author'])

        # Adding model 'Package'
        db.create_table('warehouse_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('summary', self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, default='')),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['warehouse.Author'], related_name='packages')),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True, auto_now=True)),
            ('tags', self.gf('tagging_autocomplete.models.TagAutocompleteField')(default='')),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
        ))
        db.send_create_signal('warehouse', ['Package'])

        # Adding M2M table for field categories on 'Package'
        m2m_table_name = db.shorten_name('warehouse_package_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm['warehouse.package'], null=False)),
            ('category', models.ForeignKey(orm['taxonomy.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('warehouse_author')

        # Deleting model 'Package'
        db.delete_table('warehouse_package')

        # Removing M2M table for field categories on 'Package'
        db.delete_table(db.shorten_name('warehouse_package_categories'))


    models = {
        'taxonomy.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '4', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'children'", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'unique': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '200', 'null': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '16', 'null': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'packages'", 'to': "orm['taxonomy.Category']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['warehouse']