# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipsWord'
        db.create_table('searcher_tipsword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=36, unique=True)),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, max_length=8, default=0)),
            ('status', self.gf('model_utils.fields.StatusField')(blank=True, max_length=100, default='draft', no_check_for_status=True)),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, null=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('searcher', ['TipsWord'])


    def backwards(self, orm):
        # Deleting model 'TipsWord'
        db.delete_table('searcher_tipsword')


    models = {
        'searcher.tipsword': {
            'Meta': {'object_name': 'TipsWord'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '36', 'unique': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '8', 'default': '0'})
        }
    }

    complete_apps = ['searcher']