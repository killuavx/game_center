# -*- coding: utf-8 -*-
from model_utils import Choices
from mongoengine import fields, queryset, DoesNotExist
from mongoengine.document import DynamicDocument, DynamicEmbeddedDocument
from account.models import User
from account.documents.credit import CreditLog
from activity.documents.actions.base import Action, Task, TaskRule, Ownerable, TaskAlreadyDone

from django.utils.timezone import now
from random import randint
import uuid

db_alias = 'data_center'


class ActionExcutable(object):

    def execute(self):
        pass

    def can_execute(self):
        return False


class ActionBindLottery(object):

    task = fields.ReferenceField('LotteryTask', dbref=False, required=False)

    lottery_id = fields.IntField()

    _lottery = False

    @property
    def lottery(self):
        if self.lottery_id and self._lottery is False:
            from activity import models
            try:
                self._lottery = models.Lottery.objects.get(pk=self.lottery_id)
            except models.Lottery.DoesNotExist:
                self._lottery = None
                self.lottery_id = None
        return self._lottery

    @lottery.setter
    def lottery(self, obj):
        if obj is not None:
            self._lottery = obj
            self.lottery_id = obj.pk
        else:
            self._lottery = None
            self.lottery_id = None

    @property
    def content(self):
        return self.lottery

    @content.setter
    def content(self, obj):
        self.lottery = obj


class LotteryPlayAction(ActionExcutable, ActionBindLottery, Action):

    CODE = 'lottery_play'

    winning_action = fields.ReferenceField('LotteryWinningAction',
                                           required=False,
                                           dbref=False)

    def build_summary(self):
        return "%s 参与 %s 抽奖活动" %(self.user.username, self.lottery)


class ActionBindLotteryWinning(ActionBindLottery):

    _prize = None

    prize_id = fields.IntField()

    prize_level = fields.IntField()

    prize_level_name = fields.StringField()

    prize_title = fields.StringField()

    prize_group = fields.IntField()

    _winning = False

    winning_id = fields.IntField()

    @property
    def winning(self):
        if self._winning:
            return self._winning

        if self.winning_id and self._winning is False:
            from activity import models
            try:
                self._winning = models.LotteryWinning.objects.get(pk=self.winning_id)
            except models.LotteryWinning.DoesNotExist:
                self._winning = None
        return self._winning

    @winning.setter
    def winning(self, obj):
        if obj is not None:
            self._winning = obj
            self.winning_id = obj.pk
        else:
            self._winning = None
            self.winning_id = None

    _prize = False

    @property
    def prize(self):
        if self._prize:
            return self._prize
        if self.prize_id and self._prize is False:
            from activity import models
            try:
                self._prize = models.LotteryPrize.objects.get(pk=self.prize_id)
                self.prize_level = self._winning.prize.level
                self.prize_level_name = self._winning.prize.level_name
                self.prize_gorup = self._winning.prize.group
            except models.LotteryPrize.DoesNotExist:
                self._prize = None
        return self._prize

    @prize.setter
    def prize(self, obj):
        if obj is None:
            self.prize_id = None
            self.prize_level = None
            self.prize_level_name = None
            self.prize_group = None
            self.prize_title = None
        else:
            self.prize_id = obj.pk
            self._prize = obj
            self.prize_group = obj.group
            self.prize_level = obj.level
            self.prize_level_name = obj.level_name
            self.prize_title = obj.title


class LotteryWinningActionQuerySet(queryset.QuerySet):

    def lottery_winning_list(self, lottery_id):
        return self.filter(lottery_id=lottery_id).order_by('-prize_level', '-win_date')


class LotteryWinningAction(ActionExcutable, ActionBindLotteryWinning, Action):

    CODE = 'lottery_winning'

    play_action = fields.ReferenceField(LotteryPlayAction,
                                        required=True,
                                        dbref=False)
    @property
    def content(self):
        return self.winning

    @content.setter
    def content(self, obj):
        self.winning = obj

    username = fields.StringField()

    @property
    def user(self):
        return super(LotteryWinningAction, self).user

    @user.setter
    def user(self, user=None):
        if user is None:
            self._user = None
            self.user_id = None
        else:
            self._user = user
            self.user_id = user.pk
            self.username = user.username

    win_date = fields.DateTimeField(default=lambda: now().astimezone())

    def build_summary(self):
        return "%s 抽中了 %s:%s" %(self.username, self.prize_level_name, self.prize_title)

    meta = {
        'db_alias': db_alias,
        'indexes': [
            ['lottery_id', ],
            ['lottery_id', 'user'],
            ['lottery_id', '-prize_level', '-win_date'],
        ],
        'queryset_class': LotteryWinningActionQuerySet,
    }

    def __str__(self):
        if not self.winning_id:
            return None
        return "%s 抽中 %s(%s)" %(self.username, self.prize_level_name, self.prize_title)


class LotteryPrize(DynamicEmbeddedDocument):

    prize_id = fields.IntField()

    level_name = fields.StringField()

    level = fields.IntField()

    group = fields.IntField()

    title = fields.StringField()

    win_prompt = fields.StringField()

    award_coin = fields.IntField(default=0)

    STATUS = Choices(
        (0, 'notover', '未结束'),
        (1, 'over', '结束'),
    )

    #status = fields.IntField(verbose_name='领取状态',
    #                         choices=STATUS,
    #                         default=STATUS.notover,)


class NoneLottery(object):
    pass


class LotteryExpiry(TaskAlreadyDone):
    pass


class LotteryDone(TaskAlreadyDone):
    pass


class LotteryTask(Task):

    CODE = 'lottery'

    code = fields.StringField(default='lottery')

    title = fields.StringField()

    user_id = fields.IntField(default=0)

    lottery_id = fields.IntField()

    _lottery = False

    @property
    def lottery(self):
        if self.lottery_id and self._lottery is False:
            from activity import models
            try:
                lottery = models.Lottery.objects.get(pk=self.lottery_id)
                self._update_lottery(lottery)
            except models.Lottery.DoesNotExist:
                self._update_lottery(None)
        return self._lottery

    @lottery.setter
    def lottery(self, obj):
        self._update_lottery(obj)

    def _update_lottery(self, obj):
        if obj is not None:
            self._lottery = obj
            self.lottery_id = obj.pk
            self.title = obj.title
            self.cost_coin = obj.cost_coin
            self.description = obj.description
        else:
            self._lottery = None
            self.lottery_id = None

    name = fields.StringField(default='抽奖')

    takepartin_times = fields.IntField(default=0)

    takepartin_count = fields.IntField(default=0)


    prizes = fields.SortedListField(fields.EmbeddedDocumentField(LotteryPrize),
                                    ordering='level',
                                    reverse=True)

    publish_date = fields.DateTimeField()

    expiry_date = fields.DateTimeField()

    cost_coin = fields.IntField(default=0)

    @classmethod
    def get_action_class(cls, *args, **kwargs):
        if kwargs.get('type') == 'winning':
            return LotteryWinningAction
        return LotteryPlayAction

    @classmethod
    def factory_action(cls, user, type=None, play_action=None, *args, **kwargs):
        action_cls = cls.get_action_class(type=type)
        action = action_cls(user=user,
                            ip_address=kwargs.get('ip_address'))
        if type == 'winning':
            assert play_action
            action.play_action = play_action
            action.task = play_action.task
            action.ip_address = play_action.ip_address
        return action

    def update_action(self, user, action, rule, rule_status, *args, **kwargs):
        if TaskRule.STATUS.posted == rule_status:
            self.rule = rule
            self.credit_exchange_coin = -abs(self.lottery.cost_coin)
        action.credit_exchange_coin = self.credit_exchange_coin
        action.task = self

        if not action.id:
            action.save()

        self.actions.append(action)
        self.ip_address = action.ip_address
        self.updated_datetime = action.created_datetime

    def process(self, action, rule, *args, **kwargs):
        rule_pre_check_status = rule.pre_update_action_check(task=self, action=action, *args, **kwargs)

        if TaskRule.STATUS.done == rule_pre_check_status:
            raise TaskAlreadyDone

        self.update_action(user=action.user, action=action,
                           rule=rule, rule_status=rule_pre_check_status,
                           *args, **kwargs)

        rule_status = rule.post_update_action_check(task=self, action=action, *args, **kwargs)

        if TaskRule.STATUS.done == rule_status:
            raise TaskAlreadyDone

        rule.draw(action=action)

        self.update_status(user=action.user, action=action,
                           rule_status=rule_status, *args, **kwargs)

        self.save()

        if rule_status == TaskRule.STATUS.finish \
            and self.status == self.STATUS.done:
            self.make_done()

        return self

    @classmethod
    def get_rule_class(cls):
        return LotteryRule

    @classmethod
    def factory_rule(cls, *args, **kwargs):
        rule_cls = cls.get_rule_class()
        try:
            return rule_cls.objects.get(code=rule_cls.CODE)
        except:
            rule = rule_cls(code="%s" % rule_cls.CODE)
            rule.save()
            return rule

    @classmethod
    def factory(cls, lottery, user, action_datetime=None, *args, **kwargs):
        """
            factory
                ::task
                ::user
                ::action
                ::rule
        """
        task = cls.factory_task(lottery=lottery,
                                action_datetime=action_datetime)
        rule = cls.factory_rule()

    @classmethod
    def factory_task(cls, lottery=None, *args, **kwargs):
        try:
            if lottery:
                task = cls.objects.get(lottery_id=lottery.pk)
            else:
                task = cls.objects.order_by('-publish_date')[0]
        except (IndexError, DoesNotExist) as e:
            task = cls(title=lottery.title,
                       cost_coin=lottery.cost_coin,
                       publish_date=lottery.publish_date.astimezone(),
                       expiry_date=lottery.expiry_date.astimezone(),
                       )
            task.lottery = lottery
            if kwargs.get('action_datetime'):
                task.created_datetime = kwargs.get('action_datetime').astimezone()

            if not task.created_datetime:
                task.created_datetime = task.publish_date

            for p in lottery.prizes.all():
                task.prizes.append(LotteryPrize(
                    prize_id=p.pk,
                    level_name=p.level_name,
                    level=p.level,
                    group=p.group,
                    title=p.title,
                    win_prompt=p.win_prompt,
                    award_coin=p.award_coin,
                ))
            task.save()
        return task

    def make_done(self):
        pass

    def is_expired(self, nowdt=None):
        if not self.expiry_date:
            return False
        nowdt = nowdt.astimezone() if nowdt else now().astimezone()
        return nowdt > self.expiry_date.astimezone()

    def is_published(self, nowdt=None):
        if self.status not in (self.STATUS.posted, self.STATUS.inprogress):
            return False

        nowdt = nowdt.astimezone() if nowdt else now().astimezone()
        return self.publish_date.astimezone() >= nowdt


class LotteryRule(TaskRule):

    CODE = 'lottery'

    def pre_update_action_check(self, task, action, *args, **kwargs):
        if task.id:
            return self.STATUS.inprogress
        else:
            return self.STATUS.posted

    def post_update_action_check(self, task, action, *args, **kwargs):
        if task.id:
            return self.STATUS.inprogress
        else:
            return self.STATUS.posted


def lottery_sum_play_takepartin(lottery_id):
    cls = LotteryPlayAction
    code = LotteryPlayAction.CODE
    collection, cls_name = cls._meta['collection'], cls._types[0]
    result = cls.objects.exec_js("""function(){
        var result = db.runCommand({
            group: {
                ns:'%(collection)s',
                key: { _cls:1, lottery_id:1, user_id:1 },
                cond: { code:"%(code)s", lottery_id:%(lottery_id)d },
                $reduce: function(cur, result){},
                initial: {}
            }
        });
        delete result['retval'];
        return result;
    }""" % dict(code=code,
                collection=collection,
                lottery_id=lottery_id))
    takepartin_count = result.get('keys')
    takepartin_times = result.get('count')
    return takepartin_count, takepartin_times
