# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PetitionPackageVersion'
        db.create_table('comment_petitionpackageversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True, null=True)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True, null=True)),
            ('version_name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True, null=True)),
        ))
        db.send_create_signal('comment', ['PetitionPackageVersion'])

        # Adding unique constraint on 'PetitionPackageVersion', fields ['site', 'url', 'title', 'package_name', 'version_name']
        db.create_unique('comment_petitionpackageversion', ['site_id', 'url', 'title', 'package_name', 'version_name'])

        # Adding model 'Petition'
        db.create_table('comment_petition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['account.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, default=None, blank=True, null=True)),
            ('petition_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comment.PetitionPackageVersion'])),
            ('packageversion', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['warehouse.PackageVersion'])),
            ('status', self.gf('model_utils.fields.StatusField')(max_length=100, default='posted', blank=True, no_check_for_status=True)),
            ('verifier', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['account.User'], related_name='confirm_petitions')),
            ('confirmed_at', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('finished_at', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('rejected_at', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('deleted_at', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
        ))
        db.send_create_signal('comment', ['Petition'])

        # Adding index on 'Petition', fields ['site', 'user', 'created']
        db.create_index('comment_petition', ['site_id', 'user_id', 'created'])

        # Adding index on 'Petition', fields ['site', 'user', 'petition_for', 'packageversion']
        db.create_index('comment_petition', ['site_id', 'user_id', 'petition_for_id', 'packageversion_id'])

        # Adding index on 'Petition', fields ['site', 'user', 'petition_for', 'packageversion', 'status']
        db.create_index('comment_petition', ['site_id', 'user_id', 'petition_for_id', 'packageversion_id', 'status'])

        # Adding index on 'Petition', fields ['site', 'user', 'packageversion']
        db.create_index('comment_petition', ['site_id', 'user_id', 'packageversion_id'])

        # Adding index on 'Petition', fields ['site', 'user', 'packageversion', 'status']
        db.create_index('comment_petition', ['site_id', 'user_id', 'packageversion_id', 'status'])

        # Adding index on 'Petition', fields ['site', 'user', 'packageversion', 'status', 'finished_at']
        db.create_index('comment_petition', ['site_id', 'user_id', 'packageversion_id', 'status', 'finished_at'])


    def backwards(self, orm):
        # Removing index on 'Petition', fields ['site', 'user', 'packageversion', 'status', 'finished_at']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'packageversion_id', 'status', 'finished_at'])

        # Removing index on 'Petition', fields ['site', 'user', 'packageversion', 'status']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'packageversion_id', 'status'])

        # Removing index on 'Petition', fields ['site', 'user', 'packageversion']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'packageversion_id'])

        # Removing index on 'Petition', fields ['site', 'user', 'petition_for', 'packageversion', 'status']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'petition_for_id', 'packageversion_id', 'status'])

        # Removing index on 'Petition', fields ['site', 'user', 'petition_for', 'packageversion']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'petition_for_id', 'packageversion_id'])

        # Removing index on 'Petition', fields ['site', 'user', 'created']
        db.delete_index('comment_petition', ['site_id', 'user_id', 'created'])

        # Removing unique constraint on 'PetitionPackageVersion', fields ['site', 'url', 'title', 'package_name', 'version_name']
        db.delete_unique('comment_petitionpackageversion', ['site_id', 'url', 'title', 'package_name', 'version_name'])

        # Deleting model 'PetitionPackageVersion'
        db.delete_table('comment_petitionpackageversion')

        # Deleting model 'Petition'
        db.delete_table('comment_petition')


    models = {
        'account.user': {
            'Meta': {'object_name': 'User', 'db_table': "'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comment.feedback': {
            'Meta': {'ordering': "('site', 'created')", 'index_together': "(('site', 'kind'), ('site', 'kind', 'created'), ('site', 'kind', 'status'), ('site', 'kind', 'status', 'created'), ('site', 'user'), ('site', 'user', 'created'), ('site', 'user', 'status'), ('site', 'user', 'status', 'created'))", 'object_name': 'Feedback'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'contact_im_qq': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'content_type_set_for_feedback'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'is_owner_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.FeedbackType']", 'related_name': "'feedbacks'"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'posted'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['account.User']"})
        },
        'comment.feedbacktype': {
            'Meta': {'unique_together': "(('site', 'slug'), ('site', 'title'))", 'ordering': "('-level',)", 'object_name': 'FeedbackType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'comment.petition': {
            'Meta': {'ordering': "('created',)", 'index_together': "(('site', 'user', 'created'), ('site', 'user', 'petition_for', 'packageversion'), ('site', 'user', 'petition_for', 'packageversion', 'status'), ('site', 'user', 'packageversion'), ('site', 'user', 'packageversion', 'status'), ('site', 'user', 'packageversion', 'status', 'finished_at'))", 'object_name': 'Petition'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'confirmed_at': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'deleted_at': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'finished_at': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'packageversion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['warehouse.PackageVersion']"}),
            'petition_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.PetitionPackageVersion']"}),
            'rejected_at': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'posted'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['account.User']"}),
            'verifier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['account.User']", 'related_name': "'confirm_petitions'"})
        },
        'comment.petitionpackageversion': {
            'Meta': {'unique_together': "(('site', 'url', 'title', 'package_name', 'version_name'),)", 'object_name': 'PetitionPackageVersion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True', 'null': 'True'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'db_table': "'django_comments'", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'content_type_set_for_comment'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['account.User']", 'related_name': "'comment_comments'"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
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
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'null': 'True', 'related_name': "'ratings'"}),
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
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.ThreadedComment']", 'null': 'True', 'related_name': "'comments'"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taxonomy.category': {
            'Meta': {'unique_together': "(('site', 'slug'), ('site', 'name'))", 'ordering': "('ordering',)", 'object_name': 'Category'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'children'"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''", 'blank': 'True', 'null': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'taxonomy.topic': {
            'Meta': {'unique_together': "(('site', 'slug'), ('site', 'name'))", 'ordering': "('ordering',)", 'object_name': 'Topic'},
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
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Topic']", 'related_name': "'children'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'unique_together': "(('topic', 'content_type', 'object_id'),)", 'ordering': "('ordering',)", 'index_together': "(('topic', 'content_type'),)", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'})
        },
        'toolkit.star': {
            'Meta': {'object_name': 'Star', 'db_table': "'common_star'"},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['generic.ThreadedComment']", 'on_delete': 'models.DO_NOTHING', 'related_name': "'content_star'", 'blank': 'True', 'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'related_name': "'stars'", 'blank': 'True', 'null': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'})
        },
        'warehouse.package': {
            'Meta': {'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'packages'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'di_download': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'download': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
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
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'}),
            'version_code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'whatsnew': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        }
    }

    complete_apps = ['comment']