# -*- coding: utf-8 -*-
from mongoengine import fields, queryset
from mongoengine.document import DynamicDocument
from account.models import User
from account.documents.credit import CreditLog
from activity.documents.actions.base import Action

from django.utils.timezone import now
from random import randint
import uuid


class ScratchRule(DynamicDocument):
    """
    刮奖规则
    """

    group = fields.UUIDField(binary=False,
                             unique=False,
                             default=uuid.uuid4)

    coins = fields.ListField(fields.IntField())

    winning_rate = fields.IntField()

    meta = {
        'db_alias': 'data_center',
        'collection': 'activity_scratchrule',
        'indexes': [
            ['group', 'winning_rate'],
            ],
        }

    def rand_coin(self):
        return self.coins[randint(0, len(self.coins)-1)]

    def __str__(self):
        return "%s, %s, %s" % (self.group, self.winning_rate, self.coins)


class ScratchCardQuerySet(queryset.QuerySet):

    def received(self, reverse=True):
        qs = self.filter(is_received=True)
        if reverse:
            return qs.order_by('-received_datetime')
        return qs


class ScratchCard(DynamicDocument):

    rule = fields.ReferenceField(ScratchRule,
                                 dbref=False,
                                 verbose_name='刮奖规则')

    title = fields.StringField(verbose_name='刮奖标题')

    signcode = fields.UUIDField(verbose_name='刮奖码',
                                binary=False,
                                unique=True,
                                default=uuid.uuid4)

    winner_id = fields.IntField(verbose_name='获奖用户ID', required=False)

    winner_name = fields.StringField(verbose_name='获奖用户明', required=False)

    is_received = fields.BooleanField(verbose_name='已领取', default=False)

    received_datetime = fields.DateTimeField(verbose_name='领取时间',
                                             required=False, default=None)

    updated_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    created_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    award_coin = fields.IntField(verbose_name='奖励金币')

    meta = {
        'db_alias': 'data_center',
        'collection': 'activity_scratchcard',
        'indexes': [
            ['rule',],
            ['signcode',],
            ['winner_id',],
            ['winner_id', 'is_received'],
            ['is_received', '-received_datetime', ],
            ],
        'queryset_class': ScratchCardQuerySet,
        }

    @property
    def winner(self):
        if not hasattr(self, 'user'):
            try:
                self._user = User.objects.get(pk=self.winner_id)
                self.winner_name = self._user.username
            except:
                self._user = None
        return self._user

    @winner.setter
    def winner(self, user):
        self._user = user
        self.winner_id = user.pk
        self.winner_name = user.username

    def save(self, *args, **kwargs):
        self.updated_datetime = now().astimezone()
        return super(ScratchCard, self).save(*args, **kwargs)

    def __str__(self):
        return "%s, %s" % (self.title, self.signcode)


class ScratchLuckyDraw(object):

    rule_class = ScratchRule

    _DEFAULT_GROUP_UUID = uuid.UUID('cb4e6bab-3bb4-4530-bf7b-e662c523742d')
    _DEFAULT_RULES = (
        (5, [0]),
        (90, range(1, 10)),
        (4, range(10, 50+1, 10)),
        (1, range(60, 100+1, 10)),
    )

    @classmethod
    def generate_rules(self):
        for dr in self._DEFAULT_RULES:
            rule = self.rule_class(group=self._DEFAULT_GROUP_UUID,
                                   winning_rate=dr[0],
                                   coins=list(dr[1]))
            rule.save()

    def __init__(self, group=None):
        self.group = group if group else self._DEFAULT_GROUP_UUID

    def get_rules(self):
        qs = self.rule_class.objects.filter(group=self.group)
        if qs.count() == 0:
            self.generate_rules()
        return qs

    def rand_rule(self):
        if not hasattr(self, 'rules'):
            self.rules = self.get_rules()
        return self._rand(self.rules)

    def _rand(self, rules):
        pro_sum = sum((r.winning_rate for r in rules))
        for i, r in enumerate(rules):
            rand_num = randint(1, pro_sum)
            if rand_num <= r.winning_rate:
                return r
            else:
                pro_sum -= r.winning_rate
        return None


class OwnerNotMatch(Exception):
    pass


class ScratchAction(Action):

    CODE = 'scratch'

    name = fields.StringField(default='刮刮卡')

    card = fields.GenericReferenceField()

    def build_summary(self):
        return "刮中%d金币" % self.credit_exchange_coin

    @property
    def content(self):
        return self.card

    @content.setter
    def content(self, content):
        self.card = content

    def can_execute(self):
        if self.card and self.card.award_coin:
            return True
        return False

    def execute(self):
        log = CreditLog.factory(exchangable=self,
                                user=self.card.winner,
                                credit_datetime=self.card.received_datetime)
        log.save()

    def save(self, *args, **kwargs):
        self.credit_exchange_coin = self.card.award_coin
        return super(ScratchAction, self).save(*args, **kwargs)


scratch_luckydraw = ScratchLuckyDraw()


def generate_scratchcard_by_user(user):
    rule = scratch_luckydraw.rand_rule()
    coin = rule.rand_coin()
    return ScratchCard(winner=user,
                       rule=rule,
                       title='+%d金币' % coin if coin else '谢谢参与',
                       award_coin=coin)


def receive_scratchcard(queryset, signcode, user, ip_address=None):
    card = queryset.get(signcode=signcode)
    if card.winner_id != user.pk:
        raise OwnerNotMatch
    if card.is_received is True:
        return card
    card.is_received = True
    card.received_datetime = now().astimezone()
    card.save()

    action = ScratchAction(content=card,
                           user=user,
                           ip_address=ip_address,
                           created_datetime=card.received_datetime)
    action.save()
    if action.can_execute():
        action.execute()

    return card
