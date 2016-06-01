# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LotteryPrize'
        db.create_table('activity_lotteryprize', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('lottery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Lottery'], related_name='prizes')),
            ('group', self.gf('django.db.models.fields.IntegerField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('total_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('win_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('award_coin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('win_prompt', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('activity', ['LotteryPrize'])

        # Adding unique constraint on 'LotteryPrize', fields ['lottery', 'group', 'level']
        db.create_unique('activity_lotteryprize', ['lottery_id', 'group', 'level'])

        # Adding index on 'LotteryPrize', fields ['lottery', 'status']
        db.create_index('activity_lotteryprize', ['lottery_id', 'status'])

        # Adding index on 'LotteryPrize', fields ['lottery', 'group', 'level']
        db.create_index('activity_lotteryprize', ['lottery_id', 'group', 'level'])

        # Adding model 'LotteryWinning'
        db.create_table('activity_lotterywinning', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'], related_name='lotterywinnings')),
            ('prize', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.LotteryPrize'], related_name='winnings')),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=500, default='')),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('win_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('accept_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('activity', ['LotteryWinning'])

        # Adding index on 'LotteryWinning', fields ['prize', 'status']
        db.create_index('activity_lotterywinning', ['prize_id', 'status'])

        # Adding index on 'LotteryWinning', fields ['prize', 'status', 'win_date']
        db.create_index('activity_lotterywinning', ['prize_id', 'status', 'win_date'])

        # Adding model 'Lottery'
        db.create_table('activity_lottery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('cost_coin', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('takepartin_times', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('takepartin_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('activity', ['Lottery'])

        # Adding index on 'Lottery', fields ['status', 'publish_date']
        db.create_index('activity_lottery', ['status', 'publish_date'])

        # Adding index on 'Lottery', fields ['status', 'publish_date', 'expiry_date']
        db.create_index('activity_lottery', ['status', 'publish_date', 'expiry_date'])


    def backwards(self, orm):
        # Removing index on 'Lottery', fields ['status', 'publish_date', 'expiry_date']
        db.delete_index('activity_lottery', ['status', 'publish_date', 'expiry_date'])

        # Removing index on 'Lottery', fields ['status', 'publish_date']
        db.delete_index('activity_lottery', ['status', 'publish_date'])

        # Removing index on 'LotteryWinning', fields ['prize', 'status', 'win_date']
        db.delete_index('activity_lotterywinning', ['prize_id', 'status', 'win_date'])

        # Removing index on 'LotteryWinning', fields ['prize', 'status']
        db.delete_index('activity_lotterywinning', ['prize_id', 'status'])

        # Removing index on 'LotteryPrize', fields ['lottery', 'group', 'level']
        db.delete_index('activity_lotteryprize', ['lottery_id', 'group', 'level'])

        # Removing index on 'LotteryPrize', fields ['lottery', 'status']
        db.delete_index('activity_lotteryprize', ['lottery_id', 'status'])

        # Removing unique constraint on 'LotteryPrize', fields ['lottery', 'group', 'level']
        db.delete_unique('activity_lotteryprize', ['lottery_id', 'group', 'level'])

        # Deleting model 'LotteryPrize'
        db.delete_table('activity_lotteryprize')

        # Deleting model 'LotteryWinning'
        db.delete_table('activity_lotterywinning')

        # Deleting model 'Lottery'
        db.delete_table('activity_lottery')


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
        'activity.activity': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Activity', 'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))"},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True', 'null': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']"}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'activitys'"}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'activity.bulletin': {
            'Meta': {'ordering': "('-publish_date',)", 'index_together': "(('site', 'status'), ('site', 'status', 'publish_date', 'expiry_date'))", 'object_name': 'Bulletin'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'bulletins'"})
        },
        'activity.giftbag': {
            'Meta': {'ordering': "('-publish_date',)", 'index_together': "(('site', 'for_package'), ('site', 'for_package', 'for_version'), ('site', 'publish_date'), ('site', 'for_package', 'publish_date'), ('site', 'for_package', 'for_version', 'publish_date'), ('site', 'status', 'publish_date'), ('site', 'status', 'for_package', 'publish_date'), ('site', 'status', 'for_package', 'for_version', 'publish_date'))", 'object_name': 'GiftBag'},
            'cards_remaining_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cards_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'for_package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'giftbags'"}),
            'for_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['warehouse.PackageVersion']", 'related_name': "'giftbags'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issue_description': ('django.db.models.fields.TextField', [], {}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'usage_description': ('django.db.models.fields.TextField', [], {})
        },
        'activity.giftcard': {
            'Meta': {'unique_together': "(('site', 'giftbag', 'code'),)", 'object_name': 'GiftCard', 'index_together': "(('site', 'giftbag', 'owner'), ('site', 'giftbag', 'owner', 'took_date'), ('site', 'owner'))"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'giftbag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.GiftBag']", 'related_name': "'cards'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'on_delete': 'models.DO_NOTHING', 'null': 'True', 'to': "orm['account.User']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'took_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'activity.lottery': {
            'Meta': {'object_name': 'Lottery', 'index_together': "(('status', 'publish_date'), ('status', 'publish_date', 'expiry_date'))"},
            'cost_coin': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'takepartin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'takepartin_times': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'activity.lotteryprize': {
            'Meta': {'unique_together': "(('lottery', 'group', 'level'),)", 'object_name': 'LotteryPrize', 'index_together': "(('lottery', 'status'), ('lottery', 'group', 'level'))"},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'lottery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Lottery']", 'related_name': "'prizes'"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'win_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'win_prompt': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'activity.lotterywinning': {
            'Meta': {'object_name': 'LotteryWinning', 'index_together': "(('prize', 'status'), ('prize', 'status', 'win_date'))"},
            'accept_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prize': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.LotteryPrize']", 'related_name': "'winnings'"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']", 'related_name': "'lotterywinnings'"}),
            'win_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'activity.note': {
            'Meta': {'unique_together': "(('site', 'slug'),)", 'object_name': 'Note'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
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
        'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic.Keyword']", 'related_name': "'assignments'"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
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
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
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
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'taxonomy.topicalitem': {
            'Meta': {'unique_together': "(('topic', 'content_type', 'object_id'),)", 'ordering': "('ordering',)", 'index_together': "(('site', 'topic'), ('site', 'topic', 'content_type'), ('site', 'topic', 'content_type', 'object_id'), ('site', 'topic', 'content_type', 'object_id', 'ordering'), ('topic', 'content_type'))", 'object_name': 'TopicalItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'topic_content_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taxonomy.Topic']", 'related_name': "'items'"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'auto_now': 'True'})
        },
        'toolkit.resource': {
            'Meta': {'unique_together': "(('site', 'content_type', 'object_pk', 'kind', 'alias'),)", 'db_table': "'common_resource'", 'ordering': "('site', 'content_type', 'object_pk', 'kind')", 'index_together': "(('site', 'content_type'), ('site', 'content_type', 'object_pk'), ('site', 'content_type', 'object_pk', 'kind'))", 'object_name': 'Resource'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'default': "'default'", 'blank': 'True'}),
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '500'}),
            'file_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'default': '0', 'blank': 'True'})
        },
        'toolkit.star': {
            'Meta': {'object_name': 'Star', 'db_table': "'common_star'"},
            'by_comment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'default': 'None', 'to': "orm['generic.ThreadedComment']", 'on_delete': 'models.DO_NOTHING', 'related_name': "'content_star'"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'null': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'default': 'True', 'to': "orm['account.User']", 'on_delete': 'models.DO_NOTHING', 'related_name': "'stars'"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'warehouse.author': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Author'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True', 'null': 'True'}),
            'resources': ('toolkit.fields.MultiResourceField', [], {'object_id_field': "'object_pk'", 'to': "orm['toolkit.Resource']"}),
            'resources_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.package': {
            'Meta': {'unique_together': "(('site', 'package_name'),)", 'object_name': 'Package', 'index_together': "(('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'))"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Author']", 'related_name': "'packages'"}),
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'packages'"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True', 'db_index': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_version': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['warehouse.PackageVersion']", 'null': 'True', 'related_name': "'+'"}),
            'main_category_names': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "''"}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'primary_packages'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'root_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['taxonomy.Category']", 'related_name': "'root_packages'"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'no_check_for_status': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'auto_now_add': 'True'}),
            'workspace': ('mezzanine.core.fields.FileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'})
        },
        'warehouse.packageversion': {
            'Meta': {'unique_together': "(('site', 'package', 'version_code'),)", 'object_name': 'PackageVersion', 'index_together': "(('site', 'package'), ('site', 'id'), ('site', 'status'), ('site', 'status', 'released_datetime'), ('has_award',), ('site', 'has_award'), ('site', 'award_coin'), ('site', 'reported'), ('site', 'reported', 'status'))"},
            'award_coin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('comment.fields.CommentsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.ThreadedComment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'di_download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'di_download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'di_download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'download': ('toolkit.fields.PkgFileField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '9', 'default': '0', 'blank': 'True'}),
            'download_md5': ('django.db.models.fields.CharField', [], {'max_length': '40', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'download_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'has_award': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['warehouse.Package']", 'related_name': "'versions'"}),
            'released_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'reported': ('warehouse.models.PkgReportField', [], {'default': 'False'}),
            'reported_adv': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_gplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'draft'", 'blank': 'True', 'no_check_for_status': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "''", 'blank': 'True'}),
            'supported_devices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedDevice']"}),
            'supported_features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedFeature']"}),
            'supported_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['warehouse.SupportedLanguage']"}),
            'tags_text': ('toolkit.fields.TagField', [], {'default': "''"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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

    complete_apps = ['activity']