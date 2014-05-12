# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PackageVersion.subtitle'
        db.alter_column('warehouse_packageversion', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Package.package_name'
        db.alter_column('warehouse_package', 'package_name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Package.title'
        db.alter_column('warehouse_package', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'PackageVersion.subtitle'
        db.alter_column('warehouse_packageversion', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Package.package_name'
        db.alter_column('warehouse_package', 'package_name', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Package.title'
        db.alter_column('warehouse_package', 'title', self.gf('django.db.models.fields.CharField')(max_length=128))

    models = {
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'db_table': "'django_comments'", 'object_name': 'Comment', 'ordering': "('submit_date',)"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'content_type_set_for_comment'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['account.User']", 'blank': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
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
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['account.User']", 'related_name': "'ratings'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'_ormbases': ['comments.Comment'], 'object_name': 'ThreadedComment', 'ordering': "('submit_date',)"},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['comments.Comment']", 'unique': 'True', 'primary_key': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'to': "orm['generic.Rating']", 'object_id_field': "'object_pk'"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['generic.ThreadedComment']", 'related_name': "'comments'"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'db_index': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['taxonomy.Category']", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'object_name': 'Topic', 'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'db_index': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['taxonomy.Topic']", 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('topic', 'content_type'),)", 'object_name': 'TopicalItem', 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'db_index': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['generic.ThreadedComment']", 'default': 'None', 'related_name': "'content_star'", 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['account.User']", 'default': 'True', 'related_name': "'stars'", 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author', 'unique_together': "(('site', 'name'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '16', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"})
        },
        'warehouse.iosauthor': {
            'Meta': {'_ormbases': ['warehouse.Author'], 'object_name': 'IOSAuthor'},
            'artist_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'author_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['warehouse.Author']", 'unique': 'True', 'primary_key': 'True'}),
            'seller_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '150', 'blank': 'True'}),
            'seller_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '500', 'blank': 'True'}),
            'view_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '500', 'blank': 'True'})
        },
        'warehouse.iospackage': {
            'Meta': {'_ormbases': ['warehouse.Package'], 'object_name': 'IOSPackage'},
            'appleuser_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'package_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['warehouse.Package']", 'unique': 'True', 'primary_key': 'True'}),
            'track_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'view_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '500', 'blank': 'True'})
        },
        'warehouse.iospackageversion': {
            'Meta': {'_ormbases': ['warehouse.PackageVersion'], 'object_name': 'IOSPackageVersion'},
            'appleformatted_rating': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '12', 'default': 'None', 'blank': 'True'}),
            'appleuser_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'formatted_price': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'}),
            'is_support_ipad': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_support_iphone': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'packageversion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['warehouse.PackageVersion']", 'unique': 'True', 'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '3', 'db_index': 'True', 'default': '0', 'max_digits': '12'}),
            'price_currency': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '4', 'default': 'None', 'blank': 'True'})
        },
        'warehouse.package': {
            'Meta': {'object_name': 'Package', 'unique_together': "(('site', 'package_name'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'blank': 'True', 'to': "orm['taxonomy.Category']", 'symmetrical': 'False'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'db_index': 'True', 'default': '0', 'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'db_index': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'object_name': 'PackageVersion', 'unique_together': "(('site', 'package', 'version_code'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '40', 'default': 'None', 'blank': 'True'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'stars': ('toolkit.fields.StarsField', [], {'to': "orm['toolkit.Star']", 'object_id_field': "'object_pk'"}),
            'stars_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_good_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_low_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_low_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_medium_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stars_medium_rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'stars_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('model_utils.fields.StatusField', [], {'blank': 'True', 'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedDevice']", 'symmetrical': 'False'}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedFeature']", 'symmetrical': 'False'}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedLanguage']", 'symmetrical': 'False'}),
            'tags_text': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'default': '1'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.PackageVersion']", 'related_name': "'screenshots'"})
        },
        'warehouse.supporteddevice': {
            'Meta': {'object_name': 'SupportedDevice', 'unique_together': "(('site', 'code'),)"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "''"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedfeature': {
            'Meta': {'object_name': 'SupportedFeature', 'unique_together': "(('site', 'code'),)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30', 'default': "''"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedlanguage': {
            'Meta': {'object_name': 'SupportedLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['warehouse']