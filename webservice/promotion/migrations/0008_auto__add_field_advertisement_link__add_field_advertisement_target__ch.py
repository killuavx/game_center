# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Advertisement.link'
        db.add_column('promotion_advertisement', 'link',
                      self.gf('django.db.models.fields.URLField')(max_length=1024, blank=True, default=''),
                      keep_default=False)

        # Adding field 'Advertisement.target'
        db.add_column('promotion_advertisement', 'target',
                      self.gf('django.db.models.fields.CharField')(max_length=10, default='_self'),
                      keep_default=False)


        # Changing field 'Advertisement.content_type'
        db.alter_column('promotion_advertisement', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType']))

    def backwards(self, orm):
        # Deleting field 'Advertisement.link'
        db.delete_column('promotion_advertisement', 'link')

        # Deleting field 'Advertisement.target'
        db.delete_column('promotion_advertisement', 'target')


        # Changing field 'Advertisement.content_type'
        db.alter_column('promotion_advertisement', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], default=None))

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'promotion.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'blank': 'True', 'default': 'None', 'related_name': "'adv_content_type'"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'blank': 'True', 'default': "''"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['promotion.Advertisement_Places']", 'symmetrical': 'False', 'related_name': "'advertisements'", 'null': 'True', 'to': "orm['promotion.Place']", 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'no_check_for_status': 'True', 'blank': 'True', 'default': "'draft'"}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'_self'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'blank': 'True', 'default': "''"})
        },
        'promotion.advertisement_places': {
            'Meta': {'ordering': "('place', '-ordering')", 'index_together': "(('place', 'ordering'),)", 'object_name': 'Advertisement_Places', 'unique_together': "(('place', 'advertisement'),)"},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_advertisement'", 'to': "orm['promotion.Advertisement']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'blank': 'True', 'default': '0'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_place'", 'to': "orm['promotion.Place']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'})
        },
        'promotion.place': {
            'Meta': {'object_name': 'Place', 'unique_together': "(('site', 'slug'),)"},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'toolkit.resource': {
            'Meta': {'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'db_table': "'common_resource'", 'object_name': 'Resource', 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True', 'default': "'default'"}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'default': "''"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True', 'default': 'None'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True', 'default': 'None'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True', 'default': '0'})
        }
    }

    complete_apps = ['promotion']