# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recommend'
        db.create_table('promotion_recommend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resources_count', self.gf('django.db.models.fields.IntegerField')(blank=True, default=0)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], blank=True, null=True)),
            ('workspace', self.gf('mezzanine.core.fields.FileField')(blank=True, default='', max_length=500)),
            ('status', self.gf('model_utils.fields.StatusField')(blank=True, default='draft', no_check_for_status=True, max_length=100)),
            ('weekday_numbers', self.gf('django.db.models.fields.CharField')(default='0', max_length=15)),
            ('released_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=datetime.datetime.now, blank=True)),
            ('expiry_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('resources', self.gf('toolkit.fields.MultiResourceField')(to=orm['toolkit.Resource'], object_id_field='object_pk')),
        ))
        db.send_create_signal('promotion', ['Recommend'])

        # Adding index on 'Recommend', fields ['site', 'content_type', 'object_id']
        db.create_index('promotion_recommend', ['site_id', 'content_type_id', 'object_id'])

        # Adding index on 'Recommend', fields ['site', 'status']
        db.create_index('promotion_recommend', ['site_id', 'status'])

        # Adding index on 'Recommend', fields ['site', 'released_datetime', 'expiry_datetime']
        db.create_index('promotion_recommend', ['site_id', 'released_datetime', 'expiry_datetime'])

        # Adding index on 'Recommend', fields ['site', 'status', 'released_datetime', 'expiry_datetime']
        db.create_index('promotion_recommend', ['site_id', 'status', 'released_datetime', 'expiry_datetime'])


    def backwards(self, orm):
        # Removing index on 'Recommend', fields ['site', 'status', 'released_datetime', 'expiry_datetime']
        db.delete_index('promotion_recommend', ['site_id', 'status', 'released_datetime', 'expiry_datetime'])

        # Removing index on 'Recommend', fields ['site', 'released_datetime', 'expiry_datetime']
        db.delete_index('promotion_recommend', ['site_id', 'released_datetime', 'expiry_datetime'])

        # Removing index on 'Recommend', fields ['site', 'status']
        db.delete_index('promotion_recommend', ['site_id', 'status'])

        # Removing index on 'Recommend', fields ['site', 'content_type', 'object_id']
        db.delete_index('promotion_recommend', ['site_id', 'content_type_id', 'object_id'])

        # Deleting model 'Recommend'
        db.delete_table('promotion_recommend')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'promotion.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'blank': 'True', 'null': 'True', 'default': 'None', 'related_name': "'adv_content_type'"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'default': "''", 'max_length': '1024'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'through': "orm['promotion.Advertisement_Places']", 'to': "orm['promotion.Place']", 'blank': 'True', 'related_name': "'advertisements'", 'symmetrical': 'False'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'target': ('django.db.models.fields.CharField', [], {'default': "'_self'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'promotion.advertisement_places': {
            'Meta': {'index_together': "(('place', 'ordering'),)", 'ordering': "('place', '-ordering')", 'unique_together': "(('place', 'advertisement'),)", 'object_name': 'Advertisement_Places'},
            'advertisement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Advertisement']", 'related_name': "'relation_advertisement'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '3'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotion.Place']", 'related_name': "'relation_place'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True', 'auto_now': 'True'})
        },
        'promotion.place': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Place'},
            'help_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'promotion.recommend': {
            'Meta': {'index_together': "(('site', 'content_type', 'object_id'), ('site', 'status'), ('site', 'released_datetime', 'expiry_datetime'), ('site', 'status', 'released_datetime', 'expiry_datetime'))", 'object_name': 'Recommend'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'blank': 'True', 'null': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'datetime.datetime.now', 'blank': 'True'}),
            'expiry_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'default': "'draft'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'weekday_numbers': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '15'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'default': "''", 'max_length': '500'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'toolkit.resource': {
            'Meta': {'object_name': 'Resource', 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'db_table': "'common_resource'"},
            'alias': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'default'", 'max_length': '50'}),
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '40'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'max_length': '100'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': '0', 'max_length': '6'})
        }
    }

    complete_apps = ['promotion']