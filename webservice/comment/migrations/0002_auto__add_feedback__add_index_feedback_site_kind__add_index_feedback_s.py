# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table('comment_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_feedback', to=orm['contenttypes.ContentType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.User'], blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['comment.FeedbackType'])),
            ('object_pk', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('model_utils.fields.StatusField')(default='posted', no_check_for_status=True, max_length=100, blank=True)),
            ('is_owner_ignored', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('comment', ['Feedback'])

        # Adding index on 'Feedback', fields ['site', 'kind']
        db.create_index('comment_feedback', ['site_id', 'kind_id'])

        # Adding index on 'Feedback', fields ['site', 'kind', 'created']
        db.create_index('comment_feedback', ['site_id', 'kind_id', 'created'])

        # Adding index on 'Feedback', fields ['site', 'kind', 'status']
        db.create_index('comment_feedback', ['site_id', 'kind_id', 'status'])

        # Adding index on 'Feedback', fields ['site', 'kind', 'status', 'created']
        db.create_index('comment_feedback', ['site_id', 'kind_id', 'status', 'created'])

        # Adding index on 'Feedback', fields ['site', 'user']
        db.create_index('comment_feedback', ['site_id', 'user_id'])

        # Adding index on 'Feedback', fields ['site', 'user', 'created']
        db.create_index('comment_feedback', ['site_id', 'user_id', 'created'])

        # Adding index on 'Feedback', fields ['site', 'user', 'status']
        db.create_index('comment_feedback', ['site_id', 'user_id', 'status'])

        # Adding index on 'Feedback', fields ['site', 'user', 'status', 'created']
        db.create_index('comment_feedback', ['site_id', 'user_id', 'status', 'created'])

        # Adding model 'FeedbackType'
        db.create_table('comment_feedbacktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('level', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal('comment', ['FeedbackType'])

        # Adding unique constraint on 'FeedbackType', fields ['site', 'slug']
        db.create_unique('comment_feedbacktype', ['site_id', 'slug'])

        # Adding unique constraint on 'FeedbackType', fields ['site', 'title']
        db.create_unique('comment_feedbacktype', ['site_id', 'title'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeedbackType', fields ['site', 'title']
        db.delete_unique('comment_feedbacktype', ['site_id', 'title'])

        # Removing unique constraint on 'FeedbackType', fields ['site', 'slug']
        db.delete_unique('comment_feedbacktype', ['site_id', 'slug'])

        # Removing index on 'Feedback', fields ['site', 'user', 'status', 'created']
        db.delete_index('comment_feedback', ['site_id', 'user_id', 'status', 'created'])

        # Removing index on 'Feedback', fields ['site', 'user', 'status']
        db.delete_index('comment_feedback', ['site_id', 'user_id', 'status'])

        # Removing index on 'Feedback', fields ['site', 'user', 'created']
        db.delete_index('comment_feedback', ['site_id', 'user_id', 'created'])

        # Removing index on 'Feedback', fields ['site', 'user']
        db.delete_index('comment_feedback', ['site_id', 'user_id'])

        # Removing index on 'Feedback', fields ['site', 'kind', 'status', 'created']
        db.delete_index('comment_feedback', ['site_id', 'kind_id', 'status', 'created'])

        # Removing index on 'Feedback', fields ['site', 'kind', 'status']
        db.delete_index('comment_feedback', ['site_id', 'kind_id', 'status'])

        # Removing index on 'Feedback', fields ['site', 'kind', 'created']
        db.delete_index('comment_feedback', ['site_id', 'kind_id', 'created'])

        # Removing index on 'Feedback', fields ['site', 'kind']
        db.delete_index('comment_feedback', ['site_id', 'kind_id'])

        # Deleting model 'Feedback'
        db.delete_table('comment_feedback')

        # Deleting model 'FeedbackType'
        db.delete_table('comment_feedbacktype')


    models = {
        'account.user': {
            'Meta': {'object_name': 'User', 'db_table': "'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'comment.feedback': {
            'Meta': {'ordering': "('site', 'created')", 'object_name': 'Feedback', 'index_together': "(('site', 'kind'), ('site', 'kind', 'created'), ('site', 'kind', 'status'), ('site', 'kind', 'status', 'created'), ('site', 'user'), ('site', 'user', 'created'), ('site', 'user', 'status'), ('site', 'user', 'status', 'created'))"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_feedback'", 'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_owner_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.FeedbackType']"}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'posted'", 'no_check_for_status': 'True', 'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['account.User']", 'blank': 'True'})
        },
        'comment.feedbacktype': {
            'Meta': {'unique_together': "(('site', 'slug'), ('site', 'title'))", 'object_name': 'FeedbackType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
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
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['account.User']", 'null': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.threadedcomment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'ThreadedComment', '_ormbases': ['comments.Comment']},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['comments.Comment']"}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.Rating']"}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['generic.ThreadedComment']", 'null': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['comment']