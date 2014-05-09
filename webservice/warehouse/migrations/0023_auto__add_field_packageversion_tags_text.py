# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PackageVersion.tags_text'
        db.add_column('warehouse_packageversion', 'tags_text',
                      self.gf('tagging_autocomplete.models.TagAutocompleteField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PackageVersion.tags_text'
        db.delete_column('warehouse_packageversion', 'tags_text')


    models = {
        'account.user': {
            'Meta': {'object_name': 'User', 'db_table': "'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'ratings'", 'null': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'_ormbases': ['comments.Comment'], 'ordering': "('submit_date',)", 'object_name': 'ThreadedComment'},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['comments.Comment']", 'unique': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.Rating']"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.ThreadedComment']", 'related_name': "'comments'", 'null': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'related_name': "'children'", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'default': "''", 'null': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['taxonomy.Topic']", 'blank': 'True', 'related_name': "'children'", 'null': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'default': "'draft'", 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'})
        },
        'toolkit.star': {
            'Meta': {'object_name': 'Star', 'db_table': "'common_star'"},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.DO_NOTHING', 'blank': 'True', 'default': 'None', 'to': "orm['generic.ThreadedComment']", 'related_name': "'content_star'", 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.DO_NOTHING', 'blank': 'True', 'default': 'True', 'to': "orm['account.User']", 'related_name': "'stars'", 'null': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'draft'", 'max_length': '100'})
        },
        'warehouse.package': {
            'Meta': {'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['taxonomy.Category']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'packages'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True', 'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'draft'", 'max_length': '100'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'default': '0', 'max_length': '9'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'stars': ('toolkit.fields.StarsField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Star']"}),
            'stars_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_low_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_low_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_medium_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_medium_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'default': "'draft'", 'max_length': '100'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '128'}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '255'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'auto_now': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '4'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['warehouse.PackageVersion']"})
        }
    }

    complete_apps = ['warehouse']