# -*- coding: utf-8 -*-
from django.utils.timezone import now
from mongoengine import fields
from mongoengine.document import DynamicDocument, DynamicEmbeddedDocument
from activity.documents.base import Ownerable

PREFIX = 'account'

db_alias = 'data_center'


def collection_name(name):
    return "%s_%s" %(PREFIX, name)


class CreditValue(DynamicEmbeddedDocument):

    coin = fields.IntField()

    experience = fields.IntField()


class CreditLog(Ownerable, DynamicDocument):

    summary = fields.StringField()

    exchange = fields.GenericReferenceField()

    created_datetime = fields.DateTimeField(default=lambda: now().astimezone())

    from_value = fields.EmbeddedDocumentField(CreditValue)

    to_value = fields.EmbeddedDocumentField(CreditValue)

    @classmethod
    def factory(cls, exchangable, user, credit_datetime):
        log = cls(exchange=exchangable,
                  user=user,
                  created_datetime=credit_datetime
        )
        return log.process()

    def process(self):
        from_val = CreditValue(
            coin=self.user.profile.coin,
            experience=self.user.profile.experience
        )
        exchange = self.exchange
        self.summary = exchange.build_summary()
        to_val = CreditValue(
            coin=from_val.coin+exchange.credit_exchange_coin,
            experience=from_val.experience+exchange.credit_exchange_experience
        )
        self.user.profile.change_experience(to_val.experience)
        self.user.profile.coin = to_val.coin
        self.from_value = from_val
        self.to_value = to_val
        self.save()
        return self

    def save(self, *args, **kwargs):
        tracker = self.user.profile.tracker
        if tracker.has_changed('coin') or tracker.has_changed('experience'):
            self.user.profile.save()
        return super(CreditLog, self).save(*args, **kwargs)

    meta = {
        'allow_inheritance': True,
        'db_alias': db_alias,
        'collection': collection_name('creditlog'),
        'indexes': [
            ('user_id', 'created_datetime', ),
            ('user_id', '-created_datetime', ),
            ],
        }


class CreditExchangable(object):

    def build_summary(self):
        raise NotImplementedError

    credit_exchange_coin = fields.IntField(default=0, required=False)

    credit_exchange_experience = fields.IntField(default=0, required=False)


