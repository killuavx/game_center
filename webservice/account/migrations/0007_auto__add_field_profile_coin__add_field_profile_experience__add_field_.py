# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.coin'
        db.add_column('account_profile', 'coin',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Profile.experience'
        db.add_column('account_profile', 'experience',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Profile.level'
        db.add_column('account_profile', 'level',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.coin'
        db.delete_column('account_profile', 'coin')

        # Deleting field 'Profile.experience'
        db.delete_column('account_profile', 'experience')

        # Deleting field 'Profile.level'
        db.delete_column('account_profile', 'level')


    models = {
        'account.profile': {
            'Meta': {'object_name': 'Profile'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bookmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.Package']", 'symmetrical': 'False', 'blank': 'True'}),
            'coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'default': "''", 'unique': 'True'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "''", 'unique': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': '15', 'default': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'gamecenter_profile'", 'unique': 'True', 'to': "orm['account.User']"})
        },
        'account.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'account.userappbind': {
            'Meta': {'index_together': "(('user', 'app'), ('user', 'created'))", 'object_name': 'UserAppBind', 'unique_together': "(('user', 'app'), ('app', 'uid'))"},
            'app': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appbinds'", 'to': "orm['account.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['account.User']", 'blank': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'ratings'", 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'ordering': "('submit_date',)", '_ormbases': ['comments.Comment'], 'object_name': 'ThreadedComment'},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['comments.Comment']"}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.Rating']"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'comments'", 'to': "orm['generic.ThreadedComment']"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'ordering': "('domain',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['taxonomy.Category']", 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''", 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('site', 'slug'), ('site', 'name'))", 'object_name': 'Topic'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['taxonomy.Topic']", 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'ordering': "('ordering',)", 'index_together': "(('site', 'topic'), ('site', 'topic', 'content_type'), ('site', 'topic', 'content_type', 'object_id'), ('site', 'topic', 'content_type', 'object_id', 'ordering'), ('topic', 'content_type'))", 'object_name': 'TopicalItem', 'unique_together': "(('topic', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_content_type'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['taxonomy.Topic']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'auto_now': 'True', 'blank': 'True'})
        },
        'toolkit.resource': {
            'Meta': {'db_table': "'common_resource'", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'object_name': 'Resource', 'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)"},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'default'", 'blank': 'True'}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'null': 'True', 'blank': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': 'None', 'null': 'True', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'})
        },
        'toolkit.star': {
            'Meta': {'db_table': "'common_star'", 'object_name': 'Star'},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_star'", 'null': 'True', 'blank': 'True', 'default': 'None', 'on_delete': 'models.DO_NOTHING', 'to': "orm['generic.ThreadedComment']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stars'", 'null': 'True', 'blank': 'True', 'default': 'True', 'on_delete': 'models.DO_NOTHING', 'to': "orm['account.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.package': {
            'Meta': {'index_together': "(('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))", 'object_name': 'Package', 'unique_together': "(('site', 'package_name'),)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packages'", 'to': "orm['warehouse.Author']"}),
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'packages'", 'to': "orm['taxonomy.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '9', 'default': '0', 'blank': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'+'", 'default': 'None', 'to': "orm['warehouse.PackageVersion']"}),
            'main_category_names': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_packages'", 'null': 'True', 'to': "orm['taxonomy.Category']", 'blank': 'True'}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root_packages'", 'null': 'True', 'to': "orm['taxonomy.Category']", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'index_together': "(('site', 'package'), ('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'), ('has_award',), ('site', 'has_award'), ('site', 'award_coin'))", 'object_name': 'PackageVersion', 'unique_together': "(('site', 'package', 'version_code'),)"},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('comment.fields.CommentsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.ThreadedComment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'null': 'True', 'blank': 'True'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'null': 'True', 'blank': 'True'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['warehouse.Package']"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
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
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedDevice']", 'symmetrical': 'False', 'blank': 'True'}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedFeature']", 'symmetrical': 'False', 'blank': 'True'}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['warehouse.SupportedLanguage']", 'symmetrical': 'False', 'blank': 'True'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'default': '1'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.supporteddevice': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedDevice'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "''", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedfeature': {
            'Meta': {'unique_together': "(('site', 'code'),)", 'object_name': 'SupportedFeature'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'default': "''", 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'warehouse.supportedlanguage': {
            'Meta': {'object_name': 'SupportedLanguage'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        }
    }

    complete_apps = ['account']