# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Place', fields ['slug']
        db.delete_unique('promotion_place', ['slug'])

        # Adding field 'Advertisement.site'
        db.add_column('promotion_advertisement', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding field 'Place.site'
        db.add_column('promotion_place', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'Place', fields ['site', 'slug']
        db.create_unique('promotion_place', ['site_id', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Place', fields ['site', 'slug']
        db.delete_unique('promotion_place', ['site_id', 'slug'])

        # Deleting field 'Advertisement.site'
        db.delete_column('promotion_advertisement', 'site_id')

        # Deleting field 'Place.site'
        db.delete_column('promotion_place', 'site_id')

        # Adding unique constraint on 'Place', fields ['slug']
        db.create_unique('promotion_place', ['slug'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'promotion.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adv_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advertisements'", 'null': 'True', 'to': "orm['promotion.Place']", 'through': "orm['promotion.Advertisement_Places']", 'blank': 'True', 'symmetrical': 'False'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'no_check_for_status': 'True', 'default': "'draft'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'promotion.advertisement_places': {
            'Meta': {'object_name': 'Advertisement_Places', 'unique_together': "(('place', 'advertisement'),)", 'ordering': "('place', '-ordering')", 'index_together': "(('place', 'ordering'),)"},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_advertisement'", 'to': "orm['promotion.Advertisement']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'default': '0', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_place'", 'to': "orm['promotion.Place']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place', 'unique_together': "(('site', 'slug'),)"},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'ordering': "('domain',)", 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['promotion']