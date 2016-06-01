# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PackageRankingType'
        db.create_table('ranking_packagerankingtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=2000)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(null=True, blank=True, max_length=200)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(to=orm['generic.AssignedKeyword'], object_id_field='object_pk')),
        ))
        db.send_create_signal('ranking', ['PackageRankingType'])

        # Adding unique constraint on 'PackageRankingType', fields ['site', 'slug']
        db.create_unique('ranking_packagerankingtype', ['site_id', 'slug'])

        # Adding model 'PackageRanking'
        db.create_table('ranking_packageranking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cycle_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ranking_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ranking.PackageRankingType'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taxonomy.Category'])),
        ))
        db.send_create_signal('ranking', ['PackageRanking'])

        # Adding unique constraint on 'PackageRanking', fields ['site', 'category', 'ranking_type', 'cycle_type']
        db.create_unique('ranking_packageranking', ['site_id', 'category_id', 'ranking_type_id', 'cycle_type'])

        # Adding index on 'PackageRanking', fields ['site', 'category']
        db.create_index('ranking_packageranking', ['site_id', 'category_id'])

        # Adding index on 'PackageRanking', fields ['site', 'category', '_order']
        db.create_index('ranking_packageranking', ['site_id', 'category_id', '_order'])

        # Adding index on 'PackageRanking', fields ['site', 'category', 'ranking_type']
        db.create_index('ranking_packageranking', ['site_id', 'category_id', 'ranking_type_id'])

        # Adding model 'PackageRankingItem'
        db.create_table('ranking_packagerankingitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('ranking', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_ranking', to=orm['ranking.PackageRanking'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_package', to=orm['warehouse.Package'])),
        ))
        db.send_create_signal('ranking', ['PackageRankingItem'])

        # Adding unique constraint on 'PackageRankingItem', fields ['ranking', 'package']
        db.create_unique('ranking_packagerankingitem', ['ranking_id', 'package_id'])

        # Adding index on 'PackageRankingItem', fields ['ranking', '_order']
        db.create_index('ranking_packagerankingitem', ['ranking_id', '_order'])


    def backwards(self, orm):
        # Removing index on 'PackageRankingItem', fields ['ranking', '_order']
        db.delete_index('ranking_packagerankingitem', ['ranking_id', '_order'])

        # Removing unique constraint on 'PackageRankingItem', fields ['ranking', 'package']
        db.delete_unique('ranking_packagerankingitem', ['ranking_id', 'package_id'])

        # Removing index on 'PackageRanking', fields ['site', 'category', 'ranking_type']
        db.delete_index('ranking_packageranking', ['site_id', 'category_id', 'ranking_type_id'])

        # Removing index on 'PackageRanking', fields ['site', 'category', '_order']
        db.delete_index('ranking_packageranking', ['site_id', 'category_id', '_order'])

        # Removing index on 'PackageRanking', fields ['site', 'category']
        db.delete_index('ranking_packageranking', ['site_id', 'category_id'])

        # Removing unique constraint on 'PackageRanking', fields ['site', 'category', 'ranking_type', 'cycle_type']
        db.delete_unique('ranking_packageranking', ['site_id', 'category_id', 'ranking_type_id', 'cycle_type'])

        # Removing unique constraint on 'PackageRankingType', fields ['site', 'slug']
        db.delete_unique('ranking_packagerankingtype', ['site_id', 'slug'])

        # Deleting model 'PackageRankingType'
        db.delete_table('ranking_packagerankingtype')

        # Deleting model 'PackageRanking'
        db.delete_table('ranking_packageranking')

        # Deleting model 'PackageRankingItem'
        db.delete_table('ranking_packagerankingitem')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.assignedkeyword': {
            'Meta': {'object_name': 'AssignedKeyword', 'ordering': "('_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'ranking.packageranking': {
            'Meta': {'object_name': 'PackageRanking', 'ordering': "('_order',)", 'unique_together': "(('site', 'category', 'ranking_type', 'cycle_type'),)", 'index_together': "(('site', 'category'), ('site', 'category', '_order'), ('site', 'category', 'ranking_type'))"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cycle_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rankings'", 'blank': 'True', 'through': "orm['ranking.PackageRankingItem']", 'null': 'True', 'symmetrical': 'False', 'to': "orm['warehouse.Package']"}),
            'ranking_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ranking.PackageRankingType']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'ranking.packagerankingitem': {
            'Meta': {'object_name': 'PackageRankingItem', 'ordering': "('ranking', '_order')", 'unique_together': "(('ranking', 'package'),)", 'index_together': "(('ranking', '_order'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_package'", 'to': "orm['warehouse.Package']"}),
            'ranking': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_ranking'", 'to': "orm['ranking.PackageRanking']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'ranking.packagerankingtype': {
            'Meta': {'object_name': 'PackageRankingType', 'unique_together': "(('site', 'slug'),)"},
            '_meta_title': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '500'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'to': "orm['generic.AssignedKeyword']", 'object_id_field': "'object_pk'"}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '2000'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "''", 'blank': 'True', 'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['taxonomy.Topic']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'object_name': 'TopicalItem', 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'index_together': "(('topic', 'content_type'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author', 'unique_together': "(('site', 'name'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '16'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package', 'unique_together': "(('site', 'package_name'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'packages'", 'blank': 'True', 'to': "orm['taxonomy.Category']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['ranking']