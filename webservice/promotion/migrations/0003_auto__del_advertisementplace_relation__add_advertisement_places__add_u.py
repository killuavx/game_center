# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AdvertisementPlace_Relation'
        db.delete_table('promotion_advertisementplace_relation')

        # Adding model 'Advertisement_Places'
        db.create_table('promotion_advertisement_places', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Place'], related_name='relation_place')),
            ('advertisement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Advertisement'], related_name='relation_advertisement')),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, default=0, max_length=3)),
        ))
        db.send_create_signal('promotion', ['Advertisement_Places'])

        # Adding unique constraint on 'Advertisement_Places', fields ['place', 'advertisement']
        db.create_unique('promotion_advertisement_places', ['place_id', 'advertisement_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Advertisement_Places', fields ['place', 'advertisement']
        db.delete_unique('promotion_advertisement_places', ['place_id', 'advertisement_id'])

        # Adding model 'AdvertisementPlace_Relation'
        db.create_table('promotion_advertisementplace_relation', (
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, default=0, max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Place'], related_name='relation_place')),
            ('advertisement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Advertisement'], related_name='advertisement')),
        ))
        db.send_create_signal('promotion', ['AdvertisementPlace_Relation'])

        # Deleting model 'Advertisement_Places'
        db.delete_table('promotion_advertisement_places')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
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
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['promotion.Place']", 'related_name': "'advertisements'", 'through': "orm['promotion.Advertisement_Places']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'promotion.advertisement_places': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'Advertisement_Places', 'unique_together': "(('place', 'advertisement'),)"},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Advertisement']", 'related_name': "'relation_advertisement'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '3'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Place']", 'related_name': "'relation_place'"})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place'},
            'help_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'})
        }
    }

    complete_apps = ['promotion']