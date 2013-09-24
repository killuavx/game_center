# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table('promotion_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('help_text', self.gf('django.db.models.fields.CharField')(default='', blank=True, max_length=50)),
        ))
        db.send_create_signal('promotion', ['Place'])

        # Adding model 'Advertisement'
        db.create_table('promotion_advertisement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], related_name='adv_content_type')),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', blank=True, no_check_for_status=True, max_length=100)),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True, db_index=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('promotion', ['Advertisement'])

        # Adding M2M table for field places on 'Advertisement'
        m2m_table_name = db.shorten_name('promotion_advertisement_places')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('advertisement', models.ForeignKey(orm['promotion.advertisement'], null=False)),
            ('place', models.ForeignKey(orm['promotion.place'], null=False)),
            ('ordering', models.PositiveIntegerField( max_length=3, default=0, blank=True, null=False)),
        ))
        db.create_unique(m2m_table_name, ['advertisement_id', 'place_id'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table('promotion_place')

        # Deleting model 'Advertisement'
        db.delete_table('promotion_advertisement')

        # Removing M2M table for field places on 'Advertisement'
        db.delete_table(db.shorten_name('promotion_advertisement_places'))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
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
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['promotion.Place']", 'related_name': "'advertisements'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place'},
            'help_text': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['promotion']