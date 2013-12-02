# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Advertisement_Places.updated_datetime'
        db.add_column('promotion_advertisement_places', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now, auto_now=True),
                      keep_default=False)

        # Adding field 'Advertisement_Places.created_datetime'
        db.add_column('promotion_advertisement_places', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True, default=datetime.datetime.now),
                      keep_default=False)

        # Adding index on 'Advertisement_Places', fields ['place', 'ordering']
        db.create_index('promotion_advertisement_places', ['place_id', 'ordering'])


    def backwards(self, orm):
        # Removing index on 'Advertisement_Places', fields ['place', 'ordering']
        db.delete_index('promotion_advertisement_places', ['place_id', 'ordering'])

        # Deleting field 'Advertisement_Places.updated_datetime'
        db.delete_column('promotion_advertisement_places', 'updated_datetime')

        # Deleting field 'Advertisement_Places.created_datetime'
        db.delete_column('promotion_advertisement_places', 'created_datetime')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'promotion.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'adv_content_type'"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'advertisements'", 'blank': 'True', 'to': "orm['promotion.Place']", 'through': "orm['promotion.Advertisement_Places']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'max_length': '100', 'no_check_for_status': 'True', 'default': "'draft'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'promotion.advertisement_places': {
            'Meta': {'index_together': "(('place', 'ordering'),)", 'object_name': 'Advertisement_Places', 'unique_together': "(('place', 'advertisement'),)", 'ordering': "('place', '-ordering')"},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Advertisement']", 'related_name': "'relation_advertisement'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '3', 'default': '0'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Place']", 'related_name': "'relation_place'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now', 'auto_now': 'True'})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place'},
            'help_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'})
        }
    }

    complete_apps = ['promotion']