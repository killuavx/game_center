# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'TipsWord', fields ['keyword']
        db.delete_unique('searcher_tipsword', ['keyword'])

        # Adding field 'TipsWord.site'
        db.add_column('searcher_tipsword', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], default=1),
                      keep_default=False)

        # Adding unique constraint on 'TipsWord', fields ['site', 'keyword']
        db.create_unique('searcher_tipsword', ['site_id', 'keyword'])


    def backwards(self, orm):
        # Removing unique constraint on 'TipsWord', fields ['site', 'keyword']
        db.delete_unique('searcher_tipsword', ['site_id', 'keyword'])

        # Deleting field 'TipsWord.site'
        db.delete_column('searcher_tipsword', 'site_id')

        # Adding unique constraint on 'TipsWord', fields ['keyword']
        db.create_unique('searcher_tipsword', ['keyword'])


    models = {
        'searcher.tipsword': {
            'Meta': {'object_name': 'TipsWord', 'unique_together': "(('site', 'keyword'),)", 'ordering': "('-weight',)"},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'max_length': '100', 'no_check_for_status': 'True', 'default': "'draft'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '8', 'default': '0'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['searcher']