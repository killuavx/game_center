# -*- coding: utf-8 -*-
from kombu import uuid
from model_utils import FieldTracker
from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.db.models.query import QuerySet
from django.utils.timezone import now
from mezzanine.core.models import TimeStamped, CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT
from mezzanine.utils.models import get_user_model_name

from activity.managers import GiftBagManager, GiftCardManager, BulletinManager, ActivityManager
from toolkit.models import PublishDisplayable, SiteRelated
from toolkit.helpers import current_request, get_global_site
from toolkit.helpers import sync_status_from


class EmptyRemainingGiftCard(Exception):
    pass


user_model_name = get_user_model_name()


class GiftBag(PublishDisplayable,
              SiteRelated,
              TimeStamped,
              models.Model):

    objects = GiftBagManager()

    title = models.CharField(max_length=500)

    for_package = models.ForeignKey('warehouse.Package',
                                    verbose_name='应用',
                                    related_name='giftbags')

    for_version = models.ForeignKey('warehouse.PackageVersion',
                                    verbose_name='应用版本',
                                    related_name='giftbags',
                                    null=True,
                                    blank=True)

    summary = models.CharField(verbose_name='礼包内容', max_length=500)

    usage_description = models.TextField(verbose_name='使用方法')

    issue_description = models.TextField(verbose_name='发号说明')

    cards_remaining_count = models.IntegerField(default=0, editable=False)

    cards_total_count = models.IntegerField(default=0, editable=False)

    publisher = models.ForeignKey(user_model_name,
                                  on_delete=models.DO_NOTHING)

    tracker = FieldTracker()

    def clean(self):
        super(GiftBag, self).clean()
        if self.for_version_id is not None:
            if self.for_version.package_id != self.for_package_id:
                raise ValidationError('PackageVersion (%s) Does not belong to Package (%s)' %(self.for_version,
                                                                                              self.for_package))

    def save(self, *args, **kwargs):
        if self.publisher_id is None:
            self.publisher = current_request().user
        if self.cards_remaining_count == 0:
            self.status = CONTENT_STATUS_DRAFT
        return super(GiftBag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '礼包'
        verbose_name_plural = '礼包'
        index_together = (
            ('site', 'for_package',),
            ('site', 'for_package', 'for_version'),

            ('site', 'publish_date', ),
            ('site', 'for_package', 'publish_date',),
            ('site', 'for_package', 'for_version', 'publish_date', ),

            ('site', 'status', 'publish_date', ),
            ('site', 'status', 'for_package', 'publish_date',),
            ('site', 'status', 'for_package', 'for_version', 'publish_date', ),
        )
        ordering = ('-publish_date', )

    @transaction.commit_on_success
    def take_by(self, user, took_date=None):
        dt = now().astimezone() if took_date is None else took_date
        try:
            card = self.cards.select_for_update().remaining()[0]
        except IndexError:
            raise EmptyRemainingGiftCard
        else:
            card.owner = user
            card.took_date = dt
            card.save()
            return card

    def has_took_by(self, user):
        return self.get_took_card_by(user).exists()

    def get_took_cards_by(self, user):
        return self.cards.filter(owner_id=user.pk)

    def __str__(self):
        return self.title

    def is_status_published(self):
        return self.status==CONTENT_STATUS_PUBLISHED


class GiftCardQuerySet(QuerySet):

    def remaining(self):
        table = self.model._meta.db_table
        return self.extra(where=['%s.owner_id IS NULL' % table])

    def has_took(self, giftbag, user):
        if isinstance(giftbag, int):
            giftbag_id = giftbag
        else:
            giftbag_id = giftbag.pk
        return self.filter(giftbag_id=giftbag_id, owner=user.pk).exists()

    def took_by(self, user):
        return self.filter(owner_id=user.pk)

    def took_from(self, giftbag):
        if isinstance(giftbag, int):
            giftbag_id = giftbag
        else:
            giftbag_id = giftbag.pk
        return self.filter(giftbag_id=giftbag_id)


class GiftCard(SiteRelated, models.Model):

    objects = GiftCardManager.for_queryset_class(GiftCardQuerySet)()

    giftbag = models.ForeignKey(GiftBag, related_name='cards')

    code = models.CharField(max_length=50, editable=False)

    owner = models.ForeignKey(user_model_name,
                              null=True,
                              blank=True,
                              on_delete=models.DO_NOTHING)

    took_date = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name = '礼品码'
        verbose_name_plural = '礼品码'
        unique_together = (
            ('site', 'giftbag', 'code'),
        )
        index_together = (
            ('site', 'giftbag', 'owner'),
            ('site', 'giftbag', 'owner', 'took_date'),
            ('site', 'owner'),
        )

    def __str__(self):
        return "%s: %s" % (self.giftbag_id, self.code)


from import_export import resources, widgets, fields as ie_fields


class CodeWidget(widgets.CharWidget):

    def clean(self, value):
        if value:
            return value.strip()
        return value


class GiftCardResource(resources.ModelResource):

    giftbag = ie_fields.Field(column_name='giftbag',
                              attribute='giftbag_id',
                              widget=widgets.IntegerWidget())

    code = ie_fields.Field(column_name='code',
                           attribute='code',
                           widget=CodeWidget())

    class Meta:
        model = GiftCard
        fields = ('giftbag', 'code', )
        import_id_fields = ['giftbag', 'code']

    def get_instance(self, instance_loader, row):
        giftbag_field = self.fields['giftbag']
        code_field = self.fields['code']
        model = self._meta.model
        try:
            return model.objects.get(site_id=get_global_site().pk,
                                     giftbag_id=giftbag_field.clean(row),
                                     code=code_field.clean(row))
        except model.DoesNotExist:
            return None


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete


@receiver(pre_save, sender=GiftCard)
def giftcard_pre_save_took(sender, instance, **kwargs):
    if instance.pk and instance.tracker.has_changed('owner_id'):
        instance._owner_changed = True


@receiver(post_save, sender=GiftCard)
def giftcard_post_save_took(sender, instance, created, **kwargs):
    if getattr(instance, '_owner_changed', False):
        del instance._owner_changed
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.save()


@receiver(post_save, sender=GiftCard)
def giftcard_created(sender, instance, created, **kwargs):
    if created:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()


@receiver(post_delete, sender=GiftCard)
def giftcard_delete(sender, instance, **kwargs):
    try:
        giftbag = instance.giftbag
        giftbag.cards_remaining_count = giftbag.cards.remaining().count()
        giftbag.cards_total_count = giftbag.cards.count()
        giftbag.save()
    except GiftBag.DoesNotExist:
        pass


from warehouse.tasks import sync_package


FLAG_GIFTBAG = '礼包'


def remove_giftbag_flag(giftbag):
    package = giftbag.for_package
    version = giftbag.for_version
    def _remove_tag(inst, tag):
        inst.tags_text = inst.tags_text.replace(tag, '').replace('  ', ' ')
        inst.save()
        return inst

    if version:
        _remove_tag(version, FLAG_GIFTBAG)

    version_flag = False
    for v in package.versions.published():
        if FLAG_GIFTBAG in v.tags_text:
            version_flag = True
            break
    if not version_flag:
        _remove_tag(package, FLAG_GIFTBAG)

    sync_package.apply_async((package.pk,), countdown=10)


def add_giftbag_flag(giftbag):
    version = giftbag.for_version
    package = giftbag.for_package
    version_changed = False
    if version and FLAG_GIFTBAG not in version.tags_text:
        version.tags_text = FLAG_GIFTBAG + " " + version.tags_text
        version.save()
        version_changed = True


    package_changed = False
    if FLAG_GIFTBAG not in package.tags_text:
        package.tags_text = FLAG_GIFTBAG + ' ' + package.tags_text
        package.save()
        package_changed = True

    if package_changed or (version_changed and package.latest_version_id == version.pk):
        sync_package.apply_async((package.pk,), countdown=10)


giftbag_sync_flag = '_sync_package_flag_type'


@receiver(pre_save, sender=GiftBag)
def change_giftbag_cards_count(sender, instance, **kwargs):
    if instance.tracker.has_changed('status') and instance.is_status_published():
        setattr(instance, giftbag_sync_flag, 'add')
        return

    if not instance.pk and instance.tracker.has_changed('status') and not instance.is_status_published():
        setattr(instance, giftbag_sync_flag, 'remove')
        return

    if not instance.is_status_published():
        return

    total_grow = False
    if instance.cards_total_count > instance.tracker.previous('cards_total_count'):
        total_grow = True

    if instance.tracker.previous('cards_total_count') == 0 and total_grow:
        setattr(instance, giftbag_sync_flag, 'add')
    elif instance.cards_remaining_count == 0:
        setattr(instance, giftbag_sync_flag, 'remove')


@receiver(post_save, sender=GiftBag)
def sync_giftbag_package_flag(sender, instance, **kwargs):
    sync_type = getattr(instance, giftbag_sync_flag, None)
    if sync_type == 'remove':
        remove_giftbag_flag(instance)
    elif sync_type == 'add':
        add_giftbag_flag(instance)


@receiver(post_delete, sender=GiftBag)
def delete_package_giftbag_flag(sender, instance, **kwargs):
    remove_giftbag_flag(instance)


from django.utils.timezone import utc
#from activity import documents as docs

#@receiver(post_save, sender=GiftBag)
"""
def giftbag_post_save_sync(sender, instance, created, **kwargs):
    defaults=dict(
        site_id=instance.site_id,
        title=instance.title,
        for_package_id=instance.for_package_id,
        for_version_id=instance.for_version_id,
        summary=instance.summary,
        usage_description=instance.usage_description,
        issue_description=instance.issue_description,
        publish_date=instance.publish_date.astimezone(utc),
        expirty_date=instance.expiry_date.astimezone(utc) if instance.expiry_date else None,
        cards_total_count=instance.cards_total_count,
        cards_remaining_count=instance.cards_remaining_count,
    )
    gb, created = docs.GiftBag.objects.get_or_create(id=instance.pk,
                                            defaults=defaults)
    if not created:
        for k,v in defaults.items():
            setattr(gb, k, v)
"""

from toolkit.managers import CurrentSiteManager


class Note(SiteRelated,
           models.Model):

    objects = CurrentSiteManager()

    all_objects = models.Manager()

    slug = models.SlugField(max_length=150)

    title = models.CharField(max_length=250)

    description = models.TextField()

    #rich_description = RichTextField()

    class Meta:
        verbose_name_plural = verbose_name = '说明'
        unique_together = (
            ('site', 'slug'),
        )


import os
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Ownable, MetaData
from mezzanine.core.fields import FileField
from easy_thumbnails.fields import ThumbnailerImageField

ACTIVITY_DIRECTORY_DTFORMAT = 'activity/%Y/%m/%d/%H%M-%S-%f'


def activity_profile_upload_to(instance, filename):
    activity_workspace_by_created(instance)
    basename = os.path.basename(filename)
    return "%s/%s" % (instance.workspace.name, basename)


def activity_workspace_by_created(instance):
    if not instance.workspace:
        if not instance.created:
            instance.created = now().astimezone()
        else:
            instance.created = instance.created.astimezone()
        sd = instance.created
        instance.workspace = sd.strftime(ACTIVITY_DIRECTORY_DTFORMAT)


class Activity(SiteRelated,
               MetaData,
               PublishDisplayable,
               TimeStamped,
               Ownable,
               models.Model):

    objects = ActivityManager()

    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=2000, null=True)

    cover = ThumbnailerImageField(
        default='',
        upload_to=activity_profile_upload_to,
        blank=True,
        max_length=500,
    )

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          help_text='!!切勿随意修改!!',
                          format='File')

    objects = ActivityManager()

    content = RichTextField(help_text="""1.添加标签class属性:event-open-activity,客户端即可点击跳转至抽奖活动UI\n"""
        """2.添加标签class属性:lottery-{id}, {id}代表抽奖ID即可在活动结束后, 点击活动页面进入获奖列表页面"""
    )

    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
        unique_together = (
            ('site', 'slug',),
        )
        index_together = (
            ('site', 'status', ),
            ('site', 'status', 'publish_date', 'expiry_date'),
        )

    def get_absolute_url(self):
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        activity_workspace_by_created(self)
        return super(Activity, self).save(*args, **kwargs)

    def sync_status(self):
        return sync_status_from(self)


class Bulletin(SiteRelated,
               PublishDisplayable,
               TimeStamped,
               Ownable,
               models.Model):

    objects = BulletinManager()

    title = models.CharField(max_length=500)

    summary = models.CharField(max_length=500)

    content = RichTextField()

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        index_together = (
            ('site', 'status', ),
            ('site', 'status', 'publish_date', 'expiry_date'),
        )
        ordering = ('-publish_date', )

    def get_absolute_url(self):
        return None

    def __str__(self):
        return self.title


# 抽奖

from activity.managers import LotteryManager
from model_utils import Choices


LOTTERY_PRIZE_GROUP = Choices(
    (1, 'real', '实物奖'),
    (0, 'virtual', '虚拟奖'),
)

LOTTERY_PRIZE_LEVEL = Choices(
    (100, 'top', '我是传奇'),
    (70, 'lucky', '一等幸运'),
    (40, 'well', '喜大普奔'),
    (10, 'good', '你是好人'),
    (1, 'again', '再来一次'),
)


class RealPrizeDuplicateAward(Exception):
    pass


class Lottery(PublishDisplayable,
              TimeStamped,
              models.Model):

    objects = LotteryManager()

    title = models.CharField(max_length=500)

    description = models.TextField(verbose_name='抽奖规则')

    cost_coin = models.IntegerField(default=100, verbose_name='消费金币数')

    takepartin_times = models.IntegerField(default=0, editable=False, verbose_name='参与人次')

    takepartin_count = models.IntegerField(default=0, editable=False,verbose_name='参与人数')

    @property
    def active_summary(self):
        return "%s - %s" % (self.publish_date.strftime('%Y-%m-%d'),
                            self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else "")

    class Meta:
        verbose_name = '抽奖'
        verbose_name_plural = '抽奖'
        index_together = (
            ('status',),
            ('status', 'publish_date', ),
            ('status', 'publish_date', 'expiry_date'),
        )

    def __str__(self):
        return self.title

    def is_expired(self, nowdt=None):
        if not self.expiry_date:
            return False
        nowdt = nowdt.astimezone() if nowdt else now().astimezone()
        return nowdt > self.expiry_date.astimezone()

    def is_published(self, nowdt=None):
        if self.status != CONTENT_STATUS_PUBLISHED:
            return False

        nowdt = nowdt.astimezone() if nowdt else now().astimezone()
        return self.publish_date.astimezone() <= nowdt


from model_utils.managers import PassThroughManager


class LotteryPrizeManager(PassThroughManager):

    def drawable(self):
        return self.filter(status=self.model.STATUS.notover)


class LotteryPrize(TimeStamped,
                   models.Model):

    objects = LotteryPrizeManager()

    lottery = models.ForeignKey(Lottery, related_name='prizes',
                                verbose_name='抽奖')

    GROUP = LOTTERY_PRIZE_GROUP

    group = models.IntegerField(choices=LOTTERY_PRIZE_GROUP, verbose_name='奖项组别')

    LEVEL = LOTTERY_PRIZE_LEVEL

    level = models.IntegerField(choices=LOTTERY_PRIZE_LEVEL,
                                verbose_name='奖项等级')

    rate = models.IntegerField(default=0, verbose_name='中奖概率')

    @property
    def level_name(self):
        return self.LEVEL[self.level]

    title = models.CharField(max_length=500, verbose_name='奖项标题')

    total_count = models.IntegerField(default=0, verbose_name='总发放数量')

    win_count = models.IntegerField(default=0, editable=False,
                                    verbose_name='已经中奖人数',
                                    help_text='正常途径中奖者(不包括内定)')

    award_coin = models.IntegerField(default=0, verbose_name='虚拟金币奖励')

    win_prompt = models.CharField(max_length=500, verbose_name='中奖提示')

    STATUS = Choices(
        (0, 'notover', '未结束'),
        (1, 'over', '结束'),
        (2, 'finish', '完成'),
    )

    status = models.IntegerField(verbose_name='领取状态',
                                 choices=STATUS,
                                 default=STATUS.notover,
                                 db_index=True,
                                 help_text="1. notover 未领奖状态; \n"
                                           "2. over 内定和正常途径中奖数获奖结束; total_count 不一\n"
                                           "3. finish 所有奖品发放完成(内定), total_count必定与win_count相等且不为0;"
                                 )

    tracker = FieldTracker()

    class Meta:
        verbose_name = verbose_name_plural = '奖品'
        index_together = (
            ('lottery', 'status', ),
            ('lottery', 'group', 'level'),
        )
        unique_together = (
            ('lottery', 'group', 'level'),
        )
        ordering = ('lottery', '-level',)

    def as_group_cls(self):
        if self.group == self.GROUP.real:
            self.__class__ = RealPrize
            return self
        elif self.group == self.GROUP.virtual:
            self.__class__ = VirtualPrize
            return self
        raise TypeError

    def __str__(self):
        return "%s: %s" %(self.level_name, self.title)

    def sync_win_status(self):
        # 同步奖项获奖状态
        # notover: 内定+中奖 < 预计发放数
        # over: 内定+中奖 == 预计发放数
        # finish: 中奖 == 预计发放数
        if self.pk and self.total_count:
            self.win_count = self.winnings.won().count()
            if self.total_count != self.win_count:
                all_winnings = self.winnings.all()
                if all_winnings.count() >= self.total_count:
                    self.status = self.STATUS.over
                else:
                    self.status = self.STATUS.notover
            else:
                self.status = self.STATUS.finish


class VirtualPrize(LotteryPrize):

    class Meta:
        proxy = True


class RealPrize(LotteryPrize):

    class Meta:
        proxy = True


class LotteryWinningQuerySet(QuerySet):

    def won(self):
        return self.filter(status__gt=self.model.STATUS.unofficial)


class LotteryWinning(TimeStamped,
                     Ownable,
                     models.Model):

    objects = PassThroughManager\
        .for_queryset_class(LotteryWinningQuerySet)()

    lottery = models.ForeignKey(Lottery, related_name='winnings')

    prize = models.ForeignKey(LotteryPrize, related_name='winnings')

    STATUS = Choices(
        (0, 'unofficial', '内定获奖'),
        (1, 'win', '获奖'),
        (2, 'accept', '已领奖'),
    )

    summary = models.CharField(max_length=500, default='')

    status = models.IntegerField(choices=STATUS,
                                 default=STATUS.win,
                                 db_index=True)

    win_date = models.DateTimeField(null=True, verbose_name='获奖时间')

    accept_date = models.DateTimeField(null=True,
                                       blank=True,
                                       verbose_name='领奖时间')

    tracker = FieldTracker()

    class Meta:
        verbose_name = '中奖名单'
        verbose_name_plural = '中奖名单'
        index_together = (
            ('lottery', 'status',),
            ('lottery', 'prize',),
            ('prize', 'status',),
            ('prize', 'status', 'win_date',),
        )

    def save(self, *args, **kwargs):
        if self.tracker.has_changed('status') \
            and not self.summary \
            and self.status > self.STATUS.unofficial:
            self.summary = "%s:%s:%s" % (self.user.username,
                                         self.prize.level_name,
                                         self.prize.title)
        if not self.lottery_id:
            self.lottery_id = self.prize.lottery_id
        return super(LotteryWinning, self).save(*args, **kwargs)

    def __str__(self):
        return self.summary


_has_changed_winning_status_flag = '_has_changed_winning_status'

@receiver(pre_save, sender=LotteryWinning)
def lottery_winning_previous_status_to_change_prize_win_count(sender, instance, *args, **kwargs):
    flag = False
    if instance.pk and instance.tracker.has_changed('status'):
        flag = True
    setattr(instance, _has_changed_winning_status_flag, flag)


@receiver(post_save, sender=LotteryWinning)
def lottery_winning_change_prize_win_count(sender, instance, created, *args, **kwargs):
    prize = None
    if created:
        prize = instance.prize
    elif getattr(instance, _has_changed_winning_status_flag, False):
        prize = instance.prize

    if prize:
        prize.sync_win_status()
        prize.save()

    delattr(instance, _has_changed_winning_status_flag)


@receiver(post_delete, sender=LotteryWinning)
def lottery_winning_post_delete_change_prize_status(sender, instance, *args, **kwargs):
    if instance.prize:
        instance.prize.sync_win_status()
        instance.prize.save()


@receiver(pre_save, sender=LotteryPrize)
def lottery_prize_pre_change_total_count(sender, instance, *args, **kwargs):
    if instance.pk and instance.tracker.has_changed('total_count'):
        instance.sync_win_status()


from random import randint


class BaseLotteryException(ValidationError):

    def __init__(self, code=None, *args, **kwargs):
        code = code if code else self.code
        super(BaseLotteryException, self).__init__(code=code, *args, **kwargs)


class LotteryNotPublished(BaseLotteryException):

    code = 1


class LotteryExpired(BaseLotteryException):

    code = 2


class LotteryMoreCoinRequired(BaseLotteryException):

    code = 3


from account.models import Profile


class LotteryPrizeGiveOutCompletely(BaseLotteryException):
    """
    奖项发放完毕
    """

    code = 101


class LotteryLuckyDraw(object):

    def __init__(self, lottery, request=None, win_date=None):
        self.lottery = lottery
        self.request = request
        self.win_date = win_date.astimezone() if win_date else now().astimezone()

    def __rand_prize(self, prizes):
        reverse_max = max((p.level for p in prizes)) + 1
        pro_sum = sum((reverse_max - p.level for p in prizes))

        for i, p in enumerate(prizes):
            rand_num = randint(1, pro_sum)
            cur_num = reverse_max-p.level
            if rand_num <= cur_num:
                return p
            else:
                pro_sum -= cur_num
        return None

    def _rand_prize(self, prizes):
        pro_sum = sum((p.rate for p in prizes))

        for i, p in enumerate(prizes):
            rand_num = randint(1, pro_sum)
            if rand_num <= p.rate:
                return p
            else:
                pro_sum -= p.rate
        return None

    def get_prizes(self):
        return self.lottery.prizes\
            .filter(status=LotteryPrize.STATUS.notover)

    def filter_real_prize_winned(self, user):
        return self.lottery.winnings.filter(user=user, prize__group=LotteryPrize.GROUP.real)

    def check_drawable(self, user):
        if not self.lottery.is_published(self.win_date):
            raise LotteryNotPublished(message='本次抽奖还未开始')

        if self.lottery.is_expired(self.win_date):
            raise LotteryExpired(message='本次抽奖已经截止')

        if not self.is_user_enough_coin(user):
            raise LotteryMoreCoinRequired(message='少侠，先去赚点金币，再来抽大奖！')

    def is_user_enough_coin(self, user):
        p = Profile.objects.get(user_id=user.pk)
        return p.coin >= self.lottery.cost_coin

    def draw(self, user, check_drawable=False):
        if check_drawable:
            self.check_drawable(user)

        win_date = self.win_date

        prizes_to_rand = self.allowed_prizes(user=user)
        prize = self._rand_prize(prizes_to_rand)
        if prize:
            if hasattr(transaction, 'atomic'):
                _transtaction_draw = self._transaction_draw_with_atomic
            else:
                _transtaction_draw = self._transaction_draw
            return _transtaction_draw(prize=prize, user=user, win_date=win_date)
        return None

    def draw_manually(self, user, prize, check_drawable=False):
        if check_drawable:
            self.check_drawable(user)

        assert prize.lottery_id == self.lottery.pk
        self.check_prize_remaining(prize)

        win_date = self.win_date
        if hasattr(transaction, 'atomic'):
            _transtaction_draw = self._transaction_draw_with_atomic
        else:
            _transtaction_draw = self._transaction_draw
        return _transtaction_draw(prize=prize, user=user, win_date=win_date)

    def check_prize_remaining(self, prize):
        if prize.status != LotteryPrize.STATUS.notover:
            raise LotteryPrizeGiveOutCompletely(message='奖品发放完毕')

    def _transaction_draw(self, prize, user, win_date):
        try:
            sid = transaction.savepoint()
            p = LotteryPrize.objects.select_for_update().get(pk=prize.pk)
            if p.status != LotteryPrize.STATUS.notover:
                transaction.savepoint_rollback(sid)
                return None
            else:
                winning = self.create_winning(prize=p, user=user, win_date=win_date)
                transaction.savepoint_commit(sid)
                self.log_play_credit(user=user,
                                     prize=prize,
                                     win_date=win_date,
                                     winning=winning)
                self.update_lottery_play_takepartin()
                return prize, winning
        except IntegrityError:
            transaction.savepoint_rollback(sid)
        return None

    def _transaction_draw_with_atomic(self, prize, user, win_date):
        try:
            with transaction.atomic():
                p = LotteryPrize.objects.select_for_update().get(pk=prize.pk)
                if p.status != LotteryPrize.STATUS.notover:
                    return None
                else:
                    winning = self.create_winning(prize=p, user=user, win_date=win_date)
                    self.log_play_credit(user=user,
                                         prize=prize,
                                         win_date=win_date,
                                         winning=winning)
                    self.update_lottery_play_takepartin()
                    return prize, winning
        except IntegrityError:
            return None

    def allowed_prizes(self, user):
        # 已经抽中实物奖的用户，排除本次抽中实物奖机会
        # filter real prizes
        real_prizes = self.filter_real_prize_winned(user)
        prizes = self.get_prizes()
        if real_prizes.exists():
            prizes_to_rand = list(filter(lambda i:i.group != LotteryPrize.GROUP.real, prizes))
        else:
            prizes_to_rand = prizes
        return prizes_to_rand

    def create_winning(self, prize, user, win_date):
        #if prize.group == LotteryPrize.GROUP.real:
        winning = LotteryWinning.objects.create(prize=prize,
                                                lottery=self.lottery,
                                                user=user,
                                                status=LotteryWinning.STATUS.win,
                                                win_date=win_date)
        return winning
        #else:
        #    rt = None

    def log_play_credit(self, user, prize, win_date, winning=None, *args, **kwargs):
        from account.documents.credit import CreditLog
        from activity.documents.actions.lottery import LotteryPlayAction, LotteryWinningAction

        action_uuid = uuid()

        ip_address = self.request.client_ip() if self.request and hasattr(self.request, 'client_ip') else None
        play_action = LotteryPlayAction(user=user,
                                        lottery=self.lottery,
                                        credit_exchange_coin=-abs(self.lottery.cost_coin),
                                        action_uuid=action_uuid,
                                        ip_address=ip_address,
                                        )
        play_action.save()
        log = CreditLog.factory(exchangable=play_action, user=user,
                          credit_datetime=win_date,
                          )
        if not log.pk:
            log.save()

        winning_action = LotteryWinningAction(user=user,
                                              prize=prize,
                                              lottery=self.lottery,
                                              play_action=play_action,
                                              credit_exchange_coin=prize.award_coin,
                                              action_uuid=action_uuid,
                                              ip_address=ip_address,
                                              )
        if winning:
            winning_action.winning = winning

        winning_action.save()
        log = CreditLog.factory(exchangable=winning_action, user=user,
                          credit_datetime=win_date,
                          )
        if not log.pk:
            log.save()

        play_action.winning_action = winning_action
        play_action.save()

    def update_lottery_play_takepartin(self):
        from activity.documents.actions.lottery import lottery_sum_play_takepartin
        self.lottery.takepartin_count, self.lottery.takepartin_times = lottery_sum_play_takepartin(self.lottery.pk)
        self.lottery.save()
