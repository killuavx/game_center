# -*- coding: utf-8 -*-
from activity.models import GiftBag, GiftCard
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from toolkit.helpers import qurl_to
from rest_framework import serializers
from mobapi2.serializers import HyperlinkedModelSerializer, ModelSerializer, Serializer
from mobapi2.helpers import PackageDetailApiUrlEncode, PackageVersionDetailApiUrlEncode
from mobapi2.settings import IMAGE_ICON_SIZE, IMAGE_COVER_SIZE


def giftbag_icon(giftbag):
    try:
        if giftbag.for_version_id:
            version = giftbag.for_version
        else:
            version = giftbag.for_package.versions.latest_published()
        return version.icon[IMAGE_ICON_SIZE].url
    except Exception as e:
        return None


def get_take_url(self, obj):
    view_name = self.opts.router.get_base_name('giftbag-take')
    take_url = reverse(view_name, kwargs=dict(pk=obj.pk))
    try:
        request = self.context.get('request')
        return request.build_absolute_uri(take_url)
    except AttributeError:
        pass
    return take_url


class GiftBagSummarySerializer(HyperlinkedModelSerializer):

    icon = serializers.SerializerMethodField('get_giftbag_icon')

    package_name = serializers.SerializerMethodField('get_package_name')

    def get_package_name(self, obj):
        return obj.for_package.package_name

    package_title = serializers.SerializerMethodField('get_package_title')

    def get_package_title(self, obj):
        try:
            return obj.for_version.title
        except:
            return obj.for_package.title


    def get_giftbag_icon(self, obj):
        if not hasattr(obj, '_icon_url'):
            obj._icon_url = giftbag_icon(obj)
        return obj._icon_url

    publish_datetime = serializers.DateTimeField(source='publish_date')

    expiry_datetime = serializers.DateTimeField(source='expiry_date')

    total_count = serializers.IntegerField(source='cards_total_count')

    remaining_count = serializers.IntegerField(source='cards_remaining_count')

    take = serializers.SerializerMethodField('get_take_url')

    has_took = serializers.SerializerMethodField('get_has_took')

    def get_has_took(self, obj):
        return False

    code = serializers.SerializerMethodField('get_code')

    def get_code(self, obj):
        return None

    get_take_url = get_take_url

    package_url = serializers.SerializerMethodField('get_package_url')

    def get_package_url(self, obj):
        request = self.context.get('request')
        router = self.opts.router
        if obj.for_version_id:
            return PackageVersionDetailApiUrlEncode(obj.for_version_id,
                                                    request=request,
                                                    router=router).get_url()
        else:
            return PackageDetailApiUrlEncode(obj.for_package_id,
                                             request=request,
                                             router=router).get_url()

    class Meta:
        model = GiftBag
        fields = ('url',
                  'title',
                  'package_name',
                  'package_title',
                  'icon',
                  'summary',
                  'publish_datetime',
                  'expiry_datetime',
                  'total_count',
                  'remaining_count',
                  'take',
                  'package_url',
                  'id',
                  'code',
                  'has_took',
        )


class GiftBagDetailSerializer(HyperlinkedModelSerializer):


    package_title = serializers.SerializerMethodField('get_package_title')

    def get_package_title(self, obj):
        try:
            return obj.for_version.title
        except:
            return obj.for_package.title

    package_name = serializers.SerializerMethodField('get_package_name')

    def get_package_name(self, obj):
        return obj.for_package.package_name

    icon = serializers.SerializerMethodField('get_giftbag_icon')

    def get_giftbag_icon(self, obj):
        if not hasattr(obj, '_icon_url'):
            obj._icon_url = giftbag_icon(obj)
        return obj._icon_url

    publish_datetime = serializers.DateTimeField(source='publish_date')

    expiry_datetime = serializers.DateTimeField(source='expiry_date')

    total_count = serializers.IntegerField(source='cards_total_count')

    remaining_count = serializers.IntegerField(source='cards_remaining_count')

    take = serializers.SerializerMethodField('get_take_url')

    get_take_url = get_take_url

    package_url = serializers.SerializerMethodField('get_package_url')

    has_took = serializers.SerializerMethodField('get_has_took')

    def get_has_took(self, obj):
        return False

    code = serializers.SerializerMethodField('get_code')

    def get_code(self, obj):
        return None

    def get_package_url(self, obj):
        request = self.context.get('request')
        router = self.opts.router
        if obj.for_version_id:
            return PackageVersionDetailApiUrlEncode(obj.for_version_id,
                                                    request=request,
                                                    router=router).get_url()
        else:
            return PackageDetailApiUrlEncode(obj.for_package_id,
                                             request=request,
                                             router=router).get_url()

    related_url = serializers.SerializerMethodField('get_related_url')

    def get_related_url(self, obj):
        router = self.opts.router
        reverse_viewname = 'giftbag-list'
        if router:
            reverse_viewname = router.get_base_name(reverse_viewname)
        url = reverse(reverse_viewname)

        request = self.context.get('request')
        url = qurl_to(url, for_package=obj.for_package_id)
        if request:
            url = request.build_absolute_uri(url)
        return url

    class Meta:
        model = GiftBag
        fields = ('url',
                  'title',
                  'package_name',
                  'package_title',
                  'icon',
                  'summary',
                  'usage_description',
                  'issue_description',
                  'publish_datetime',
                  'expiry_datetime',
                  'total_count',
                  'remaining_count',
                  'take',
                  'package_url',
                  'related_url',
                  'code',
                  'id',
                  'has_took',
        )


class GiftCardSerializer(ModelSerializer):

    took_datetime = serializers.DateTimeField(source='took_date')

    class Meta:
        model = GiftCard
        fields = (
            'code',
            'took_datetime',
        )


from activity.models import Note


class NoteSummarySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Note
        fields = (
            'url',
            'title',
        )


class NoteDetailSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Note
        fields = (
            'url',
            'title',
            'description',
        )


class GenerateScratchCardSerializer(Serializer):

    title = serializers.CharField()
    signcode = serializers.CharField()
    is_win = serializers.SerializerMethodField('get_is_win')
    def get_is_win(self, obj):
        return bool(obj.award_coin)


class WinnerScratchCardSerializer(Serializer):

    title = serializers.CharField()
    username = serializers.SerializerMethodField('get_username')

    def get_username(self, obj):
        return obj.winner_name


class AwardScratchCardSerializer(Serializer):

    title = serializers.CharField()
    signcode = serializers.CharField()


from activity.documents.actions.base import Task
from activity.documents.actions.comment import CommentTask
from activity.documents.actions.install import InstallTask
from activity.documents.actions.share import ShareTask
from activity.documents.actions.signin import SigninTask


class TaskStatusSerializer(Serializer):

    progress_current = serializers.IntegerField(source='progress.current')

    progress_standard = serializers.IntegerField(source='progress.standard')

    status = serializers.CharField()

    experience = serializers.SerializerMethodField('get_experience')
    def get_experience(self, obj):
        if obj.status != Task.STATUS.done:
            return 0
        return getattr(obj.rule, 'experience', 0)

    #coin = serializers.SerializerMethodField('get_coin')
    def get_coin(self, obj):
        if obj.status != Task.STATUS.done:
            return 0
        return getattr(obj.rule, 'coin', 0)


class MyTasksStatusSerializer(Serializer):

    summary = serializers.SerializerMethodField('get_summary')

    def get_summary(self, obj):
        experience = coin = 0
        for key, task in obj.items():
            if not task:
                continue
            if not isinstance(task, Task):
                continue
            if task.status == Task.STATUS.done:
                experience += getattr(task.rule, 'experience', 0)
                coin += getattr(task.rule, 'coin', 0)

        msgs = list()
        if experience:
            msgs.append("%d经验" % experience)
        if coin:
            msgs.append("%d金币" % coin)

        if msgs:
            return "今天你已攒到%s, %s" % (",".join(msgs), "继续加油哦~")
        else:
            return "今天你还没有完成任务, 快来参加吧~"

    signin = TaskStatusSerializer(many=False)
    share = TaskStatusSerializer(many=False)
    install = TaskStatusSerializer(many=False)
    comment = TaskStatusSerializer(many=False)

    @classmethod
    def factory(cls, user, action_datetime=None):
        action_datetime = action_datetime.astimezone() if action_datetime else now().astimezone()

        comment_task = CommentTask.factory_task(user, action_datetime)
        comment_task.rule = comment_task.rule if comment_task.id else CommentTask.factory_rule()
        comment_task.user = user

        share_task = ShareTask.factory_task(user, action_datetime)
        share_task.rule = share_task.rule \
            if share_task.id else ShareTask.factory_rule()
        share_task.user = user

        install_task = InstallTask.factory_task(user, action_datetime)
        install_task.rule = install_task.rule if install_task.id else InstallTask.factory_rule()
        install_task.user = user

        signin_task = SigninTask.factory_task(user, action_datetime)
        signin_task.rule = signin_task.rule if signin_task.id else SigninTask.factory_rule()
        signin_task.user = user

        data = dict(
            signin=signin_task,
            comment=comment_task,
            share=share_task,
            install=install_task,
        )
        return cls(data)


from activity.models import Bulletin, Activity


class BulletinSummarySerializer(ModelSerializer):

    page_url = serializers.SerializerMethodField('get_page_url')
    def get_page_url(self, obj):
        request = self.context.get('request')
        url =  reverse('apiv2-bulletin-richpage', kwargs=dict(pk=obj.pk))
        if request:
            return request.build_absolute_uri(url)
        return url

    class Meta:
        model = Bulletin
        fields = (
            'page_url',
            'title',
            'summary',
            'publish_date',
        )


class ActivitySummarySerializer(ModelSerializer):

    page_url = serializers.SerializerMethodField('get_page_url')
    def get_page_url(self, obj):
        request = self.context.get('request')
        url =  reverse('apiv2-activity-richpage', kwargs=dict(pk=obj.pk))
        if request:
            return request.build_absolute_uri(url)
        return url

    cover = serializers.SerializerMethodField('get_cover_url')
    def get_cover_url(self, obj):
        try:
            return obj.cover[IMAGE_COVER_SIZE].url
        except:
            return None

    class Meta:
        model = Activity
        fields = (
            'page_url',
            'title',
            'cover',
            'is_active',
            'publish_date',
        )


from datetime import datetime
from mobapi2.rest_clients import android_api
from mobapi2.activity.throttling import *


class NotificationSerializer(Serializer):

    def __init__(self, view, request, *args, **kwargs):
        assert request
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        self.context['request'] = request
        self.context['view'] = view

    activity = serializers.SerializerMethodField('get_activity')

    def get_activity(self, obj):
        #request = self.context.get('request')
        response = android_api.activities.get()
        try:
            latest = response.data['results'][0]
            result = dict(
                new_count=1 if latest['is_active'] else 0,
                latest=latest,
                #active=latest['is_active']
            )
        except Exception as e:
            result = dict(new_count=0, latest=None, active=False)
        return result

    bulletin = serializers.SerializerMethodField('get_bulletin')

    def get_bulletin(self, obj):
        request = self.context.get('request')
        response = android_api.bulletins.get()
        data = response.data
        result = dict(new_count=0, latest=None)
        if data['count']:
            result['new_count'] = self._bulletin_newcount(request, data)
            #result['active'] = result['new_count'] > 0
            result['latest'] = data['results'][0]
        return result

    def _bulletin_newcount(self, request, data):
        new_count = 0
        n = now().astimezone()
        for item in data['results']:
            cur_dt = datetime.fromtimestamp(int(item['publish_date']),
                                            tz=n.tzinfo)
            if (n - cur_dt) < timedelta(days=3):
                new_count += 1
        return new_count

    scratchcard = serializers.SerializerMethodField('get_scratchcard')

    def get_scratchcard(self, obj):
        throttle = ScratchCardPlayDailyThrottle()
        active = throttle.check_allowed(request=self.context.get('request'),
                                        view=self.context.get('view'))
        return dict(active=active)

    lottery = serializers.SerializerMethodField('get_lottery')

    def get_lottery(self, obj):
        throttle = LotteryPlayDailyThrottle()
        active = throttle.check_allowed(request=self.context.get('request'),
                                        view=self.context.get('view'))

        res = android_api.lotteries.get('active')
        if res.status == 200:
            active = active and res.data['status'] == LotterySerializer.STATUS.inprogress
        else:
            active = False
        return dict(active=active)


from model_utils.choices import Choices
from activity.models import Lottery, LotteryPrize, LotteryWinning
from django.utils import timezone
from toolkit.models import CONTENT_STATUS_PUBLISHED
from activity.documents.actions import lottery as lottery_doc


class LotterySerializer(HyperlinkedModelSerializer):

    STATUS = Choices(
        ('comingsoon', 'comingsoon', '即将开始'),
        ('inprogress', 'inprogress', '进行中'),
        ('finish', 'finish', '活动结束'),
        ('expired', 'expired', '活动截止'),
    )

    def __init__(self, instance=None, now=None, *args, **kwargs):
        self.now = now if now else timezone.now().astimezone()
        super(LotterySerializer, self).__init__(instance=instance, *args, **kwargs)

    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        if obj.status != CONTENT_STATUS_PUBLISHED:
            return self.STATUS.comingsoon

        if obj.publish_date.astimezone() >= self.now and self.now < obj.expiry_date.astimezone():
            return self.STATUS.comingsoon

        if self.now > obj.expiry_date.astimezone():
            return self.STATUS.expired

        return self.STATUS.inprogress

    play = serializers.SerializerMethodField('get_play_url')

    def get_play_url(self, obj):
        request = self.context.get('request')
        base_name = self.opts.router.get_base_name('lottery-play')
        url = reverse(base_name, kwargs=dict(pk=obj.pk))
        if request:
            return request.build_absolute_uri(url)
        return url

    winning_url = serializers.SerializerMethodField('get_winning_url')

    def get_winning_url(self, obj):
        request = self.context.get('request')
        base_name = self.opts.router.get_base_name('lottery-winnings-richpage')
        url = reverse(base_name, kwargs=dict(pk=obj.pk))
        if request:
            return request.build_absolute_uri(url)
        return url

    class Meta:
        model = Lottery
        fields = (
            'url',
            'title',
            'cost_coin',
            'status',
            'publish_date',
            'expiry_date',
        )


class LotterySummarySerializer(LotterySerializer):

    class Meta:
        model = Lottery
        fields = (
            'url',
            'title',
            'cost_coin',
            'status',
            'publish_date',
            'expiry_date',
        )


class LotteryDetailSerializer(LotterySerializer):

    prizes = serializers.SerializerMethodField('get_prizes')

    def get_prizes(self, obj):
        prizes = list()
        for p in sorted(obj.prizes.all(),
                        key=lambda item:item.level,
                        reverse=True):
            prizes.append(dict(
                level=p.level,
                group=p.group,
                title=p.title,
                level_name=p.level_name,
            ))
        return prizes

    winnings = serializers.SerializerMethodField('get_winnings')

    def get_winnings(self, obj):
        winners = list()
        for winning in lottery_doc.LotteryWinningAction\
                        .objects.lottery_winning_list(obj.pk)[0:5]:
            try:
                winners.append(dict(username=winning.username,
                                    level_name=winning.prize_level_name,
                                    group=winning.prize_group,
                                    title=winning.prize_title))
            except:
                pass
        return winners


    class Meta:
        model = Lottery
        fields = (
            'url',
            'title',
            'play',
            'prizes',
            'cost_coin',
            'description',
            'status',
            'publish_date',
            'expiry_date',
            'takepartin_count',
            'winnings',
            'winning_url',
        )


class LotteryPrizeWinningSerializer(Serializer):

    prize_group = serializers.SerializerMethodField('get_group')

    prize_title = serializers.SerializerMethodField('get_title')

    prize_prompt = serializers.SerializerMethodField('get_prompt')

    level = serializers.SerializerMethodField('get_level')

    def get_level(self, obj):
        prize, _ = obj
        return prize.level

    def get_prompt(self, obj):
        prize, _ = obj
        return prize.win_prompt

    def get_title(self, obj):
        prize, _ = obj
        return "%s: %s" % (prize.level_name, prize.title)

    def get_group(self, obj):
        prize, _ = obj
        return prize.group

    winning_detail_url = serializers.SerializerMethodField('get_winning_detail_url')

    def get_winning_detail_url(self, obj):
        prize, winning = obj
        request = self.context.get('request')
        view_name = self.opts.router.get_base_name('lottery-winning-detail-richpage')
        url = reverse(view_name, kwargs=dict(winning_id=winning.pk))
        if request:
            return request.build_absolute_uri(url)
        return url

    def save_object(self, obj, **kwargs):
        pass

    def delete_object(self, obj):
        pass

    class Meta:
        fields = (
            'level',
            'prize_group',
            'prize_title',
            'prize_prompt',
            'winning_detail_url',
        )

