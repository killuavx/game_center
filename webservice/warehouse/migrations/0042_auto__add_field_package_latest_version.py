# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Package.latest_version'
        db.add_column('warehouse_package', 'latest_version',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['warehouse.PackageVersion'], default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Package.latest_version'
        db.delete_column('warehouse_package', 'latest_version_id')


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
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comments.comment': {
            'Meta': {'db_table': "'django_comments'", 'ordering': "('submit_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_comments'", 'blank': 'True', 'null': 'True', 'to': "orm['account.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
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
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'null': 'True', 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'object_name': 'ThreadedComment', 'ordering': "('submit_date',)", '_ormbases': ['comments.Comment']},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['comments.Comment']", 'primary_key': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'to': "orm['generic.Rating']", 'object_id_field': "'object_pk'"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'null': 'True', 'to': "orm['generic.ThreadedComment']"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']"}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Topic']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'index_together': "(('site', 'topic'), ('site', 'topic', 'content_type'), ('site', 'topic', 'content_type', 'object_id'), ('site', 'topic', 'content_type', 'object_id', 'ordering'), ('topic', 'content_type'))", 'ordering': "('ordering',)", 'unique_together': "(('topic', 'content_type', 'object_id'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'})
        },
        'toolkit.resource': {
            'Meta': {'db_table': "'common_resource'", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'object_name': 'Resource'},
            'alias': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'default': "'default'"}),
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40', 'default': 'None'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'height': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '6', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'default': 'None'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '6', 'default': '0'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_star'", 'null': 'True', 'blank': 'True', 'to': "orm['generic.ThreadedComment']", 'on_delete': 'models.DO_NOTHING', 'default': 'None'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stars'", 'null': 'True', 'blank': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'default': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'object_name': 'Author', 'unique_together': "(('site', 'name'),)"},
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '16'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"})
        },
        'warehouse.iosauthor': {
            'Meta': {'object_name': 'IOSAuthor', '_ormbases': ['warehouse.Author']},
            'artist_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'author_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['warehouse.Author']", 'primary_key': 'True'}),
            'seller_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '150'}),
            'seller_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '500'}),
            'view_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '500'})
        },
        'warehouse.iospackage': {
            'Meta': {'object_name': 'IOSPackage', '_ormbases': ['warehouse.Package']},
            'appleuser_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'package_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['warehouse.Package']", 'primary_key': 'True'}),
            'track_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'view_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '500'})
        },
        'warehouse.iospackageversion': {
            'Meta': {'object_name': 'IOSPackageVersion', '_ormbases': ['warehouse.PackageVersion']},
            'appleformatted_rating': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '12', 'default': 'None'}),
            'appleuser_rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'formatted_price': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '50'}),
            'is_support_ipad': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'is_support_iphone': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'packageversion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['warehouse.PackageVersion']", 'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'db_index': 'True', 'default': '0', 'max_digits': '12', 'decimal_places': '3'}),
            'price_currency': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '4', 'default': 'None'})
        },
        'warehouse.package': {
            'Meta': {'index_together': "(('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))", 'object_name': 'Package', 'unique_together': "(('site', 'package_name'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'blank': 'True', 'to': "orm['taxonomy.Category']", 'symmetrical': 'False'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'blank': 'True', 'max_length': '9', 'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['warehouse.PackageVersion']", 'default': 'None'}),
            'package_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_packages'", 'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root_packages'", 'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'max_length': '100', 'default': "'draft'"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"})
        },
        'warehouse.packageversion': {
            'Meta': {'index_together': "(('site', 'package'), ('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))", 'object_name': 'PackageVersion', 'unique_together': "(('site', 'package', 'version_code'),)"},
            'comments': ('comment.fields.CommentsField', [], {'to': "orm['generic.ThreadedComment']", 'object_id_field': "'object_pk'"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '500', 'default': "''"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40', 'default': 'None'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'download': ('toolkit.fields.PkgFileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'max_length': '9', 'default': '0'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '40', 'default': 'None'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '500', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'to': "orm['toolkit.Resource']", 'object_id_field': "'object_pk'"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
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
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'blank': 'True', 'max_length': '100', 'default': "'draft'"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'summary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedDevice']", 'symmetrical': 'False'}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedFeature']", 'symmetrical': 'False'}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['warehouse.SupportedLanguage']", 'symmetrical': 'False'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'default': '1'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'blank': 'True', 'max_length': '500', 'default': "''"})
        },
        'warehouse.packageversionscreenshot': {
            'Meta': {'index_together': "(('version', 'kind'),)", 'object_name': 'PackageVersionScreenshot'},
            'alt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '500'}),
            'kind': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20', 'default': "'default'"}),
            'rotate': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': '0'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['warehouse.PackageVersion']"})
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