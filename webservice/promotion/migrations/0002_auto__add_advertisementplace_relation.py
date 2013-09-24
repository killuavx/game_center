# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdvertisementPlace_Relation'
        db.create_table('promotion_advertisementplace_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Place'], related_name='relation_place')),
            ('advertisement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotion.Advertisement'], related_name='advertisement')),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3, default=0, blank=True)),
        ))
        db.send_create_signal('promotion', ['AdvertisementPlace_Relation'])

        # Removing M2M table for field places on 'Advertisement'
        db.delete_table(db.shorten_name('promotion_advertisement_places'))


    def backwards(self, orm):
        # Deleting model 'AdvertisementPlace_Relation'
        db.delete_table('promotion_advertisementplace_relation')

        # Adding M2M table for field places on 'Advertisement'
        m2m_table_name = db.shorten_name('promotion_advertisement_places')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('advertisement', models.ForeignKey(orm['promotion.advertisement'], null=False)),
            ('place', models.ForeignKey(orm['promotion.place'], null=False))
        ))
        db.create_unique(m2m_table_name, ['advertisement_id', 'place_id'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
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
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['promotion.Place']", 'through': "orm['promotion.AdvertisementPlace_Relation']", 'related_name': "'advertisements'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'promotion.advertisementplace_relation': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'AdvertisementPlace_Relation'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Advertisement']", 'related_name': "'advertisement'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'default': '0', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Place']", 'related_name': "'relation_place'"})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True'})
        }
    }

    complete_apps = ['promotion']